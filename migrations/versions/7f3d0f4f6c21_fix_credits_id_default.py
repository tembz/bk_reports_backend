"""fix credits.id server default

Revision ID: 7f3d0f4f6c21
Revises: d21692a8c54a
Create Date: 2026-04-28 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '7f3d0f4f6c21'
down_revision: Union[str, Sequence[str], None] = 'd21692a8c54a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SEQUENCE IF NOT EXISTS credits_id_seq")
    op.execute(
        """
        SELECT setval(
            'credits_id_seq',
            COALESCE((SELECT MAX(id) FROM credits), 0) + 1,
            false
        )
        """
    )
    op.execute(
        """
        ALTER TABLE credits
        ALTER COLUMN id SET DEFAULT nextval('credits_id_seq'::regclass)
        """
    )
    op.execute("ALTER SEQUENCE credits_id_seq OWNED BY credits.id")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE credits ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS credits_id_seq")
