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

    # Create partitioning login_history table
    op.execute("""
    CREATE TABLE login_history_new (
    id UUID NOT NULL,
    user_id UUID NOT NULL,
    user_agent VARCHAR(50) NOT NULL,
    auth_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id, auth_datetime)
    ) PARTITION BY RANGE (auth_datetime);
    """)

    # Create partitioning login_history table
    for i in range(1, 13):
        year = '2023'
        month = str(i).zfill(2)
        table_name = f'login_history_y{year}m{month}'
        start_date = f'{year}-{month}-01'

        if i == 12:
            end_date = f'{str(int(year) + 1)}-{str(1).zfill(2)}-01'
        else:
            end_date = f'{year}-{str(i + 1).zfill(2)}-01'

        query = f"""
        CREATE TABLE {table_name}
        PARTITION OF login_history_new 
        FOR VALUES FROM ('{start_date}') TO ('{end_date}');
        """
        op.execute(query)

    # Copy data from login_history to login_history_new
    op.execute("""
    INSERT INTO login_history_new (id, user_id, user_agent, auth_datetime)
    SELECT id, user_id, user_agent, auth_datetime
    FROM login_history;
    """)
    # Drop login_history
    op.execute("""DROP TABLE login_history;""")
    # Rename login_history_new to login_history
    op.execute("""ALTER TABLE login_history_new RENAME TO login_history;""")
    # Create index for partitioning
    op.execute("""CREATE INDEX ON login_history (auth_datetime);""")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('login_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
