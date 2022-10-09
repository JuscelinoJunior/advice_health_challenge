from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# SQAlchemy model classes
Base = declarative_base()

# Database connection
db_engine = create_engine("mysql+mysqldb://root:root@127.0.0.1/advice_health_challenge")
