import argparse
import json
import logging
import os
import shutil

from tqdm import tqdm

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--items-path', required=True)
    parser.add_argument('--games-path', required=True)
    parser.add_argument('--year', default='2005')
    return parser.parse_args()


def load_games(path, year):
    games = set()
    with open(path) as infile:
        for line in infile:
            tokens = line.split('\t')
            url = tokens[-1].strip()
            date = tokens[2]
            if date >= year:
                games.add(url)
    return games


def load_items(path, games):
    items = set()
    with open(path) as infile:
        for line in infile:
            item = json.loads(line)
            url = item['game_url']
            if url in games:
                for image_item in item['images']:
                    items.add(image_item['path'])
    return items


def select(input_dir, output_dir, items_path, games_path, year):
    games = load_games(games_path, year)
    logging.warning('%d games loaded', len(games))
    items = load_items(items_path, games)
    logging.warning('%d items loaded', len(items))

    os.makedirs(output_dir, exist_ok=True)
    for path in tqdm(items):
        name = os.path.basename(path)
        src_path = os.path.join(input_dir, path)
        dst_path = os.path.join(output_dir, name)
        shutil.copyfile(src_path, dst_path)


def main():
    args = parse_args()
    select(**vars(args))


if __name__ == '__main__':
    main()
