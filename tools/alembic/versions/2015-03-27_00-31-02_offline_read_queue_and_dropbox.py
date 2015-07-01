"""offline-read-queue-and-dropbox

Revision ID: 31c5ba5b356c
Revises: 400b8d3359e8
Create Date: 2015-03-27 00:31:02.030069

"""

# revision identifiers, used by Alembic.
revision = '31c5ba5b356c'
down_revision = '400b8d3359e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('offline_read_queue_task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('out_file', sa.String(length=512), nullable=True),
    sa.Column('format', sa.String(length=24), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'profile', sa.Column('dropbox_access_token', sa.String(length=512), nullable=True))


def downgrade():
    op.drop_column(u'profile', 'dropbox_access_token')
    op.drop_table('offline_read_queue_task')
