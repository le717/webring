from httpx import codes

from tests import helpers


def test_no_auth_key(client) -> None:
    """The request should fail from a missing auth key."""
    response = client.post("/", data=helpers.entry_all_good())
    assert response.status_code == codes.UNPROCESSABLE_ENTITY
    assert "auth_key" in helpers.from_json(response.data)["errors"]["query"]


def test_unknown_auth_key(client) -> None:
    """The request should fail from an unknown auth key."""
    response = client.post(
        helpers.authed_request("/", auth=helpers.INVALID_AUTH),
        data=helpers.entry_all_good(),
    )
    assert response.status_code == codes.UNPROCESSABLE_ENTITY
    assert "auth_key" in helpers.from_json(response.data)["errors"]["query"]
