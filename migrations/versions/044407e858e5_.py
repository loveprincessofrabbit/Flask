"""empty message

Revision ID: 044407e858e5
Revises: abde1953a666
Create Date: 2017-05-29 15:04:28.506684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '044407e858e5'
down_revision = 'abde1953a666'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_protect_problem', table_name='users')
    op.drop_column('users', 'protect_problem')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('protect_problem', sa.VARCHAR(length=64), nullable=True))
    op.create_index('ix_users_protect_problem', 'users', ['protect_problem'], unique=1)
    ### end Alembic commands ###