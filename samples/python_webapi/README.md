# randd_samples

## ビルド

```sh
docker build -t randd_sample .
```

## テスト

```sh
docker run -it --rm -p8000:8000 randd_sample python setup.py test
```

## 学習

```sh
python -m src.randd_sample.model.trainer train --output src/randd_sample/model/pkl/sample.pkl
```

## 実行

```sh
docker run -it --rm -p8000:8000 randd_sample
```

```sh
$ curl -XGET localhost:8000/v1/sample
Sample.
curl -XPOST -H 'Content-Type:application/json' localhost:8000/v1/analyse -d '{"CRIM": 0.00632, "ZN": 18.0, "INDUS": 2.31, "CHAS": 0.0, "NOX": 0.538, "RM": 6.575, "AGE": 65.2, "DIS": 4.09, "RAD": 1.0, "TAX": 296.0, "PTRATIO": 15.3, "B": 396.9, "LSTAT": 4.98}'
{"MEDV":29.1634570300974}
```
