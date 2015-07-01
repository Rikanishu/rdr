"""user_image_id

Revision ID: 4c0ecc79a7c9
Revises: 484e27f8f07e
Create Date: 2014-11-23 14:55:00.937127

"""

# revision identifiers, used by Alembic.
revision = '4c0ecc79a7c9'
down_revision = '484e27f8f07e'

from alembic import op, context
import sqlalchemy as sa


def upgrade():
    op.create_table('profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('image_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    opts = context.get_context().opts
    signals = opts.get('signals')
    if signals:
        def apply_data(sender):
            print "Apply data"
            from rdr.application.database import db
            from rdr.modules.users.models import User, Profile
            users = User.query.all()
            for user in users:
                if not user.profile:
                    prof = Profile(user_id=user.id)
                    db.session.add(prof)
            db.session.commit()

        signals('on_complete').connect(apply_data, weak=False)


def downgrade():
    op.drop_table('profile')
