"""empty message

Revision ID: 42996786066e
Revises: af8dd6a6b50b
Create Date: 2023-07-18 10:58:15.363841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42996786066e'
down_revision = 'af8dd6a6b50b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_meetups')
    with op.batch_alter_table('meetups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('longitude', sa.Float(), nullable=True))
        batch_op.drop_column('longtitude')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meetups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('longtitude', sa.FLOAT(), nullable=True))
        batch_op.drop_column('longitude')

    op.create_table('_alembic_tmp_meetups',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('pet_id', sa.INTEGER(), nullable=True),
    sa.Column('venue', sa.VARCHAR(), nullable=True),
    sa.Column('street_address', sa.VARCHAR(), nullable=True),
    sa.Column('city', sa.VARCHAR(), nullable=True),
    sa.Column('state', sa.VARCHAR(), nullable=True),
    sa.Column('country', sa.VARCHAR(), nullable=True),
    sa.Column('latitude', sa.FLOAT(), nullable=True),
    sa.Column('longitude', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name='fk_meetups_pet_id_pets'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###