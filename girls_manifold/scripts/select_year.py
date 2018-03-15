import argparse
import json
import logging
import os
import shutil
import cv2

from tqdm import tqdm

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', default='../../anime_faces/images')
    parser.add_argument('--output-dir', default='../../data')
    parser.add_argument('--items-path', default='../../data/chu.jl')
    parser.add_argument('--games-path', default='../../data/results.tsv')
    parser.add_argument('--year', type=int, default=2005)
    parser.add_argument('--step', type=int, default=None)
    return parser.parse_args()


def load_games(path, year, step):
    games = set()
    with open(path) as infile:
        for line in infile:
            tokens = line.split('\t')
            url = tokens[-1].strip()
            date = int(tokens[2].split('-')[0])
            if step is None:
                if date >= year:
                    games.add(url)
            else:
                if (date >= year) & (date < year + step):
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


def select(input_dir, output_dir, items_path, games_path, year, step):
    games = load_games(games_path, year, step)
    logging.warning('%d games loaded', len(games))
    items = load_items(items_path, games)
    logging.warning('%d items loaded', len(items))
    if step is None:
        output_dir = os.path.join(output_dir, str(year) + '_after1')
    elif step == 1:
        output_dir = os.path.join(output_dir, str(year))
    else:
        output_dir = os.path.join(output_dir, str(year) + '-' + str(year+step-1))
    os.makedirs(output_dir, exist_ok=True)
    cnt = 0
    for path in tqdm(items):
        # name = os.path.basename(path)
        src_path = os.path.join(input_dir, path)

        img = cv2.imread(src_path)
        if img.shape[0] >= 80 & img.shape[1] >= 80:
            cnt += 1
            dst_path = os.path.join(output_dir, '%05d.jpg' % cnt)
            shutil.copyfile(src_path, dst_path)


def main():
    args = parse_args()
    select(**vars(args))


if __name__ == '__main__':
    main()
