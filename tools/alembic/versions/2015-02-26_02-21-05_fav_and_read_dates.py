"""fav_and_read_dates

Revision ID: 520afc544eff
Revises: 2b52dc39ea87
Create Date: 2015-02-26 02:21:05.750496

"""

# revision identifiers, used by Alembic.
revision = '520afc544eff'
down_revision = '2b52dc39ea87'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('article_favorite', sa.Column('fav_date', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_article_favorite_fav_date'), 'article_favorite', ['fav_date'], unique=False)
    op.add_column('article_status', sa.Column('read_date', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_article_status_read_date'), 'article_status', ['read_date'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_article_status_read_date'), table_name='article_status')
    op.drop_column('article_status', 'read_date')
    op.drop_index(op.f('ix_article_favorite_fav_date'), table_name='article_favorite')
    op.drop_column('article_favorite', 'fav_date')
