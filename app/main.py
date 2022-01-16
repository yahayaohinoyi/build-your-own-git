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

    elif command == "write-tree":
        # argType = sys.argv[2]
        write_tree(f'{os.getcwd()}')

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

def hash_object(argType, file, caller = "main"):
    if argType == '-w':
        with open(file, 'rb') as f:
            size = os.stat(f'{file}').st_size
            read_file = f.read()
            header = f"blob {str(size)}\0".encode("utf-8")
            content = read_file.decode("utf-8")
            t = b"".join([header, read_file])
            compress = zlib.compress(t)
            sha_1 = hashlib.sha1(f"blob {size}\0{content}".encode("utf-8"))
            write_object(sha_1.hexdigest(), compress, file)
            if caller == "main":
                print(f"{sha_1.hexdigest()} \n")
            return f"{sha_1.hexdigest()}"

def write_object(hash, compress, file):
    try:
        dir = f'{os.getcwd()}/.git/objects/{hash[:2]}'
        if os.path.isfile(f"{dir}/{hash[2:]}"):
            return
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
    # print(content)
    for i in range(1, len(content) - 1):
        try:
            print(content[i].split()[-1].decode())
        except:
            continue
    

def filter_non_printable(_str):
    return ''.join(i for i in _str if ord(i)<128)

def write_tree(_dir):
    res = recur_tree(_dir)
    print(res)
    return res

def recur_tree(_dir):
    children = []
    _hash = ""
    nei = [n for n in os.listdir(_dir) if n != ".git"]
    for node in nei:
        if not is_directory(f'{_dir}/{node}'):
            _hash = hash_object("-w", f'{_dir}/{node}', caller="write_tree")
        elif node != '.git':
            _hash = recur_tree(f'{_dir}/{node}')
        children.append((_hash, node))
    _hash = commit_tree(sorted(children, key=lambda x: x[-1]), _dir)
    return _hash

def concat_bytes(f, s):
    return b"".join([f, s])

def commit_tree(children, _dir):
    tree = f"".encode()
    for child in children:
        mode = get_mode(f"{_dir}/{child[1]}")
    
        content_info = concat_bytes(f"{mode} {child[1]}\0".encode(), child[0].encode())

        tree = concat_bytes(tree, content_info)   

    size = len(tree)
    tree = concat_bytes(f"tree {size}\0".encode(), tree)

    tree_sha = hashlib.sha1(tree).hexdigest()

    sha_dir = f'{os.getcwd()}/.git/objects/{tree_sha[:2]}'
    sha_file = f'{sha_dir}/{tree_sha[2:]}'

    if not os.path.exists(sha_dir):
        os.mkdir(sha_dir)

    with open(sha_file, "wb") as fp: 
        fp.write(zlib.compress(tree))
    return tree_sha

def is_directory(path):
    return os.path.isdir(path)

def get_mode(path):
    if path[-3:] == ".sh":
        return "100755"

    if os.path.isfile(path):
        return "100644"

    if is_directory(path):
        return "040000"

    if os.path.islink(path):
        return "120000"

if __name__ == "__main__":
    main()
