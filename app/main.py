import sys
import os
import zlib
import hashlib
import string
import re


def main():
    # Uncomment this block to pass the first stage
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")

    elif command == "cat-file":
        argType = sys.argv[2]
        sha = sys.argv[3]
        cat_file(argType, sha)

    elif command == "hash-object":
        argType = sys.argv[2]
        file = sys.argv[3]
        hash_object(argType, file)

    elif command == "ls-tree":
        argType = sys.argv[2]
        tree_sha = sys.argv[3]
        ls_tree(argType, tree_sha)

    else:
        raise RuntimeError(f"Unknown command #{command}")

def cat_file(argType, sha):
    if argType == "-p":
        file = f".git/objects/{sha[:2]}/{sha[2:]}"
        with open(file, "rb") as f:
            decompressed_blob = zlib.decompress(f.read()).decode('utf-8')
            remove_header_from_decompresses_blob(decompressed_blob)

def remove_header_from_decompresses_blob(db):
    data = db.split()
    objectType, fileContent = data[0], ' '.join(data[1:])
    s, ind = get_file_size(fileContent)
    start_ind = get_starting_index_of_content(ind, fileContent)
    content = fileContent[start_ind:].strip()
    print(content, end="")

def get_file_size(fileContent):
    size, i = '', 0
    while fileContent[i].isdigit():
        size += fileContent[i]
        i += 1
    return [size, i]

def get_starting_index_of_content(ind_1, fileContent):
    ind_1 += 1
    while fileContent[ind_1].isdigit():
        ind_1 += 1
    return ind_1

def hash_object(argType, file):
    if argType == '-w':
        with open(file, 'rb') as f:
            size = os.stat(f'{os.getcwd()}/{file}').st_size
            read_file = f.read()
            header = f"blob {str(size)}\0".encode("utf-8")
            content = read_file.decode("utf-8")
            t = b"".join([header, read_file])
            compress = zlib.compress(t)
            sha_1 = hashlib.sha1(f"blob {size}\0{content}".encode("utf-8"))
            write_object(sha_1.hexdigest(), compress, file)
            print(f"{sha_1.hexdigest()} \n")

def write_object(hash, compress, file):
    try:
        dir = f'{os.getcwd()}/.git/objects/{hash[:2]}'
        if not os.path.exists(dir):
            os.mkdir(dir)
        sha_file = f'{os.getcwd()}/.git/objects/{hash[:2]}/{hash[2:]}' 
        with open(sha_file, "wb") as fp: 
            fp.write(compress)

    except:
        # print(ex)
        file = f'{os.getcwd()}/.git/objects/{hash[:2]}/{hash[2:]}'
        if os.path.exists(file):
            os.remove(file)

def ls_tree(argType, hash):
    try:
        if argType == "--name-only":
            file = f'{os.getcwd()}/.git/objects/{hash[:2]}/{hash[2:]}'
            if not os.path.exists(file):
                raise FileNotFoundError("file not found, check hash and try again")
            with open(file, 'rb') as f:
                content = zlib.decompress(f.read())
                print_tree(content)

    except Exception as ex:
        print(ex)

def print_tree(content):
    content = content.split(b"\x00")
    for i in range(1, len(content), 2):
        print(content[i].split()[-1].decode())
    

def filter_non_printable(_str):
    return ''.join(i for i in _str if ord(i)<128)

if __name__ == "__main__":
    main()
