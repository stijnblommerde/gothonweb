from web import form, database
from postgres import check_credentials, unique_email
from lexicon import scan
from my_parser import parse_sentence, ParserError

db = database(dbn='postgres', db='mydb', user='', password='')


def parse_answer(answer):
    print 'enter parse_answer'
    print answer
    try:
        word_list = scan(answer)
        sentence = parse_sentence(word_list)
        return True
    except ParserError as e:
        return False

# field validators
vusername = form.regexp(r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",
                        'only ASCII letters and digits, with hyphens, '
                        'underscores and spaces as internal separators')
vemail = form.regexp(r".*@.*", "must be a valid email address")
vemail_unique = form.Validator('email exists', unique_email)
vpassword = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vanswer = form.Validator('answer not understood', parse_answer)

# form validators
valid_credentials = form.Validator(
    "Invalid email or password",
    lambda i: check_credentials(i.email, i.password))

login_form = form.Form(
    form.Textbox('email', vemail, class_="form-control"),
    form.Password('password', vpassword, class_="form-control"),
    form.Button('LOGIN', class_="btn btn-default"),
    validators=[valid_credentials],
)

register_form = form.Form(
    form.Textbox('username', vusername, class_="form-control"),
    form.Textbox('email', vemail, vemail_unique, class_="form-control"),
    form.Password('password', vpassword, class_="form-control"),
    form.Button('REGISTER', class_="btn btn-default")
)

game_form = form.Form(
    form.Textbox('answer', vanswer, class_="form-control"),
    form.Button('SUBMIT', class_="btn btn-default")
)