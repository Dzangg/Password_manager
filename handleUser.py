import bcrypt

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
import secrets
import json

import random
import string

import shutil

current_dir = os.getcwd()
usersDir = current_dir + "/users/"


# ------------------- Cryptography & Hash Section -------------------

# generate random salt
def generateRandomSalt():
    salt = bcrypt.gensalt()
    return salt


# hash password with given salt
def hash_password(password, salt):
    hashed = bcrypt.hashpw(password, salt)
    return hashed


# use to encrypt user data
def create_firstKey():
    # randon num key
    key = secrets.token_hex(16)
    return key


# use to encrypt key1
def create_secondKey(passwd):
    passwd = passwd.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=passwd,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwd))

    return key


def encrypt_firstKey(first_key, second_key):
    f = Fernet(second_key)
    encrypted_first_key = f.encrypt(first_key.encode())
    return encrypted_first_key


def decrypt_firstKey(encrypted_firstkey, password):
    second_key = create_secondKey(password)
    f = Fernet(second_key)
    decrypted_firstKey = f.decrypt(encrypted_firstkey)
    return decrypted_firstKey


def decrypt_data(password, data):
    second_key = create_secondKey(password)
    f = Fernet(second_key)
    decrypted_data = f.decrypt(data)
    normal_format = json.loads(decrypted_data)
    return normal_format


def encrypt_data(password, data):
    second_key = create_secondKey(password)
    f = Fernet(second_key)
    json_data = json.dumps(data, indent=4)
    json_data = json_data.encode()
    encrypted_data = f.encrypt(json_data)
    return encrypted_data


def compare_passwords(user, given_password):
    hashed = read_hashed(user).encode()
    salt = read_salt(user)
    hashed_given = hash_password(given_password.encode(), salt.encode())
    print("given ", hashed_given)
    print("hashed ", hashed)
    if hashed_given == hashed:
        return True
    return False


def generate_random_password():
    characterList = ""
    characterList += string.ascii_letters
    characterList += string.digits
    characterList += string.punctuation
    password = ""
    for i in range(20):
        randomChar = random.choice(characterList)
        password += randomChar

    return password


# ------------------- File Section -------------------


def createUsers():
    os.makedirs(current_dir + "/users")


def userExists(user):
    if not os.path.exists(usersDir + user):
        return False
    return True


def createUserFiles(user):
    # create users/user directory
    os.makedirs(usersDir + user)

    # key file
    with open(usersDir + user + "/file_key.key", "w") as file:
        pass

    # db file
    with open(usersDir + user + "/user_info.json", "w") as file:
        pass

    # data file
    with open(usersDir + user + "/user_data.json", "w") as file:
        pass


# create app directory
def initializeDirectory():
    if not os.path.isdir(current_dir + "/users") and not os.path.isfile(current_dir + "/users"):
        createUsers()


# saves generated firstKey to .key file
def write_firstKey(user, encrypted_first_key):
    data = []
    data.append({"Key": encrypted_first_key.decode()})
    json_data = json.dumps(data, indent=4)

    with open(usersDir + user + "/file_key.key", "w") as f:
        f.write(json_data)


# reads encrypted and return decrypted
def read_firstKey(user, password):
    fileObject = open(usersDir + user + "/file_key.key", "r")
    jsonContent = fileObject.read()
    encrypted_firstkey = json.loads(jsonContent)
    decrypted_firstkey = decrypt_firstKey(encrypted_firstkey, password)
    return decrypted_firstkey


# reads encrypted and return decrypted
def read_data(user, password):
    local_dir = usersDir + user + "/user_data.json"
    if os.path.getsize(local_dir) == 0:
        return False
    fileObject = open("test.json", "r")

    jsonContent = fileObject.read()

    print(jsonContent)
    data = json.loads(jsonContent)
    decrypted = decrypt_data(password, data)
    print("decrypted: ", decrypted)
    return decrypted


def write_data(user, password, target, data):
    local_dir = ""
    if target == "key":
        local_dir = usersDir + user + "/file_key.key"
    if target == "data":
        local_dir = usersDir + user + "/user_data.json"

    encrypted_data = encrypt_data(password, data)

    with open(local_dir, 'w') as f:
        f.write(encrypted_data.decode())


def write_info(user, hashed, generatedSalt):
    local_dir = usersDir + user + "/user_info.json"
    generatedSalt = generatedSalt.decode()
    hashed = hashed.decode()
    data = {"salt": generatedSalt, "password": hashed}
    json_data = json.dumps(data, indent=4)

    with open(local_dir, 'w') as f:
        f.write(json_data)


def read_hashed(user):
    local_dir = usersDir + user + "/user_info.json"
    with open(local_dir, "r") as f:
        json_data = f.read()
    data = json.loads(json_data)
    return data["password"]


def read_salt(user):
    local_dir = usersDir + user + "/user_info.json"
    with open(local_dir, "r") as f:
        json_data = f.read()
    data = json.loads(json_data)
    return data["salt"]


def del_user(user):
    local_dir = usersDir + user
    shutil.rmtree(local_dir)
