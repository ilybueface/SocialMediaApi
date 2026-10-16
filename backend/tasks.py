import time
from celery import shared_task


@shared_task
def send_user_notification(author_id, text):
    time.sleep(2)
    print(f"Notifications for {author_id} - {text} was sent")
