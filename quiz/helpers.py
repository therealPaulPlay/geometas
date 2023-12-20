import re

def convert_string_to_snakecase(string):
    """ 
    Convert spaces to _
    Remove anything in brackets including the brackets 
    Remove all other special chars
    Remove any _ at beginning or end of string
    Convert to lowercase 
    """
    string = string.replace(" ", "_")
    string = re.sub(r'\(.*?\)', '', string)
    string = re.sub(r'[^A-Za-z0-9_]+', '', string)
    string = string.replace("__", "_")
    string = string.strip("_")
    string = string.lower()
    return string