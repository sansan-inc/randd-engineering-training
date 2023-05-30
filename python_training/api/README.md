# api

## 準備

```bash
cp .env.example .env
vim .env
```

## ローカル

```bash
poetry update
poetry install
poetry run uvicorn app.main:app --reload
```

## docker 上での開発

```bash
docker build --target development -t api .
docker run -it -p 8000:8000 -v $(pwd)/:/app/ api
```

## テスト

```bash
poetry run pytest
```

## リンター、フォーマッター実行

```bash
poetry run isort .
poetry run black .
poetry run mypy .
poetry run flake8 .
```
