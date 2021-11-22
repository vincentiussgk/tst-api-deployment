from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==== Password Hashing ====

# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify inputted pasword
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check if user exists
def user_exists(userData, name):
    for user in userData:
        if user["username"] == name:
            return user
    return False

# Check if user exists & login data matches
def check_user(userData, creds):
    user = user_exists(userData, creds["username"])
    if (user == False):
        return 404
    else:
        if (verify_password(creds["password"], user["password"])):
            return 200
        else:
            return 403
