"""feeds

Revision ID: 291e3532fd99
Revises: 423542de4400
Create Date: 2014-08-19 01:10:45.105842

"""

# revision identifiers, used by Alembic.
revision = '291e3532fd99'
down_revision = '423542de4400'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('feed_alias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=True),
        sa.Column('alias', sa.String(length=4096), nullable=True),
        sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_alias_alias'), 'feed_alias', ['alias'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_feed_alias_alias'), table_name='feed_alias')
    op.drop_table('feed_alias')
