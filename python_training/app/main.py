import os

import requests
import streamlit as st
from streamlit_agraph import Config, Edge, Node, agraph

BACKEND_HOST = os.environ.get("BACKEND_HOST", "http://api:8000")


def get_persons() -> list[str]:
    response = requests.get(f"{BACKEND_HOST}/persons/?limit=10000")
    return response.json()["names"]


def search_person(person: str) -> list[str]:
    response = requests.get(f"{BACKEND_HOST}/persons/{person}")
    return response.json()["names"]


# タイトル
st.title("類似人物検索")

# 検索対象のユーザー群
persons = get_persons()

# サイドバー
selected_person_name = st.sidebar.selectbox("1人選んでください", set(persons))

# 検索ボタン
search_button = st.sidebar.button("検索")

# 検索ボタンが押された場合
if search_button and selected_person_name:
    similar_persons: list[str] = search_person(selected_person_name)

    nodes = []
    edges = []

    nodes.append(Node(id=selected_person_name))
    for person_name in similar_persons:
        nodes.append(Node(id=person_name, label=person_name))
        edges.append(Edge(source=selected_person_name, target=person_name))

    # 描画の設定
    config = Config(
        directed=False,
        physics=True,
    )

    # 描画
    agraph(nodes, edges, config)
