import datetime

# function definition
#--------------------------------------------------------

def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")