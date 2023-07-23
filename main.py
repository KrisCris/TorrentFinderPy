import os
import re
import argparse
from bencodepy import decode_from_file
from zhconv import convert
import shutil
import hashlib

def decode_torrent(torrent_path: str) -> str:
    try:
        data = decode_from_file(torrent_path)
        name = data[b'info'][b'name'].decode()
        return name
    except Exception as e:
        print(f"Failed to decode torrent file at {torrent_path} due to error: {e}")
        return None


def find_torrent(dir_path: str, match_string: str = None, use_regex: bool = False) -> dict:
    match_string = convert(match_string, 'zh-cn')  # Convert Chinese Characters to SC
    matched_torrents = {}
    for root, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.torrent'):
                continue
            torrent_path = os.path.join(root, file)
            decoded_name = decode_torrent(torrent_path)
            if decoded_name is None:
                continue
            rel_p = rel_path(dir_path, torrent_path)
            name_simplified = convert(decoded_name, 'zh-cn')  # Convert Chinese Characters to SC
            if use_regex:
                try:
                    pattern = re.compile(match_string, re.IGNORECASE)
                except Exception as e:
                    print(f"[ERROR]\t Invalid RegEx: {match_string}")
                    exit(1)
                if pattern.search(name_simplified):
                    matched_torrents[rel_p] = decoded_name
            else:
                if match_string is None or match_string.lower() in name_simplified.lower():
                    matched_torrents[rel_p] = decoded_name
                    
    return matched_torrents


def get_md5(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def handle_torrents(matched_torrents: dict, dir_path: str, move_path: str, no_rename: bool = False):
    if move_path is not None:
        target_dir = dir_path if move_path == "" else move_path

        if not os.path.isdir(target_dir) or not os.access(target_dir, os.W_OK):
            print(f"Destination directory {file_color(target_dir)} is not valid or write-protected.")
            return
        
        print(f"\nFiles copied to: {file_color(target_dir)}:")
        for file, decoded_name in matched_torrents.items():
            file = os.path.join(dir_path, file)
            if no_rename:
                base_name = os.path.basename(file)
            else:
                base_name = f"{decoded_name}.torrent"

            destination_path = os.path.join(target_dir, base_name)
            if os.path.normpath(file) == os.path.normpath(destination_path):
                continue

            if os.path.exists(os.path.join(target_dir, base_name)):
                if get_md5(file) == get_md5(destination_path):
                    print(f"[Info] {file_color(base_name)} exists with the same content, skipping.")
                    continue
                i = 1
                while os.path.exists(os.path.join(target_dir, base_name)):
                    base_name = f"{decoded_name}_{i}.torrent"
                    i += 1
                destination_path = os.path.join(target_dir, base_name)

            shutil.copy(file, destination_path)
            print(f"- {file_color(base_name)}")
            

def file_color(name: str) -> str:
    return f"\033[32m{name}\033[0m"

def rel_path(root: str, file: str) -> str:
    relPath = f"{os.path.relpath(file, root)}"
    if not relPath.startswith("."):
        relPath = "./" + relPath
    return relPath


def main():
    parser = argparse.ArgumentParser(description='Find .torrent files in a directory that match a given pattern.')
    parser.add_argument('-p', '--path', help='The directory path to search for .torrent files', required=True)
    parser.add_argument('-l', '--list', help='The pattern to match in torrent names', required=False, default=None, nargs='?', const="")
    parser.add_argument('-m', '--move', help='The directory to move and rename matched files to', default=None, nargs='?', const="")
    parser.add_argument('-r', '--regex', help='Use regex to match torrent names', action='store_true')
    parser.add_argument('--norename', help='Only copy files, don\'t rename', action='store_true')

    args = parser.parse_args()
    matched_torrents = find_torrent(args.path, args.list, args.regex)

    print(f"{len(matched_torrents)} matched torrents:")
    for rel, decoded_name in matched_torrents.items():
        print(f"- {file_color(decoded_name)}")
        print(f"  - {rel}")

    handle_torrents(matched_torrents, args.path, args.move, args.norename)

if __name__ == "__main__":
    main()
