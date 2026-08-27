import pytest
from fastapi import HTTPException

from app.api.deps import grant_access
from app.core.auth import AccessRoute, UserRole, ACCESS_POLICY

class FakeUser:
    def __init__(self, role: UserRole):
        self.role = role


def test_grant_access_allows_authorized_role(monkeypatch):
    route = AccessRoute.USERS_LIST

    monkeypatch.setitem(
        ACCESS_POLICY,
        route,
        {UserRole.ADMIN, UserRole.MEMBER},
    )

    current_user = FakeUser(UserRole.MEMBER)

    dependency = grant_access(route)

    assert dependency(current_user) is None


def test_grant_access_denies_unauthorized_role(monkeypatch):
    route = AccessRoute.USERS_LIST

    monkeypatch.setitem(
        ACCESS_POLICY,
        route,
        {UserRole.ADMIN},
    )

    current_user = FakeUser(UserRole.MEMBER)

    dependency = grant_access(route)

    with pytest.raises(HTTPException) as exc_info:
        dependency(current_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Access denied"


def test_grant_access_raises_if_route_not_configured(monkeypatch):
    route = AccessRoute.USERS_LIST

    monkeypatch.delitem(
        ACCESS_POLICY,
        route,
        raising=False,
    )

    current_user = FakeUser(UserRole.ADMIN)

    dependency = grant_access(route)

    with pytest.raises(RuntimeError) as exc_info:
        dependency(current_user)

    assert str(exc_info.value) == (
        f"Access policy is not configured for route: {route}"
    )


def test_grant_access_allows_admin(monkeypatch):
    route = AccessRoute.USERS_LIST

    monkeypatch.setitem(
        ACCESS_POLICY,
        route,
        {UserRole.ADMIN},
    )

    current_user = FakeUser(UserRole.ADMIN)

    dependency = grant_access(route)

    assert dependency(current_user) is None