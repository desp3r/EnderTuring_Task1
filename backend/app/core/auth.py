from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"

class AccessRoute(StrEnum):
    USERS_LIST = "users:list"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"

    USERS_ME_UPDATE = "users:me:update"
    USERS_ME_UPDATE_PASSWORD = "users:me:update:password"
    USERS_ME_READ = "users:me:read"
    USERS_ME_DELETE = "users:me:delete"

ACCESS_POLICY: dict[AccessRoute, set[UserRole]] = {
    AccessRoute.USERS_LIST: {
        UserRole.ADMIN,
        UserRole.MANAGER,
    },
    AccessRoute.USERS_CREATE: {
        UserRole.ADMIN,
        UserRole.MANAGER,
    },
    AccessRoute.USERS_UPDATE: {
        UserRole.ADMIN,
        UserRole.MANAGER,
    },
    AccessRoute.USERS_ME_UPDATE: {
        UserRole.ADMIN,
        UserRole.MANAGER,
        UserRole.MEMBER,
    },
    AccessRoute.USERS_ME_UPDATE_PASSWORD: {
        UserRole.ADMIN,
        UserRole.MANAGER,
        UserRole.MEMBER,
    },
    AccessRoute.USERS_ME_READ: {
        UserRole.ADMIN,
        UserRole.MANAGER,
        UserRole.MEMBER,
    },
    AccessRoute.USERS_ME_DELETE: {
        UserRole.ADMIN,
        UserRole.MANAGER,
        UserRole.MEMBER,
    },
}