import argparse
import logging
import os

import cv2

from tqdm import tqdm

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--min-size', type=int, default=80)
    parser.add_argument('--scale', type=float, default=1.5)
    parser.add_argument(
        '--cascade-file', default='data/lbpcascade_animeface.xml')
    return parser.parse_args()


def detect(input_dir, output_dir, min_size, scale, cascade_file):
    cascade = cv2.CascadeClassifier(cascade_file)

    os.makedirs(output_dir, exist_ok=True)
    t = tqdm(os.listdir(input_dir))
    total = 0
    for name in t:
        filename = os.path.join(input_dir, name)

        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray)
        img_h = image.shape[0]
        img_w = image.shape[1]

        images = []
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
                images.append(image[y:yy, x:xx, :])

        for i, image in enumerate(images):
            prefix, suffix = name.split('.')
            outname = os.path.join(output_dir, '{}-{}.{}'.format(
                prefix, i, suffix))
            cv2.imwrite(outname, image)
            total += 1
        t.set_postfix(total=total)


def main():
    args = parse_args()
    detect(**vars(args))


if __name__ == '__main__':
    main()
