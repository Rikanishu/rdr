"""article_hash

Revision ID: 595208859f20
Revises: 43476478ebf9
Create Date: 2015-05-17 14:42:42.698534

"""

# revision identifiers, used by Alembic.
revision = '595208859f20'
down_revision = '43476478ebf9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('article', sa.Column('hash', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_article_hash'), 'article', ['hash'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_article_hash'), table_name='article')
    op.drop_column('article', 'hash')
