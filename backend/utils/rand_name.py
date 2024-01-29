import string
import random

def rand_name(length, obj, func):
    while True:
        name = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not obj.objects.filter(func = name).exists():
            return name