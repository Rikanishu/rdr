"""file-format-offline

Revision ID: 43476478ebf9
Revises: 31c5ba5b356c
Create Date: 2015-03-27 00:52:00.655172

"""

# revision identifiers, used by Alembic.
revision = '43476478ebf9'
down_revision = '31c5ba5b356c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('offline_read_queue_task', sa.Column('file_format', sa.String(length=24), nullable=True))
    op.drop_column('offline_read_queue_task', 'format')


def downgrade():
    op.add_column('offline_read_queue_task', sa.Column('format', sa.VARCHAR(length=24), autoincrement=False, nullable=True))
    op.drop_column('offline_read_queue_task', 'file_format')
