import uuid

from httpx import codes

from tests import helpers


def test_empty_ring(client) -> None:
    """There should be no items in the webring."""
    response = client.get("/")
    assert helpers.from_json(response.get_data(as_text=True)) == []


def test_create_good_entry(client) -> None:
    """Successfully create an item."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_all_good(),
    )
    assert response.status_code == codes.CREATED
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)


def test_create_entry_dead_url(client) -> None:
    """Successfully create an item with a dead URL."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_dead_url(),
    )
    assert response.status_code == codes.CREATED
    assert isinstance(uuid.UUID(helpers.from_json(response.data)["id"]), uuid.UUID)


def test_delete_entry(client) -> None:
    """Successfully delete an entry."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_all_good(),
    )
    response = client.delete(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
    )
    assert response.status_code == codes.NO_CONTENT


def test_delete_entry_with_linkrot_history(client) -> None:
    """Successfully delete an entry and its linkrot history."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_all_good(),
    )
    entry_id = helpers.from_json(creation.data)["id"]

    # Perform a linkrot check
    client.post(helpers.authed_request("/", "linkrot", entry_id, auth=helpers.VALID_AUTH))

    delete_response = client.delete(
        helpers.authed_request("/", entry_id, auth=helpers.VALID_AUTH),
    )
    assert delete_response.status_code == codes.NO_CONTENT

    # Make sure we don't get history for a deleted entry
    history_response = client.get(
        helpers.authed_request("/", "linkrot", entry_id, "history", auth=helpers.VALID_AUTH)
    )
    assert history_response.status_code == codes.NOT_FOUND


def test_update_entry_title(client) -> None:
    """Successfully update an entry's title."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_all_good(),
    )
    response = client.patch(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
        json={"title": "My amazing website"},
    )
    assert response.status_code == codes.NO_CONTENT


def test_update_entry_dead_url(client) -> None:
    """Successfully update an entry's dead URL."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_dead_url(),
    )
    response = client.patch(
        helpers.authed_request(
            "/",
            helpers.from_json(creation.data)["id"],
            auth=helpers.VALID_AUTH,
        ),
        json={"url": "https://example.com"},
    )
    assert response.status_code == codes.NO_CONTENT
