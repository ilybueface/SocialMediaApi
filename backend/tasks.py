import time
from celery import shared_task
from requests.exceptions import ConnectionError, Timeout


@shared_task(
    autoretry_for=(ConnectionError, Timeout),
    max_retries=20,
    retry_backoff=True,
    retry_backoff_max=30,
    retry_jitter=True
)
def send_user_notification(author_id, text):
    time.sleep(2)
    print(f"Notifications for {author_id} - {text} was sent")
