import uuid

from tests import helpers


def test_empty_ring(client):
    """There should be no items in the webring."""
    response = client.get("/")
    assert helpers.from_json(response.get_data(as_text=True)) == []


def test_create_good_item(client):
    """Successfully create an item."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_all_good(),
    )
    assert response.status_code == 201
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)


def test_create_dead_url_item(client):
    """Successfully create an item with a dead URL."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )
    assert response.status_code == 201
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)
