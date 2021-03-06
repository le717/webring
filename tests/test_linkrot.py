from tests import helpers


def test_single_link_single_fail(client):
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
    assert response_data["result"]["times_failed"] == 1
    assert response_data["result"]["is_dead"] == False
    assert response_data["result"]["is_web_archive"] == False


def test_single_link_is_dead(client):
    """Ensure a dead link is flagged as rotten status of 'yes'."""
    creation = client.post(
        helpers.authed_request("/", auth=helpers.VALID_AUTH),
        json=helpers.item_dead_url(),
    )

    item_id = helpers.from_json(creation.data)["id"]
    for _ in range(3):
        response = client.post(
            helpers.authed_request("/", "linkrot", item_id, auth=helpers.VALID_AUTH)
        )
    response_data = helpers.from_json(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response_data["id"] == item_id
    assert response_data["url"] == helpers.item_dead_url()["url"]
    assert response_data["result"]["times_failed"] == 0
    assert response_data["result"]["is_dead"] == True
    assert response_data["result"]["is_web_archive"] == False
