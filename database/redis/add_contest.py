import redis
from rq import Queue

from datetime import timedelta
import time

from tasks import finish_contest


r = redis.Redis()
q = Queue(connection=r)


def add_contest(contest_id: int, days: int):
    q.enqueue_in(timedelta(days=days), finish_contest, contest_id)

