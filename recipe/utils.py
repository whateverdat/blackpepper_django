import string


# Custom functions
# https://djuices.com/topic/username-validation-in-python/
def proper_username(username):
    '''
    Your username must be 4 to 16 characters long with no spaces; 
    and can only use letters, numbers and include underscores "_"
    '''

    proper = string.ascii_letters + string.digits + "_"
    if not all(char in proper for char in username):
        return False
    if not (16 >= len(username) >= 4):
        return False
    if all(char in "_" for char in username):
        return False
    return True
    