import requests
import os
import time
import logging
import json


def read_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{symbol}?interval=5m"
    logging.info(f"Getting {url}...")
    try:
        headers = {"User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36"}
        r = requests.get(url, headers=headers)
        logging.info(r.text)
        status_code = r.status_code
        if (status_code == 200):
            j = json.loads(r.text)
            logging.debug(j)
            market_price = j["chart"]["result"][0]["meta"]["regularMarketPrice"]
            logging.debug(f"{symbol} is {market_price}")
            return market_price
        else:
            logging.error(f"HTTP error {status_code}")
    except Exception as e:
        logging.error(f"Error reading price from {url}", exc_info=True)


def write_metrics(url, token, payload):
    headers = {'Content-Type': 'text/plain',
               'Authorization': "Api-Token " + token}

    logging.debug(f"Writing mint lines: {payload}")
    try:
        r = requests.post(url, headers=headers, data=payload, verify=False, allow_redirects=False)
        logging.info(r.text)
        if r.status_code == 302:
            redirect_url = r.headers['Location']
            logging.info(f"Redirecting to {redirect_url}...")
            r = requests.post(redirect_url, headers=headers, data=payload, verify=False, allow_redirects=False)
            logging.info(r.text)
    except Exception as e:
        logging.error("Error sending MINT metric", exc_info=True)


def build_mint_line(symbol, market_price):
    line = f"nasdaq.price,symbol={symbol} {market_price}"
    logging.debug(f"MINT line: {line}")
    return line


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    dt_metric_ingest_url = os.environ.get('DT_METRICS_INGEST_URL')
    logging.info(dt_metric_ingest_url)
    dt_metric_ingest_token = os.environ.get('DT_METRIC_INGEST_TOKEN')
    logging.info(dt_metric_ingest_token)

    symbols = ["DT", "DDOG", "NEWR", "SPLK", "NOW"]

    while True:
        mint_lines = []
        for symbol in symbols:
            market_price = read_price(symbol)
            line = build_mint_line(symbol=symbol, market_price=market_price)
            mint_lines.append(line)
        write_metrics(url=dt_metric_ingest_url, token=dt_metric_ingest_token, payload='\n'.join(mint_lines))
        logging.info("Going sleep...")
        time.sleep(60)


if __name__ == '__main__':
    main()
