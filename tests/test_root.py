import uuid

from tests import helpers


def test_empty_ring(client) -> None:
    """There should be no items in the webring."""
    response = client.get("/")
    assert helpers.from_json(response.get_data(as_text=True)) == []


def test_create_good_item(client) -> None:
    """Successfully create an item."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_all_good(),
    )
    assert response.status_code == 201
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)


def test_create_item_dead_url(client) -> None:
    """Successfully create an item with a dead URL."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )
    assert response.status_code == 201
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)


def test_delete_item(client) -> None:
    """Successfully delete an item."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_all_good(),
    )
    response = client.delete(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
    )
    assert response.status_code == 204


def test_update_item_title(client) -> None:
    """Successfully update an item's title."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_all_good(),
    )
    response = client.patch(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
        json={"title": "My amazing website"},
    )
    assert response.status_code == 204


def test_update_item_dead_url(client) -> None:
    """Successfully update an item's dead URL."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )
    response = client.patch(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
        json={"url": "https://example.com"},
    )
    assert response.status_code == 204
