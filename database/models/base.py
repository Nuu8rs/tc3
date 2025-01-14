from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

Base = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(_, __, **___):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

@compiles(utcnow, "sqlite")
def sqlite_utcnow(_, __, **___):
    return "DATETIME('now')"

@compiles(utcnow, "mysql")
def mysql_utcnow(_, __, **___):
    return "CURRENT_TIMESTAMP"