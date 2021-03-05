import requests, os, time

DT_METRICS_INGEST_URL=os.environ.get('DT_METRICS_INGEST_URL')
print(DT_METRICS_INGEST_URL)
DT_METRIC_INGEST_TOKEN=os.environ.get('DT_METRIC_INGEST_TOKEN')
print(DT_METRIC_INGEST_TOKEN)

while True:
    headers = {'Content-Type': 'text/plain',
            'Authorization': "Api-Token " + DT_METRIC_INGEST_TOKEN}
    payload = "curl.test 1"
    r = requests.post(DT_METRICS_INGEST_URL, headers=headers, data=payload)
    print(r.text)
    print("Going sleep...")
    time.sleep(20)