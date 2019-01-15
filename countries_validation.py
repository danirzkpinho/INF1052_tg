import re


def validate_iso(field):
    regex = "[A-Z][A-Z]"
    return re.fullmatch(regex, field)


def validate_iso3(field):
    regex = "[A-Z][A-Z][A-Z]"
    return re.fullmatch(regex, field)


def validate_isonumeric(field):
    regex = "[0-9][0-9][0-9]"
    return re.fullmatch(regex, field)


def validate_fips(field):
    regex = "[A-Z][A-Z]"
    return re.fullmatch(regex, field)


def validate_country(field):
    regex = "[A-Z][a-z]{4,}"
    return re.fullmatch(regex, field)


def validate_capital(field):
    regex = "[A-Z][a-z]{3,}"
    return re.fullmatch(regex, field)


def validate_area(field):
    regex = "[0-9]*[0-9]"
    return re.fullmatch(regex, field)


def validate_population(field):
    regex = "[0-9]*[0-9]"
    return re.fullmatch(regex, field)


continents = ["AF", "AS", "EU", "NA", "OC", "SA", "AN"]


def validate_continent(field):
    return field in continents


def validate_tld(field):
    regex = "[.][a-z][a-z]"
    return re.fullmatch(regex, field)


def validate_currencycode(field):
    regex = "[A-Z][A-Z][A-Z]"
    return re.fullmatch(regex, field)


def validate_currencyname(field):
    regex = "[A-Z][a-z]{3,}"
    return re.fullmatch(regex, field)


def validate_phone(field):
    regex = "[0-9]*[0-9]"
    return re.fullmatch(regex, field)


def validate_postalcodeformat(field):
    return True


def validate_postalcoderegex(field):
    try:
        re.compile(field)
        return True
    except re.error:
        return False


def validate_languages(field):
    return True


def validate_geonameid(field):
    regex = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    return re.fullmatch(regex, field)


def validate_neighbours(field):
    countries = field.split(",")
    for country in countries:
        if not validate_iso(country):
            return False
    return True


def validate_equivalentfipscode(field):
    return True
