from datetime import datetime

from . import app


@app.template_filter()
def format_dt(x, format="%Y-%m-%d"):
    return x.strftime(format)


@app.template_filter()
def timestamp_to_dt(timestamp):
    return datetime.fromtimestamp(timestamp)
