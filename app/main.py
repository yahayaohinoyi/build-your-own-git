import sys
import os
import zlib


def main():
    print("Your code goes here!")
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
        # decompressed_blob = zlib.decompress(sha)
        file = f".git/objects/{sha[:2]}/{sha[2:]}"
        # print(file)
        with open(file, "rb") as f:
            decompressed_blob = zlib.decompress(f.read()).decode()
            print(decompressed_blob)
        return decompressed_blob



if __name__ == "__main__":
    main()
