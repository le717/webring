from httpx import codes

from tests import helpers


def test_no_auth_key(client) -> None:
    """The request should fail from a missing auth key."""
    response = client.post(path="/", data=helpers.entry_all_good())
    assert response.status_code == codes.BAD_REQUEST


def test_unknown_auth_key(client) -> None:
    """The request should fail from an unknown auth key."""
    response = client.post(
        path="/",
        headers=helpers.make_auth(helpers.INVALID_AUTH),
        data=helpers.entry_all_good(),
    )
    assert response.status_code == codes.FORBIDDEN
