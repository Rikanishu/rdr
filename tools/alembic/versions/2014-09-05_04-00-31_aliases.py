"""aliases

Revision ID: 16caaa4cf753
Revises: 291e3532fd99
Create Date: 2014-09-05 04:00:31.730142

"""

# revision identifiers, used by Alembic.
revision = '16caaa4cf753'
down_revision = '291e3532fd99'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('feed_alias_url',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.String(length=4096), nullable=True),
        sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_alias_url_url'), 'feed_alias_url', ['url'], unique=False)
    op.create_table('feed_alias_keyword',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=True),
        sa.Column('keyword', sa.String(length=4096), nullable=True),
        sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_alias_keyword_keyword'), 'feed_alias_keyword', ['keyword'], unique=False)
    op.drop_table('feed_alias')


def downgrade():
    op.create_table('feed_alias',
        sa.Column('id', sa.INTEGER(), server_default="nextval('feed_alias_id_seq'::regclass)", nullable=False),
        sa.Column('feed_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('alias', sa.VARCHAR(length=4096), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='feed_alias_pkey')
    )
    op.drop_index(op.f('ix_feed_alias_keyword_keyword'), table_name='feed_alias_keyword')
    op.drop_table('feed_alias_keyword')
    op.drop_index(op.f('ix_feed_alias_url_url'), table_name='feed_alias_url')
    op.drop_table('feed_alias_url')
