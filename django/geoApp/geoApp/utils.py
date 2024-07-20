import datetime
import re

# function definition
#--------------------------------------------------------

def generate_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def has_non_alphanumeric_characters(stringa):
    pattern_obj = re.compile(r'[^a-zA-Z0-9_]')
    match_obj = pattern_obj.search(stringa)
    non_alphanumeric_characters_are_found = bool(match_obj)
    return non_alphanumeric_characters_are_found 