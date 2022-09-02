import datetime
import time

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    logger.info("The sample task just ran.")
    return True


@shared_task
def sample_task():
    logger.info(f'The sample task just ran at {datetime.datetime.now()}.')
