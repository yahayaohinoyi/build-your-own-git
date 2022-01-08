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
            decompressed_blob = zlib.decompress(f.read()).decode()

            data = decompressed_blob.split()
            objectType, fileContent = data[0], ' '.join(data[1:])
            print(type(fileContent), type(fileContent[0]))
        return decompressed_blob



if __name__ == "__main__":
    main()
