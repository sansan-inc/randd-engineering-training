# Gunicorn config file
# see https://docs.gunicorn.org/en/stable/settings.html

from multiprocessing import cpu_count

wsgi_app = "app.main:app"
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
workers = cpu_count() * 2 + 1

# logging
accesslog = "-"
errorlog = "-"
loglevel = "error"

# https://github.com/benoitc/gunicorn/pull/862#issuecomment-53175919
max_requests = 500
max_requests_jitter = 200
