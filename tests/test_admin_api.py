"""The /api/users endpoints expose customer IDs on a public service, so every route needs the token."""
import pytest
from fastapi.testclient import TestClient

import main
from vibpath_bot.config.env_config import settings

USER_ROUTES = [
    ("GET", "/api/users"),
    ("GET", "/api/users/U123/preferences"),
    ("PUT", "/api/users/U123/preferences"),
    ("DELETE", "/api/users/U123/preferences"),
]
client = TestClient(main.app, raise_server_exceptions=False)


@pytest.mark.parametrize("method, path", USER_ROUTES)
@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "Bearer wrong"},
        {"Authorization": "Bearer "},
        {"X-Api-Key": "test-admin-token"},
    ],
    ids=["none", "wrong", "empty", "other-header"],
)
def test_rejected_without_the_token(method, path, headers):
    assert client.request(method, path, headers=headers).status_code == 401


@pytest.mark.parametrize("method, path", USER_ROUTES)
def test_allowed_with_the_token(method, path):
    response = client.request(
        method, path, headers={"Authorization": f"Bearer {settings.admin_api_token}"}, json={"aiReplyEnabled": True}
    )
    assert response.status_code != 401


def test_unset_token_rejects_everyone(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_token", None)
    assert client.get("/api/users", headers={"Authorization": "Bearer "}).status_code == 401
    assert client.get("/api/users", headers={"Authorization": "Bearer None"}).status_code == 401


def test_public_routes_stay_open():
    assert client.get("/health").status_code == 200
