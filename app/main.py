import sys
import os
import zlib


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
    else:
        raise RuntimeError(f"Unknown command #{command}")

def cat_file(argType, sha):
    if argType == "-p":
        file = f".git/objects/{sha[:2]}/{sha[2:]}"
        with open(file, "rb") as f:
            # print()
            decompressed_blob = zlib.decompress(f.read()).decode('utf-8')
            remove_header_from_decompresses_blob(decompressed_blob)

def remove_header_from_decompresses_blob(db):
    data = db.split()
    objectType, fileContent = data[0], ' '.join(data[1:])
    s, ind = get_file_size(fileContent)
    start_ind = get_starting_index_of_content(ind, fileContent)
    print(fileContent[start_ind:])

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


if __name__ == "__main__":
    main()
