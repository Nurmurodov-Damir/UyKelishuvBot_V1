"""add property_type column

Revision ID: add_property_type_simple
Revises: c15e11273830
Create Date: 2025-09-18 03:52:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_property_type_simple'
down_revision: Union[str, Sequence[str], None] = 'c15e11273830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add property_type column to listings table."""
    # Add property_type column
    op.add_column('listings', sa.Column('property_type', sa.Enum('kvartira', 'uy', 'ofis', name='propertytype'), nullable=True))


def downgrade() -> None:
    """Remove property_type column from listings table."""
    op.drop_column('listings', 'property_type')
