"""Initial migration.

Revision ID: 24ec1405a840
Revises: 
Create Date: 2023-05-29 19:44:29.568794

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24ec1405a840'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    roles_table = op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('login_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.Column('auth_datetime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.Column('given_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    default_roles = [
        {'id': uuid.uuid4(), 'name': 'admin'},
        {'id': uuid.uuid4(), 'name': 'user'}
    ]
    op.bulk_insert(roles_table, default_roles)


def downgrade():
    op.drop_table('user_roles')
    op.drop_table('login_history')
    op.drop_table('users')
    op.drop_table('roles')

