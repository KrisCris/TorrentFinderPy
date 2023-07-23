import os
import argparse
import re
from bencodepy import decode_from_file
from zhconv import convert

def find_torrents(dir_path, match_pattern):
    match_pattern = convert(match_pattern, 'zh-cn')  # Convert input to Simplified Chinese
    pattern = re.compile(match_pattern, re.IGNORECASE)
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.torrent'):
                torrent_path = os.path.join(root, file)
                try:
                    data = decode_from_file(torrent_path)
                    name = data[b'info'][b'name'].decode('utf-8')
                    name_simplified = convert(name, 'zh-cn')  # Convert torrent name to Simplified Chinese
                    if pattern.search(name_simplified):
                        print(f"- {torrent_path}")
                except (KeyError, UnicodeDecodeError):
                    print(f"Could not decode torrent file: {torrent_path}")

def main():
    parser = argparse.ArgumentParser(description="Find torrent files by name.")
    parser.add_argument("-p", "--path", type=str, required=True, help="Directory path to search for .torrent files.")
    parser.add_argument("-n", "--name", type=str, required=True, help="Regex pattern to search for in torrent files.")
    args = parser.parse_args()

    find_torrents(args.path, args.name)

if __name__ == "__main__":
    main()