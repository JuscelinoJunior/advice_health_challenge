from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

# SQAlchemy model classes
Base = declarative_base()

# Database connection
db_engine = create_engine("mysql+mysqldb://root:root@172.16.241.5:3306/advice_health_challenge")
