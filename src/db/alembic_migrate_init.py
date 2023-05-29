from flask_migrate import Migrate

migrate = Migrate()

def init_migration_tool(app, db):
    migrate.init_app(app, db=db)
