"""empty message

Revision ID: abde1953a666
Revises: 8342dae658e2
Create Date: 2017-05-29 14:31:06.870493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abde1953a666'
down_revision = '8342dae658e2'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('protect_answer', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('protect_problem', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_protect_answer'), 'users', ['protect_answer'], unique=True)
    op.create_index(op.f('ix_users_protect_problem'), 'users', ['protect_problem'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_protect_problem'), table_name='users')
    op.drop_index(op.f('ix_users_protect_answer'), table_name='users')
    op.drop_column('users', 'protect_problem')
    op.drop_column('users', 'protect_answer')
    ### end Alembic commands ###
