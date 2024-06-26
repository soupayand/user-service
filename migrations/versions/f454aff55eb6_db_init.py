"""db init

Revision ID: f454aff55eb6
Revises: 
Create Date: 2024-04-09 09:03:42.188135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f454aff55eb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Enums should be named explicitly to avoid issues
    roletype_enum = sa.Enum('ADMIN', 'CUSTOMER', 'MERCHANT', name='roletype')

    # ### commands auto generated by Alembic - please adjust! ###
    role_table = op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', roletype_enum, nullable=False),
        sa.Column('description', sa.String(length=256), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('type')
    )

    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=True),
        sa.Column('email', sa.String(length=80), nullable=False),
        sa.Column('date_of_birth', sa.DateTime(), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table('user_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Pre-fill the role table
    op.bulk_insert(role_table,
        [
            {'type': 'ADMIN', 'description': 'Administrator', 'active': True},
            {'type': 'CUSTOMER', 'description': 'Customer', 'active': True},
            {'type': 'MERCHANT', 'description': 'Merchant', 'active': True},
        ]
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
