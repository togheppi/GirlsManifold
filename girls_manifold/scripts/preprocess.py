import argparse

from scrapy import Selector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inpath')
    parser.add_argument('outpath')
    return parser.parse_args()


def preprocess(inpath, outpath):

    with open(inpath) as infile:
        selector = Selector(text=infile.read())

    games = selector.xpath('//div[@id="query_result_main"]//tr')[1:]

    with open(outpath, 'w') as outfile:
        for game in games:
            tokens = game.xpath('td/text()').extract()
            tokens[-1] = 'http://' + tokens[-1] + '&gc=gc'
            outfile.write('\t'.join(tokens) + '\n')


def main():
    preprocess(**vars(parse_args()))


if __name__ == '__main__':
    main()
