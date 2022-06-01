import hashlib
import time
import os


# Takes the filename as input, concatenates it with UNIX time and hashes the result
# It avoids collision in case of user tries to upload files with the same name
def hash_filename(filename):
    filename_parts = os.path.splitext(filename)
    str_to_hash = (filename_parts[0] + str(time.time())).encode('utf-8')
    hash = hashlib.md5(str_to_hash)
    return str(hash.hexdigest() + filename_parts[1])


if __name__ == '__main__':
    print(hash_filename('zidane.jpg'))
