import os
import sys
from collections import defaultdict
from hashlib import md5


def get_size_paths(root_dir: str, file_ext: str, reverse: bool):
    size_paths = defaultdict(list)
    for root, _, files in os.walk(root_dir):
        for name in files:
            path = os.path.join(root, name)
            if file_ext in os.path.splitext(name)[1]:
                size_paths[os.path.getsize(path)].append(path)
    return dict(sorted(size_paths.items(), reverse=reverse))


def show_size_paths(size_paths: dict):
    for size, paths in size_paths.items():
        if len(paths) > 1:
            print(f"\n{size} bytes", *paths, sep="\n")


def get_size_hash_paths(size_paths: dict):
    size_hash_paths = defaultdict(lambda: defaultdict(list))
    for size, paths in size_paths.items():
        if len(paths) > 1:
            for file in paths:
                with open(file, "rb") as f:
                    size_hash_paths[size][md5(f.read()).hexdigest()].append(file)

    return size_hash_paths


def show_size_hash_paths(size_hash_paths: dict):
    num_dup = 1
    path_file_duplicate = []
    for size, hashes in size_hash_paths.items():
        print(f"\n{size} bytes")
        for hash_, paths in hashes.items():
            if len(paths) > 1:
                print(f"Hash: {hash_}")
                for path in paths:
                    print(f"{num_dup}. {path}")
                    path_file_duplicate.append(path)
                    num_dup += 1
    return path_file_duplicate


def check_del():
    while True:
        try:
            num_del = [int(i) for i in input('Enter file numbers to delete:\n').split()]
            if len(num_del) < 1:
                print('Wrong format')
            return num_del
        except ValueError:
            print('Wrong format')


def delete_duplicate(path_file_duplicate: list):
    size_del = 0
    num_del = check_del()
    for num in num_del:
        with open(path_file_duplicate[num-1], "rb") as f:
            size_del += os.path.getsize(path_file_duplicate[num-1])

        os.remove(f'{path_file_duplicate[num-1]}')
    print(f'Total freed up space: {size_del} bytes')


def main():
    file_ext = "." + input("Enter file format:\n")

    print("Size sorting options:", "1. Descending", "2. Ascending\n", sep="\n")
    while (answer := input("Enter a sorting option:\n")) not in "12":
        print("Wrong option\n")
    reverse = answer == "1"

    size_paths = get_size_paths(root_folder, file_ext, reverse)
    show_size_paths(size_paths)

    while (check_duplicates := input("\nCheck for duplicates?\n")) not in ("yes", "no"):
        print("Wrong option\n")

    if check_duplicates == "yes":
        size_hash_paths = get_size_hash_paths(size_paths)
        duplicates =  show_size_hash_paths(size_hash_paths)

        while (delete_files := input("\nDelete files\n")) not in ("yes", "no"):
            print("Wrong option\n")
        if delete_files == "yes":
            delete_duplicate(duplicates)


if __name__ == "__main__":
    try:
        root_folder = sys.argv[1]
    except IndexError:
        print("Directory is not specified")
        sys.exit()
    else:
        main()
