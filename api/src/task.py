import time

from celery import shared_task


@shared_task(bind=True, ignore_result=False)
def background_task(self, a: int, b: int) -> int:
    self.update_state(state='PROGRESS', meta={'current': 1, 'total': 10})
    time.sleep(10)
    self.update_state(state='PROGRESS', meta={'current': 2, 'total': 10})
    raise ValueError('test')
    return a + b + 1 + 1
