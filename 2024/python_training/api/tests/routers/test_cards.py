from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient


class TestCardsAPI:
    endpoint: str = "/api/cards/"
    df_cards: pd.DataFrame
    dummy_user: dict

    @classmethod
    def setup_class(cls) -> None:
        data_path = Path(__file__).parents[2] / "data" / "dummy_business_cards.csv"
        cls.df_cards = pd.read_csv(data_path, dtype=str)
        cls.dummy_user = cls.df_cards.iloc[0].to_dict()

    def test_list_business_cards(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint)
        results = response.json()
        assert response.status_code == 200
        assert len(results) == len(self.df_cards)
        assert list(results[0].keys()) == self.df_cards.columns.tolist()
        assert results[0] == self.dummy_user

    def test_list_business_cards_offset_limit(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?offset=1&limit=5")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 5
        assert results[0] == self.df_cards.iloc[1].to_dict()

    def test_list_business_cards_invalid_limit_str(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?limit=a")
        results = response.json()
        assert response.status_code == 422
        assert results["detail"][0]["type"] == "int_parsing"

    def test_list_business_cards_invalid_limit_range(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?limit=0")
        results = response.json()
        assert response.status_code == 422
        assert results["detail"][0]["type"] == "greater_than_equal"

    def test_count_business_cards(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "count")
        assert response.status_code == 200
        assert response.json() == len(self.df_cards)

    def test_get_business_card(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + self.dummy_user["user_id"])
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 1
        assert list(results[0].keys()) == self.df_cards.columns.tolist()
        assert results[0] == self.dummy_user

    def test_get_business_card_not_found(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "0000000000")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 0

    def test_search_similar_person(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + self.dummy_user["user_id"] + "/similar_top10_users")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 3
        assert list(results[0].keys()) == [
            "user_id",
            "company_id",
            "full_name",
            "position",
            "company_name",
            "address",
            "phone_number",
            "similarity",
        ]

    def test_search_similar_person_not_found(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "0000000000/similar_top10_users")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 0
