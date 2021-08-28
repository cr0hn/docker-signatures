import re
import sys
import json
import select
import argparse

from typing import List

REGEX_SIGNERS = re.compile(r'''([\d]{1,3})(.*)([\w\d]{64})(.*)(.*)''')


def match_input_plain(input_text: str) -> List[dict]:
    ret = []

    for found in REGEX_SIGNERS.finditer(input_text):
        _, _, signature, name, *_ = found.groups()

        ret.append({
            "signature": signature.strip(),
            "name": name.strip()
        })

    return ret

def match_input_json(input_text: str) -> List[dict]:
    json_content = json.loads(input_text)

    ret = []

    for e in json_content:
        signers = e.get("Signers", [])

        for s in signers:

            key = s.get("Keys", [])

            if key:
                signature = key[0].get("ID", {})
            else:
                continue

            ret.append({
                "signature": signature,
                "name": s.get("Name")
            })

    return ret

def check_signers(singers: List[dict], args: dict):
    quiet = args.get("quiet")
    input_signers = set(args.get("SIGNERS"))
    found_signers = set()

    # check signers
    for s in singers:
        signer = s.get("name")

        if signer in input_signers:
            found_signers.add(signer)

    missing_signers = input_signers - found_signers

    if missing_signers:

        if not quiet:
            for ms in missing_signers:
                print(f"[!] Missing signer: '{ms}'")

        else:
            exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Docker image signers checker'
    )
    parser.add_argument(dest="SIGNERS", nargs="+")
    parser.add_argument('-q', '--quiet',
                        action="store_true",
                        default=False,
                        help="quiet mode")
    parsed_cli = parser.parse_args()

    content = []
    if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:

        while line := sys.stdin.readline():
            content.append(line)

    if not content:
        raise OSError("This program must be used as a pipe")
    else:
        content = "".join(content)

    try:
        singers = match_input_json(content)
    except:
        singers = match_input_plain(content)

    try:
        check_signers(singers, parsed_cli.__dict__)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
