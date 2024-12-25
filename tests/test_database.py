import pytest
from src.database import MongoDBClient
from unittest.mock import Mock, patch

@pytest.fixture
def db_client():
    return MongoDBClient()

def test_insert_trend(db_client):
    test_data = {
        "_id": "test_id",
        "timestamp": "2024-01-01",
        "nameoftrend1": "Test Trend"
    }
    with patch('pymongo.collection.Collection.insert_one') as mock_insert:
        mock_insert.return_value.inserted_id = "test_id"
        result = db_client.insert_trend(test_data)
        assert result == "test_id"

def test_get_latest_trend(db_client):
    with patch('pymongo.collection.Collection.find_one') as mock_find:
        mock_find.return_value = {"_id": "test_id"}
        result = db_client.get_latest_trend()
        assert result["_id"] == "test_id"
