from main import app, datetime, time

@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""

    now_timestamp = time.time()  # 클라이언트의 현재 시간
    # 시간 차이 = datetime형 현재시간 - datetime형 UTC 시간
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp(int(value) / 1000) + offset
    return value.strftime('%Y-%m-%d %H:%M:%S')