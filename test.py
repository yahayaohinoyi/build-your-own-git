# def commit_tree(children, _dir):
#     tree = f"".encode()
#     for child in children:
#         mode = get_mode(f"{_dir}/{child[1]}")

#         compressed_sha = zlib.compress(child[0].encode())
    
#         content_info = concat_bytes(f"{mode} {child[1]}\0".encode(), compressed_sha)

#         tree = concat_bytes(tree, content_info)   

#     size = len(tree)
#     tree = concat_bytes(f"tree {size}\x00".encode(), tree)
#     tree_sha = hashlib.sha1(tree).hexdigest()

#     sha_dir = f'{os.getcwd()}/.git/objects/{tree_sha[:2]}'
#     sha_file = f'{sha_dir}/{tree_sha[2:]}'

#     if not os.path.exists(sha_dir):
#         os.mkdir(sha_dir)

#     with open(sha_file, "wb") as fp: 
#         fp.write(zlib.compress(tree))
#     return tree_sha


# def make_hash(file, size, hash, mode):
#     new_line = "\n"
#     tree = f"tree {size}\x00{mode} {file}\x00{new_line}{hash}"
#     tree1 = tree.rstrip("\n")
#     t = zlib.compress(tree.encode());
#     t1 = zlib.compress(tree1.encode());

#     print("encoded and compressed hash ", hashlib.sha1(t).hexdigest())
#     print("encoded alone", hashlib.sha1(tree.encode()).hexdigest())



# make_hash("file1.txt", "37", "3b18e512dba79e4c8300dd08aeb37f8e728b8dad", "100644")


# (echo -n "tree 37\x00100644 file1.txt\x00"; echo -n "3b18e512dba79e4c8300dd08aeb37f8e728b8dad" | xxd -r -p) | sha1sum
# 82424451ac502bd69712561a524e2d97fd932c69
import os
import zlib
import hashlib

def view(hash):
    file = f'{os.getcwd()}/.git/objects/{hash[:2]}/{hash[2:]}'
    with open(file, 'rb') as f:
        content = zlib.decompress(f.read())
        print(content)

def act(hash):
    file = f'{os.getcwd()}/.git/objects/{hash[:2]}/{hash[2:]}'
    with open(file, 'rb') as f:
        content = zlib.decompress(f.read()).decode("utf-8", errors="ignore")
        print(content)

view("de0c78bc82012ee952f33ea9d582c8a4a9b863b9")
print("-"*200)
view("659240bbd957abe4875da08d093e539ec639faae")
print("*"*200)
act("de0c78bc82012ee952f33ea9d582c8a4a9b863b9")
print("-"*200)
act("659240bbd957abe4875da08d093e539ec639faae")
