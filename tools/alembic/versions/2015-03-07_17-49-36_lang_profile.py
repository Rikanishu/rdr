"""lang_profile

Revision ID: 1e49069a638
Revises: 30d3410b1a3b
Create Date: 2015-03-07 17:49:36.715787

"""

# revision identifiers, used by Alembic.
revision = '1e49069a638'
down_revision = '30d3410b1a3b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('profile', sa.Column('lang', sa.String(length=12), nullable=True))


def downgrade():
    op.drop_column('profile', 'lang')
