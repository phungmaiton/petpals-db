"""add title to meetup

Revision ID: e36c4cf91155
Revises: 9a43735db631
Create Date: 2023-07-18 18:33:30.556092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e36c4cf91155'
down_revision = '9a43735db631'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meetups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meetups', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
