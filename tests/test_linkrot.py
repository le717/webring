from tests import helpers


def test_single_link_rot_maybe(client):
    """Ensure a dead link is flagged as rotten status of 'maybe'."""
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
    response = client.post(
        helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH)
    )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.item_dead_url()["url"]
    assert response_data["result"] == "maybe"


def test_single_link_rot_yes(client):
    """Ensure a dead link is flagged as rotten status of 'yes'."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    for _ in range(2):
        response = client.post(
            helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH)
        )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.item_dead_url()["url"]
    assert response_data["result"] == "yes"
