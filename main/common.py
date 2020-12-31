from functools import wraps
from main import session, redirect, request, url_for, ALLOWED_EXTENSIONS
from string import digits, ascii_uppercase, ascii_lowercase
import random

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

def rand_generator(length=8):
    char = ascii_lowercase + ascii_uppercase + digits
    return "".join(random.sample(char, length))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member.member_login", next_url=request.url))  # request.url 은 현재 url
        return f(*args, **kwargs)
    return decorated_function