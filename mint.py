import requests
import os
import time
import logging
import json


def read_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{symbol}?interval=5m"
    logging.info(f"Getting {url}...")
    try:
        r = requests.get(url)
        logging.debug(r.text)
        j = json.loads(r.text)
        market_price = j["chart"]["result"][0]["meta"]["regularMarketPrice"]
        logging.info(f"{symbol} is {market_price}")
        return market_price
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
