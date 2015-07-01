"""category

Revision ID: 2b52dc39ea87
Revises: 6fbefc61214
Create Date: 2015-01-14 23:39:18.224242

"""

# revision identifiers, used by Alembic.
revision = '2b52dc39ea87'
down_revision = '6fbefc61214'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('feed', sa.Column('category', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('feed', 'category')
