from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient


class TestContactsAPI:
    endpoint: str = "/api/contacts/"
    df_contacts: pd.DataFrame

    @classmethod
    def setup_class(cls) -> None:
        data_path = Path(__file__).parents[2] / "data" / "dummy_business_cards_exchange_history.csv"
        cls.df_contacts = pd.read_csv(data_path, dtype=str)

    def test_list_contact_history(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint)
        results = response.json()
        assert response.status_code == 200
        assert len(results) == len(self.df_contacts)
        assert list(results[0].keys()) == self.df_contacts.columns.tolist()
        assert results[0] == self.df_contacts.iloc[0].to_dict()

    def test_list_contact_history_offset_limit(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?offset=1&limit=3")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 3
        assert results[0] == self.df_contacts.iloc[1].to_dict()

    def test_list_contact_history_start_date(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?offset=0&limit=100&start_date=2023-01-01")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 3  # 2023-01-01 以降のデータは3件のみ

    def test_list_contact_history_end_date(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?end_date=2020-12-31&offset=0&limit=100")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 1  # 2020-12-31 以前のデータは1件のみ

    def test_list_contact_history_start_date_end_date(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?start_date=2020-05-15&end_date=2020-05-15&offset=0&limit=100")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 1  # 2020-05-15 のデータは1件のみ

    def test_list_contact_history_invalid_offset(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "?offset=-1")
        results = response.json()
        assert response.status_code == 422
        assert results["detail"][0]["type"] == "greater_than_equal"

    def test_count_contact_history(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "count")
        assert response.status_code == 200
        assert response.json() == len(self.df_contacts)

    def test_list_contact_history_by_owner_user(self, test_client: TestClient) -> None:
        test_owner_user_id = self.df_contacts.iloc[0]["owner_user_id"]
        response = test_client.get(self.endpoint + f"owner_users/{test_owner_user_id}")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 1
        assert list(results[0].keys()) == self.df_contacts.columns.tolist()

    def test_list_contact_history_by_owner_user_not_found(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "owner_users/00000000")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 0

    @pytest.mark.parametrize(("owner_user_id", "expected_count"), [("129138504", 1), ("00000000", 0)])
    def test_count_contact_history_by_owner_user(
        self, test_client: TestClient, owner_user_id: str, expected_count: int
    ) -> None:
        response = test_client.get(self.endpoint + f"owner_users/{owner_user_id}/count")
        assert response.status_code == 200
        assert response.json() == expected_count

    def test_list_contact_history_by_owner_company(self, test_client: TestClient) -> None:
        test_owner_company_id = self.df_contacts.iloc[0]["owner_company_id"]
        response = test_client.get(self.endpoint + f"owner_companies/{test_owner_company_id}")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 1
        assert list(results[0].keys()) == self.df_contacts.columns.tolist()

    def test_list_contact_history_by_owner_company_not_found(self, test_client: TestClient) -> None:
        response = test_client.get(self.endpoint + "owner_companies/00000000")
        results = response.json()
        assert response.status_code == 200
        assert len(results) == 0

    @pytest.mark.parametrize(("owner_company_id", "expected_count"), [("2685496293", 1), ("00000000", 0)])
    def test_count_contact_history_by_owner_company(
        self, test_client: TestClient, owner_company_id: str, expected_count: int
    ) -> None:
        response = test_client.get(self.endpoint + f"owner_companies/{owner_company_id}/count")
        assert response.status_code == 200
        assert response.json() == expected_count
