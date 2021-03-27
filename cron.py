from apscheduler.schedulers.background import BlockingScheduler
import datetime
from scrape import *

scheduler = BlockingScheduler()
if __name__ == '__main__':
    try:
        scheduler.add_job(parse_html, 'cron', timezone='Europe/London',
                          start_date=datetime.datetime.now(), hour='*', minute='*', second='*/5',day_of_week='mon-sun')
        scheduler.start()
    except Exception as e:
        print(e, e.__class__)