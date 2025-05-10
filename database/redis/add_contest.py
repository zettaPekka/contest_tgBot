import redis
from rq import Queue

from datetime import timedelta

from database.redis.tasks import finish_contest


r = redis.Redis()
q = Queue(connection=r)


def add_contest(contest_id: int, days: float):
    q.enqueue_in(timedelta(days=days), finish_contest, contest_id)

