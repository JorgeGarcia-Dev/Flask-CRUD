from decouple import config
from flask.cli import with_appcontext

import pymysql
import click

# Database Connection
def connection():
    """
    It connects to the database and returns the connection object
    :return: The connection to the database.
    """
    db = pymysql.connect(
        host = config('HOST_MYSQL'),
        database = config('DB_MYSQL'),
        user = config('USER_MYSQL'),
        password = config('PASSWORD_MYSQL')
    )
        
    return db

# Init DB
def close_db(e=None):
    
    db = db.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    
    db = connection()

    db.commit()

@click.command('init_db')
@with_appcontext

def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)