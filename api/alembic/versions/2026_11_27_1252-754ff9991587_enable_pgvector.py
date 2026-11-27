"""enable pgvector

Revision ID: 754ff9991587
Revises:
Create Date: 2026-11-27 12:52:59.862891
"""

from collections.abc import Sequence

from alembic import op

revision: str = "754ff9991587"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # pgvector adds the `vector` column type and similarity search operators
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
