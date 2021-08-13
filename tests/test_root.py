import uuid

from tests import helpers


def test_empty_ring(client):
    """There should be no items in the webring."""
    response = client.get("/")
    assert helpers.from_json(response.data) == []


def test_create_item(client):
    """Successfully create an item."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        data=helpers.item_all_good(),
    )
    print(response.data)
    assert response is False
