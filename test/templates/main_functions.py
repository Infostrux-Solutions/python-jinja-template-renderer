from datetime import datetime

def addition(num1, num2):
    return num1 + num2

def calc_score(num):
    return division(num,120)

def current_date():
    return datetime.today().strftime('%Y-%m-%d')

def division(num1, num2):
    return num1/num2

def hello_world():
    message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
    officia deserunt mollit anim id est laborum.

    """
    return message
