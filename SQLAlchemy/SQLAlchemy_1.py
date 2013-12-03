from sqlalchemy import *

# Create an SQL Engine object: "engine://user:password@host:port/database"
db = create_engine("postgres://taiwan_user:taiwan@localhost:5432/postgres")
db.echo = False

metadata = BoundMetaData(db)

