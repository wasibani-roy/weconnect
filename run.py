from app import create_app
from app.database  import Database
import os

config_name = 'development'
app = create_app(config_name)

db = Database(os.environ["DATABASE_URL"])

if __name__ == '__main__':
    db.create_tables()
    app.run()
