from django.contrib.auth.decorators import user_passes_test



def is_author(user):
    if user.user_type=="AUTHOR" or user.is_superuser:
        return True
    return False

def is_editor(user):
    if user.user_type=="EDITOR" or user.is_superuser:
        return True
    return False