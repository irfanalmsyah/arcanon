import random
import string


def generate_random_string():
    chars = string.ascii_letters + string.digits + "_"
    return "".join(random.choice(chars) for _ in range(32))
