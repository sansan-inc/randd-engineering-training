import click
import joblib
import numpy as np
from .regression import LinearRegression
from logzero import logger
from sklearn import datasets
from sklearn.metrics import mean_squared_error, r2_score


@click.group()
def cmd():
    pass


@cmd.command()
@click.option('--output', type=click.Path(exists=False, dir_okay=False), required=True)
def train(output):
    X, y = datasets.load_boston(return_X_y=True)

    X_train = X[:-20]
    X_test = X[-20:]

    y_train = y[:-20]
    y_test = y[-20:]

    regr = LinearRegression()

    regr.fit(X_train, y_train)

    y_pred = regr.predict(X_test)

    logger.info(f'Coefficients: {regr.coef_}')
    logger.info(f'Mean squared error: {mean_squared_error(y_test, y_pred):.2f}')
    logger.info(f'Coefficient of determination: {r2_score(y_test, y_pred):.2f}')

    joblib.dump(regr, output, compress=True)
    logger.info(f"{output}")


if __name__ == "__main__":
    cmd()
