from celery import Celery

from app.core.config import settings

app = Celery("congresslens", broker=settings.redis_url, backend=settings.redis_url)

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]