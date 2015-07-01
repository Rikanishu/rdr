"""remove_last_visit_news_table

Revision ID: 222b70623b97
Revises: 4628e2d2797d
Create Date: 2015-01-04 06:17:54.480911

"""

# revision identifiers, used by Alembic.
revision = '222b70623b97'
down_revision = '4628e2d2797d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_table('last_visit_news')


def downgrade():
    op.create_table('last_visit_news',
        sa.Column('id', sa.INTEGER(), server_default="nextval('last_visit_news_id_seq'::regclass)", nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('binary_data', postgresql.BYTEA(), autoincrement=False, nullable=True),
        sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], [u'user.id'], name=u'last_visit_news_user_id_fkey', ondelete=u'CASCADE'),
        sa.PrimaryKeyConstraint('id', name=u'last_visit_news_pkey')
    )
