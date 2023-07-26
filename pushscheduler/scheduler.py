from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import register_events
from goal.models import Goal, ImpossibleDates
from account.models import UserProfile
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q


def start():
    scheduler = BackgroundScheduler(timezone = settings.TIME_ZONE)
    register_events(scheduler)

    scheduler.add_job(
        get_user_daily_schedule,
        #trigger = CronTrigger(second=0),
        'interval', seconds = 3,
        max_instances=1,
        name="daily_schedule",
    )

    scheduler.start()

def get_user_daily_schedule() -> None:
    all_users = User.objects.all()
    current_date = date.today()

    for user in all_users:
      goal_strings = [f"{UserProfile.objects.get(user=user).nickname}님의 오늘 할 일은"]
      goals = Goal.objects.filter(user=user, start_at__lte=current_date, finish_at__gte=current_date)
      for goal in goals:
        if ImpossibleDates.objects.filter(goal=goal, date=current_date).exists():
          continue
        title = goal.title
        days_diff = (goal.finish_at - current_date).days
        impossible_days = ImpossibleDates.objects.filter(goal=goal, date__gte=current_date).count()
        days = days_diff - impossible_days
        estimated_time = int(goal.residual_time/days)
        estimated_minute = int((goal.residual_time/days - int(goal.residual_time/days))*60)
        goal_string = f"{title} : {estimated_time} 시간 {estimated_minute} 분"
        goal_strings.append(goal_string)
      goal_strings.append(f"입니다.")
      
    
      for goal_str in goal_strings:
        print(goal_str)
      print()

# def job():
#     print("----------")


# def main():
#     sched = BackgroundScheduler()
#     sched.add_job(job,'interval', seconds=3, id='test')
#     sched.start()
