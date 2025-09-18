"""add_property_type_simple

Revision ID: simple_property_type
Revises: c15e11273830
Create Date: 2025-09-18 02:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'simple_property_type'
down_revision: str = 'c15e11273830'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""
    # Faqat property_type maydonini qo'shish
    op.add_column('listings', sa.Column('property_type', sa.Enum('kvartira', 'uy', 'ofis', name='propertytype'), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('listings', 'property_type')
