# batch

## Prepare

```bash
cp .env.example .env
vim .env
```

## Run

```bash
poetry install
poetry run python main.py pipeline.Main --local-scheduler
```

## Test

```bash
poetry run pytest
```

## Docker Run

```bash
poetry lock
docker build --target development -t batch .
docker run -it --rm -v $(pwd):/app --env-file .env batch
```
