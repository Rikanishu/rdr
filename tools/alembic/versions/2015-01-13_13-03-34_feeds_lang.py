"""feeds_lang

Revision ID: 59bbff80daef
Revises: 222b70623b97
Create Date: 2015-01-13 13:03:34.447648

"""

# revision identifiers, used by Alembic.
revision = '59bbff80daef'
down_revision = '222b70623b97'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('feed', sa.Column('language', sa.String(length=12), nullable=True))


def downgrade():
    op.drop_column('feed', 'language')
