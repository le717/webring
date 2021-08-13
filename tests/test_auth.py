from tests import helpers


def test_no_auth_key(client):
    """The request should fail from a missing auth key."""
    response = client.post("/", data=helpers.valid_item())
    assert response.status_code == 422
    assert "auth_key" in helpers.to_json(response.data)["errors"]["query"]


def test_unknown_auth_key(client):
    """The request should fail from an unknown auth key."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.INVALID_AUTH),
        data=helpers.valid_item(),
    )
    assert response.status_code == 422
    assert "auth_key" in helpers.to_json(response.data)["errors"]["query"]
