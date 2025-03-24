"""Update status length

Revision ID: d961aca62eb3
Revises: 3781a5eb12cb
Create Date: 2025-03-23 16:10:05.683965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d961aca62eb3"
down_revision = "3781a5eb12cb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the existing enum type constraint
    op.execute("ALTER TABLE connector_credential_pair ALTER COLUMN status TYPE varchar")

    # Create new enum type with all values
    op.execute(
        "ALTER TABLE connector_credential_pair ALTER COLUMN status TYPE VARCHAR(20) USING status::varchar(20)"
    )

    # Update the enum type to include all possible values
    op.alter_column(
        "connector_credential_pair",
        "status",
        type_=sa.Enum(
            "SCHEDULED",
            "INITIAL_INDEXING",
            "ACTIVE",
            "PAUSED",
            "DELETING",
            "INVALID",
            "REPEATED_ERROR",
            name="connectorcredentialpairstatus",
            native_enum=False,
        ),
        existing_type=sa.String(20),
        nullable=False,
    )


def downgrade() -> None:
    # no need to convert back
    pass
