"""last_visit_news

Revision ID: 4628e2d2797d
Revises: 4c0ecc79a7c9
Create Date: 2014-12-31 05:11:33.868195

"""

# revision identifiers, used by Alembic.
revision = '4628e2d2797d'
down_revision = '4c0ecc79a7c9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('last_visit_news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('binary_data', sa.LargeBinary(length=4096), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last_visit_news_date'), 'last_visit_news', ['date'], unique=False)
    op.create_table('action',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('type', sa.String(length=64), nullable=True),
        sa.Column('binary_data', sa.LargeBinary(length=8192), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_action_date'), 'action', ['date'], unique=False)
    op.add_column(u'article', sa.Column('fetched', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_article_fetched'), 'article', ['fetched'], unique=False)
    op.add_column(u'user', sa.Column('last_visit', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_last_visit'), 'user', ['last_visit'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_last_visit'), table_name='user')
    op.drop_column(u'user', 'last_visit')
    op.drop_index(op.f('ix_article_fetched'), table_name='article')
    op.drop_column(u'article', 'fetched')
    op.drop_index(op.f('ix_action_date'), table_name='action')
    op.drop_table('action')
    op.drop_index(op.f('ix_last_visit_news_date'), table_name='last_visit_news')
    op.drop_table('last_visit_news')
