# Python Training

2023年の研究開発部技術研修で使用した資料です。

## ディレクトリ構成

```bash
.
├── README.md
├── api
│   ├── Dockerfile
│   ├── app
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
├── app
│   ├── Dockerfile
│   ├── main.py
│   ├── poetry.lock
│   └── pyproject.toml
├── batch
│   ├── Dockerfile
│   ├── conf
│   ├── main.py
│   ├── pipeline
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
└── compose.yml
```

- api: API(FastAPI)
- app: Webアプリ(Streamlit)
- batch: データパイプライン(Gokart)
