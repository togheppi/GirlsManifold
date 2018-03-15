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
    parser.add_argument('--output-dir', default='../../data/faces')
    parser.add_argument('--items-path', default='../../data/chu.jl')
    parser.add_argument('--games-path', default='../../data/results.tsv')
    parser.add_argument('--year', type=int, default=2005)
    parser.add_argument('--step', type=int, default=1)
    parser.add_argument('--min-size', type=int, default=80)
    parser.add_argument('--scale', type=float, default=1.5)
    parser.add_argument('--resize_scale', type=int, default=256)
    parser.add_argument('--cascade-file', default='../../data/lbpcascade_animeface.xml')
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


def select_and_detect(input_dir, output_dir, items_path, games_path, year, step, min_size, scale, resize_scale, cascade_file):
    games = load_games(games_path, year, step)
    logging.warning('%d games loaded', len(games))
    items = load_items(items_path, games)
    logging.warning('%d items loaded', len(items))
    if step is None:
        output_dir = os.path.join(output_dir, str(year) + '_after')
    elif step == 1:
        output_dir = os.path.join(output_dir, str(year))
    else:
        output_dir = os.path.join(output_dir, str(year) + '-' + str(year+step-1))
    os.makedirs(output_dir, exist_ok=True)
    cnt = 0
    for path in tqdm(items):
        # name = os.path.basename(path)
        src_path = os.path.join(input_dir, path)

        cascade = cv2.CascadeClassifier(cascade_file)

        image = cv2.imread(src_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray)
        img_h = image.shape[0]
        img_w = image.shape[1]

        for (x, y, w, h) in faces:
            scale_factor = min((scale - 1.) / 2, x / w, y / h,
                               (img_w - x - w) / w, (img_h - y - h) / h)
            sw = int(w * scale_factor)
            sh = int(h * scale_factor)

            xx = x + w + sw
            yy = y + h + sh
            x = x - sw
            y = y - sh
            assert (x >= 0 and y >= 0 and xx <= img_w and
                    yy <= img_h), (w, h, image.shape, x, y, xx, yy)

            if xx - x >= min_size and yy - y >= min_size:
                cnt += 1
                face = image[y:yy, x:xx, :]
                img = cv2.resize(face, dsize=(resize_scale, resize_scale))
                outname = os.path.join(output_dir, '%05d.jpg' % cnt)
                cv2.imwrite(outname, img)


def main():
    args = parse_args()
    select_and_detect(**vars(args))


if __name__ == '__main__':
    main()
