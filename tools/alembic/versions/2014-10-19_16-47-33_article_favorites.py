"""article_favorites

Revision ID: 484e27f8f07e
Revises: 1e99e6ab5664
Create Date: 2014-10-19 16:47:33.270706

"""

# revision identifiers, used by Alembic.
revision = '484e27f8f07e'
down_revision = '1e99e6ab5664'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('article_favorite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('article_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['article.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('article_favorite')
