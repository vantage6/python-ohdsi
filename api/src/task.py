import time

from celery import shared_task


@shared_task(ignore_result=False)
def background_task(a: int, b: int) -> int:
    time.sleep(10)
    return a + b
