# GirlsManifold
An attempt to replicate make.girls.moe using PyTorch


## Install

Install opencv, scrapy, tqdm packages in Python 3.

## Run

1. Put `erogamescape_sql_output.zip` into `data/`.
2. Put `data/lbpcascade_animeface.xml` into `data/`.
3. Run the following:

```bash
./scripts/preprocess_sql.sh
./scripts/crawl_faces.sh
./scripts/process_faces.sh
```
