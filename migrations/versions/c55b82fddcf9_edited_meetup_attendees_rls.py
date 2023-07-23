"""edited meetup attendees rls

Revision ID: c55b82fddcf9
Revises: 640ea3e479d9
Create Date: 2023-07-21 10:50:31.168670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55b82fddcf9'
down_revision = '640ea3e479d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meetup_attendees', schema=None) as batch_op:
        batch_op.drop_constraint('meetup_attendees_meetup_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'meetups', ['meetup_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meetup_attendees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('meetup_attendees_meetup_id_fkey', 'meetups', ['meetup_id'], ['id'])

    # ### end Alembic commands ###