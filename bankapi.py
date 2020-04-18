from bank_api import create_app, db, models
from config import config

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Account': models.Account, 'Customer': models.Customer}

if __name__ == '__main__':
    app.run()