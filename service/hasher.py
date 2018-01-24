import hashlib
import random
import string

salt_length = 5


def __make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(salt_length)])


def make_hash_from(text):
    return __hash_it(text) + __make_salt()


def __hash_it(text):
    return hashlib.sha256(str.encode(text)).hexdigest()


def are_strings_same(text, hash):
    hash_no_salt = hash[:-salt_length]
    return __hash_it(text) == hash_no_salt
