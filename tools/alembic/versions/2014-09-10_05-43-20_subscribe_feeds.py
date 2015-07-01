"""subscribe_feeds

Revision ID: 33f392a12d7b
Revises: 16caaa4cf753
Create Date: 2014-09-10 05:43:20.608877

"""

# revision identifiers, used by Alembic.
revision = '33f392a12d7b'
down_revision = '16caaa4cf753'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('article_full_text',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('article_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['article.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('article', 'full_text')


def downgrade():
    op.add_column('article', sa.Column('full_text', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_table('article_full_text')
