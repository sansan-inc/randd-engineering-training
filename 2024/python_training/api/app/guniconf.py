# Gunicorn config file
# see https://docs.gunicorn.org/en/stable/settings.html

wsgi_app = "app.main:app"
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
workers = 2

# logging
accesslog = "-"
errorlog = "-"
loglevel = "error"

# https://github.com/benoitc/gunicorn/pull/862#issuecomment-53175919
max_requests = 500
max_requests_jitter = 200
