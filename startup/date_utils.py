import datetime


def parse_form_date(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")


def parse_form_date_without_seconds(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")


def parse_form_time(date):
    return datetime.datetime.strptime(date, "%H:%M")
