# app

## ローカル

```bash
poetry update
poetry install
poetry run streamlit run main.py
```

## docker 上での開発

```bash
docker build --target development -t app .
docker run -it -p 8080:8080 -v $(pwd)/:/app/ app
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
