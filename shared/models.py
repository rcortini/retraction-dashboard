from sqlalchemy import (
    Table, Column, MetaData,
    String, Integer, Date, Boolean, TIMESTAMP
)

metadata = MetaData()

works = Table(
    "works",
    metadata,
    Column("id", String, primary_key=True),
    Column("doi", String),
    Column("title", String),
    Column("publication_year", Integer),
    Column("publication_date", Date),
    Column("updated_date", TIMESTAMP),
)