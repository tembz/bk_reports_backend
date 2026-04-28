"""sync credits schema with uuid primary key

Revision ID: d21692a8c54a
Revises: 500ab9337502
Create Date: 2026-04-23 18:27:05.128387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd21692a8c54a'
down_revision: Union[str, Sequence[str], None] = '500ab9337502'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
