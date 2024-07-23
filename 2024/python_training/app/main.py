import os

import pandas as pd
import pandera as pa
import requests
import streamlit as st
from pandera.typing import DataFrame
from streamlit_agraph import Config, Edge, Node, agraph

from schemas import PersonSchema, SimilarPersonSchema

BACKEND_HOST = os.environ.get("BACKEND_HOST", "http://api:8000")


@pa.check_types
def get_persons_df() -> DataFrame[PersonSchema]:
    response = requests.get(f"{BACKEND_HOST}/v2/cards/?limit=100", timeout=10)
    return pd.DataFrame(response.json())


@pa.check_types
def search_similar_persons(user_id: str) -> DataFrame[SimilarPersonSchema]:
    response = requests.get(f"{BACKEND_HOST}/v2/cards/{user_id}/similar", timeout=10)
    return pd.DataFrame(response.json())


# タイトル
st.title("類似人物検索")

# 検索対象のユーザー群
persons_df: DataFrame[PersonSchema] = get_persons_df()

# 選択box
selected_user_name: str = str(st.selectbox("選択してください", set(persons_df["full_name"])))

# 検索ボタンが押された場合
selected_user_id: str = persons_df[persons_df["full_name"] == selected_user_name]["user_id"].values[0]
similar_persons: DataFrame[SimilarPersonSchema] = search_similar_persons(selected_user_id)

nodes = []
edges = []

st.write(f"{selected_user_name} の類似人物")

nodes.append(Node(id=selected_user_id, label=selected_user_name, shape="circle"))
for user_id, user_name, similarity in zip(
    similar_persons["user_id"], similar_persons["full_name"], similar_persons["similarity"], strict=False
):
    nodes.append(Node(id=user_id, label=user_name, shape="ellipse"))
    edges.append(Edge(source=selected_user_id, target=user_id, label=str(round(similarity, 3))))

# 描画の設定
config = Config(
    height=500,
    directed=False,
    physics=True,
)

# 描画
agraph(nodes, edges, config)
