import json


def test_empty_ring(client):
    """There should be no items in the webring."""
    response = client.get("/")
    assert json.loads(response.data) == []
