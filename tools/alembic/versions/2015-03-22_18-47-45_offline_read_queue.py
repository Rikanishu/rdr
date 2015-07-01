"""offline-read-queue

Revision ID: 400b8d3359e8
Revises: 1e49069a638
Create Date: 2015-03-22 18:47:45.175436

"""

# revision identifiers, used by Alembic.
revision = '400b8d3359e8'
down_revision = '1e49069a638'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('offline_read_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('add_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_offline_read_queue_add_date'), 'offline_read_queue', ['add_date'], unique=False)
    op.create_foreign_key(None, 'subscribe', 'feed', ['feed_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'subscribe', type_='foreignkey')
    op.drop_index(op.f('ix_offline_read_queue_add_date'), table_name='offline_read_queue')
    op.drop_table('offline_read_queue')
