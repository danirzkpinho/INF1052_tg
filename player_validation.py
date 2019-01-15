import re

def validate_name(field):
    regex = "[A-Z][a-z]+([ ][A-Z][a-z]+)*"
    return re.fullmatch(regex, field)


def validate_date(field):
    regex = "(3[01]|[12][0-9]|0[1-9])\/(1[0-2]|0[1-9])\/[0-9]{4}"
    return re.fullmatch(regex, field)


positions = ["GL", "L", "LE", "LD", "T", "MAL", "MAT", "MC", "MCL", "MA", "AL", "SA", "PL"]

def validate_position(field):
    return field in positions

def validate_club(field):
    regex = "[a-zA-Z\s].{4,35}$"
    return re.fullmatch(regex, field)


def validate_email(field):
    regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(regex, field)


def validate_contact(field):
    regex = "(?:\+?44)?[0-9]\d{7,13}$"
    return re.fullmatch(regex, field)


def validate_agent(field):
    regex = "[A-Z][a-z]+([ ][A-Z][a-z]+)*"
    return re.fullmatch(regex, field)


def validate_state(field):
    regex = "[A-Z][a-z]+([ ][A-Z][a-z]+)*"
    return re.fullmatch(regex, field)


def validate_salary(field):
    regex = "[0-9]*\d"
    return re.fullmatch(regex, field)
