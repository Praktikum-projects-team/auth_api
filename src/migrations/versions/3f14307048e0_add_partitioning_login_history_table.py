"""Add partitioning login_history table

Revision ID: 3f14307048e0
Revises: 24ec1405a840
Create Date: 2023-06-08 12:59:04.909706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f14307048e0'
down_revision = '24ec1405a840'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('login_history', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    op.execute(
        sa.text(
            "CREATE TABLE login_history_new ("
            "id UUID NOT NULL, "
            "user_id UUID NOT NULL, "
            "user_agent VARCHAR(250) NOT NULL, "
            "auth_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL, "
            "PRIMARY KEY (id, auth_datetime)"
            ") PARTITION BY RANGE (auth_datetime)"
        )
    )

    for i in range(1, 13):
        year = '2023'
        month = str(i).zfill(2)
        table_name = f'login_history_y{year}m{month}'
        start_date = f'{year}-{month}-01'

        if i == 12:
            end_date = f'{str(int(year) + 1)}-{str(1).zfill(2)}-01'
        else:
            end_date = f'{year}-{str(i + 1).zfill(2)}-01'

        op.execute(
            sa.text(
                f"CREATE TABLE {table_name} "
                f"PARTITION OF login_history_new "
                f"FOR VALUES FROM ('{start_date}') TO ('{end_date}')"
            )
        )
        op.execute(
            sa.text(
                f"CREATE INDEX {table_name}_user_id_idx ON {table_name} (user_id)"
            )
        )

    op.execute(
        sa.text(
            "INSERT INTO login_history_new (id, user_id, user_agent, auth_datetime) "
            "SELECT id, user_id, user_agent, auth_datetime FROM login_history"
        )
    )
    op.drop_table('login_history')
    op.rename_table('login_history_new', 'login_history')
    op.create_index('idx_login_history_auth_datetime', 'login_history', ['auth_datetime'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_login_history_auth_datetime', table_name='login_history')

    op.rename_table('login_history', 'login_history_new')
    op.create_table('login_history', sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('user_id', sa.String(length=36), nullable=False),
                    sa.Column('user_agent', sa.String(length=50), nullable=False),
                    sa.Column('auth_datetime', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.execute(
        sa.text(
            "INSERT INTO login_history (id, user_id, user_agent, auth_datetime) "
            "SELECT id, user_id, user_agent, auth_datetime FROM login_history_new"
        )
    )
    op.drop_table('login_history_new')

    with op.batch_alter_table('login_history', schema=None) as batch_op:
        batch_op.dropconstraint(None, type='unique')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.dropconstraint(None, type='unique')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.dropconstraint(None, type='unique')

    # ### end Alembic commands ###
