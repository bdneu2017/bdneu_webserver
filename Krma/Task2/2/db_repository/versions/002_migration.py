from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
entries = Table('entries', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_name', VARCHAR),
    Column('title', VARCHAR),
    Column('text', VARCHAR),
)

entries = Table('entries', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String),
    Column('title', String),
    Column('text', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entries'].columns['user_name'].drop()
    post_meta.tables['entries'].columns['username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entries'].columns['user_name'].create()
    post_meta.tables['entries'].columns['username'].drop()
