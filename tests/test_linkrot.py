from httpx import codes

from tests import helpers


def test_single_link_single_fail(client) -> None:
    """Ensure a dead link is flagged is not web archived or dead but failed the rot check once."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_all_good(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    client.patch(
        helpers.authed_request(
            "/",
            item_id,
            auth=helpers.VALID_AUTH,
        ),
        json={"url": helpers.item_dead_url()["url"]},
    )
    response = client.post(helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH))
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.item_dead_url()["url"]
    assert response_data["result"]["times_failed"] == 1
    assert response_data["result"]["is_dead"] is False
    assert response_data["result"]["is_web_archive"] is False


def test_single_link_is_dead(client) -> None:
    """Ensure a dead link is flagged as dead."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    for _ in range(3):
        response = client.post(
            helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH),
        )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == codes.OK
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.item_dead_url()["url"]
    assert response_data["result"]["times_failed"] == 0
    assert response_data["result"]["is_dead"] is True
    assert response_data["result"]["is_web_archive"] is False


def test_single_link_is_web_archive(client) -> None:
    """Ensure a dead link is flagged as a web archive link."""
    # TODO: Fill in this test
    assert True is True
