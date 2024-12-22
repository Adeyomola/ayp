from this.metadata import metadata
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = current_app.config['ENGINE'].connect()
    return g.db

def init_db():
    engine = current_app.config['ENGINE']
    metadata().create_all(engine)

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

import click
@click.command('db-init')
def db_init():
    init_db()
    click.echo('Database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(db_init)