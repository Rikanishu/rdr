"""fulltext_articles

Revision ID: 1e99e6ab5664
Revises: 33f392a12d7b
Create Date: 2014-10-04 16:52:28.932751

"""

# revision identifiers, used by Alembic.
revision = '1e99e6ab5664'
down_revision = '33f392a12d7b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('article', sa.Column('preview_image_src', sa.String(length=4096), nullable=True))
    op.drop_column('article', 'preview_image_id')
    op.add_column('article_full_text', sa.Column('image_src', sa.String(length=4096), nullable=True))


def downgrade():
    op.drop_column('article_full_text', 'image_src')
    op.add_column('article', sa.Column('preview_image_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('article', 'preview_image_src')
