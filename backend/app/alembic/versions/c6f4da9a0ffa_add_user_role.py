"""add user role

Revision ID: c6f4da9a0ffa
Revises: fe56fa70289e
Create Date: 2026-08-27 13:19:23.445920

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c6f4da9a0ffa'
down_revision = 'fe56fa70289e'
branch_labels = None
depends_on = None


def upgrade():
    user_role_enum = postgresql.ENUM(
        "ADMIN",
        "MANAGER",
        "MEMBER",
        name="userrole",
        create_type=False,
    )

    # Explicitly create PostgreSQL enum type first
    user_role_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    # 1. Add role as nullable because existing users don't have a value yet.
    op.add_column(
        "user",
        sa.Column(
            "role",
            user_role_enum,
            nullable=True,
        ),
    )

    # 2. Existing regular users -> MEMBER.
    #    Existing superusers -> ADMIN.
    op.execute(
        """
        UPDATE "user"
        SET role = CASE
            WHEN is_superuser = TRUE THEN 'ADMIN'::userrole
            ELSE 'MEMBER'::userrole
        END
        """
    )

    # 3. All existing rows now have a role, so enforce NOT NULL.
    op.alter_column(
        "user",
        "role",
        nullable=False,
    )


def downgrade():
    op.drop_column("user", "role")

    # PostgreSQL enum types are independent schema objects,
    # so explicitly remove it during downgrade.
    sa.Enum(
        "ADMIN",
        "MANAGER",
        "MEMBER",
        name="userrole",
    ).drop(op.get_bind())
