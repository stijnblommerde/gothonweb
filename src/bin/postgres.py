from web import database
from utils import check_password

db = database(dbn='postgres', db='mydb', user='', password='')


def check_credentials(email, password):
    records = db.query(
        'SELECT hashed_password, salt '
        'FROM example_users '
        'WHERE email=$email ',
        vars={'email': email})
    if len(records) > 0:
        record = records[0]
        return check_password(record['hashed_password'],
                              password,
                              record['salt'],)
    else:
        return False


def unique_email(email):
    records = db.query(
        'SELECT id '
        'FROM example_users '
        'WHERE email=$email ',
        vars={'email': email})
    print len(records) == 0
    return len(records) == 0