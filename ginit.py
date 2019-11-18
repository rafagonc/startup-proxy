# Gunicorn configuration file in staging/production

import multiprocessing

bind = '0.0.0.0:8080'

# keyfile = os.getenv('SSL_KEYFILE_PATH')
# certfile = os.getenv('SSL_CERTFILE_PATH')

timeout = 60
gracefultimeout = 20
workers = (multiprocessing.cpu_count() * 2) + 1
loglevel = 'debug'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # noqa
accesslog = '-'
