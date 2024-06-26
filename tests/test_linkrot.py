from httpx import codes

from tests import helpers


def test_single_link_single_fail(client) -> None:
    """Ensure a dead link is flagged is not web archived or dead but failed the rot check once."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_all_good(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    client.patch(
        helpers.authed_request(
            "/",
            item_id,
            auth=helpers.VALID_AUTH,
        ),
        json={"url": helpers.entry_dead_url()["url"]},
    )
    response = client.post(helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH))
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.entry_dead_url()["url"]
    assert response_data["result"]["times_failed"] == 1
    assert response_data["result"]["is_dead"] is False
    assert response_data["result"]["is_web_archive"] is False


def test_single_link_is_dead(client) -> None:
    """Ensure a dead link is flagged as dead."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_dead_url(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    for _ in range(4):
        response = client.post(
            helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH),
        )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.entry_dead_url()["url"]
    assert response_data["result"]["times_failed"] == 4  # noqa: PLR2004
    assert response_data["result"]["is_dead"] is True
    assert response_data["result"]["is_web_archive"] is False


def test_single_link_is_web_archive(client) -> None:
    """Ensure a dead link is flagged as a web archive link."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_web_archive_url(),
    )
    item_id = helpers.from_json(creation.data)["id"]
    for _ in range(4):
        response = client.post(
            helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH),
        )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert response_data["id"] == item_id
    assert helpers.entry_web_archive_url()["url"] in response_data["url"]
    assert response_data["result"]["times_failed"] == 4  # noqa: PLR2004
    assert response_data["result"]["is_dead"] is False
    assert response_data["result"]["is_web_archive"] is True


def test_get_linkrot_history(client) -> None:
    """Get the linkrot history for an entry."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.entry_dead_url(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    client.post(helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH))
    response = client.get(
        helpers.authed_request("/", "linkrot", item_id, "history", auth=helpers.VALID_AUTH)
    )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert len(response_data) == 1
    assert response_data[0]["message"] == "Entry has failed the linkrot check 1 time."
    assert response_data[0]["was_alive"] is False
    assert response_data[0]["url_checked"] == helpers.entry_dead_url()["url"]
