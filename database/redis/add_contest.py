import redis
from rq import Queue

from datetime import timedelta
import time

from tasks import finish_contest


r = redis.Redis()
q = Queue(connection=r)


def add_contest(contest_id: int):
    s = q.enqueue_in(timedelta(seconds=5), finish_contest, contest_id)
    print(s.get_status())
    time.sleep(5)
    print(s.get_status())
