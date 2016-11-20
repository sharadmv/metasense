import logging
logging.basicConfig(level=logging.INFO, name=__name__)
import requests
from path import Path
from bs4 import BeautifulSoup

BASE_URL = "http://jtimmer.cts.com"

from argparse import ArgumentParser

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument('year')
    argparser.add_argument('month')
    argparser.add_argument('--data_dir', default='data/')
    return argparser.parse_args()

def get_urls(base_url):
    soup = BeautifulSoup(requests.get(base_url).text, "html.parser")
    return soup.find_all('a')

def get_csv(data_dir, base_url, csv_url):
    if (data_dir / csv_url).exists():
        logging.info("Loading %s from file." % csv_url)
        with open(data_dir / csv_url) as fp:
            csv_text = fp.read()
        return csv_text
    logging.info("Fetching %s from website." % csv_url)
    csv_text = requests.get(base_url + '/' + csv_url).text.encode('utf-8')
    with open(data_dir / csv_url, 'w') as fp:
        fp.write(csv_text)
    return csv_text

def get_csvs(data_dir, base_url, csv_links):
    csvs = {}
    for link in csv_links:
        csvs[link['href']] = get_csv(data_dir, base_url, link['href'])
    return csvs

def main():
    args = parse_args()

    data_dir = Path(args.data_dir) / args.month / args.year

    data_dir.makedirs_p()

    base_url = "%s/%s/%s%s" % (BASE_URL, args.year, args.month, args.year[-2:])

    links = get_urls(base_url)
    csv_links = [link for link in links if link['href'].split('_')[0] == "yesterday"]
    logging.info("Fetching %u CSVs from %s" % (len(csv_links), base_url))
    csvs = get_csvs(data_dir, base_url, csv_links)

    return csvs


if __name__ == "__main__":
    blah = main()
