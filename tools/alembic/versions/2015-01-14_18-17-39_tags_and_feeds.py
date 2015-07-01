"""tags_and_feeds

Revision ID: 6fbefc61214
Revises: 59bbff80daef
Create Date: 2015-01-14 18:17:39.040900

"""

# revision identifiers, used by Alembic.
revision = '6fbefc61214'
down_revision = '59bbff80daef'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('article_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('tag', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'feed', sa.Column('last_etag_header', sa.String(length=255), nullable=True))
    op.add_column(u'feed', sa.Column('last_modified_header', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column(u'feed', 'last_modified_header')
    op.drop_column(u'feed', 'last_etag_header')
    op.drop_table('article_tag')
