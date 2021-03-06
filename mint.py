import requests
import os
import time
import logging

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    DT_METRICS_INGEST_URL = os.environ.get('DT_METRICS_INGEST_URL')
    logging.info(DT_METRICS_INGEST_URL)
    DT_METRIC_INGEST_TOKEN = os.environ.get('DT_METRIC_INGEST_TOKEN')
    logging.info(DT_METRIC_INGEST_TOKEN)

    while True:
        headers = {'Content-Type': 'text/plain',
                'Authorization': "Api-Token " + DT_METRIC_INGEST_TOKEN}
        payload = "curl.test 1"
        try:
            r = requests.post(DT_METRICS_INGEST_URL, headers=headers, data=payload, verify=False)
            logging.info(r.text)
        except Exception as e:
            logging.error("Error sending MINT metric", exc_info=True)

        logging.info("Going sleep...")
        time.sleep(20)

if __name__ == '__main__':
    main()