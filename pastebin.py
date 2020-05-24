#!/usr/bin/env python
# Copyright 2020 Álvaro Justen <https://github.com/turicas/pastebin-cli/>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import mimetypes
import os
import sys
from pathlib import Path
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

EXPIRES_IN_CHOICES = "N 10M 1H 1D 1W 2W 1M 6M 1Y".split()
PRIVACY_CHOICES = {"public": "0", "unlisted": "1", "private": "2"}
LOG_LEVEL_CHOICES = "CRITICAL ERROR WARNING INFO DEBUG NOTSET".split()


def get_logger(level):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def error(message, exit_code):
    print("ERROR: {message}".format(message=message), file=sys.stderr)
    exit(exit_code)


class Pastebin:
    base_url = "https://pastebin.com"

    def make_url(self, path):
        return urljoin(self.base_url, path)

    def set_logger(self, logger):
        self.logger = logger

    def define_file_format(self, filename):
        extension = filename.name.rsplit(".", maxsplit=1)[-1]
        file_format = mimetypes.types_map[".{extension}".format(extension=extension)]
        file_format = file_format.split("/")[-1]
        if file_format.startswith("x-"):
            file_format = file_format[2:]
        return file_format

    def paste(self, args):
        filename = Path(args.filename)
        if not filename.exists():
            error("file '{filename}' not found.".format(filename=args.filename), 1)
        with open(filename) as fobj:
            paste_contents = fobj.read()

        url = self.make_url("/api/api_post.php")
        post_data = {
            "api_dev_key": args.api_key,
            "api_option": "paste",
            "api_paste_code": paste_contents,
            "api_paste_expire_date": args.expires_in,
            "api_paste_format": args.file_format or self.define_file_format(filename),
            "api_paste_name": filename.name,
            "api_paste_private": PRIVACY_CHOICES[args.privacy],
            "api_user_key": "",
        }
        self.logger.debug("POST to {url}: {post_data}".format(url=url, post_data=post_data))
        post_body = urlencode(post_data).encode("utf-8")
        request = Request(url, data=post_body, method="POST")
        response = urlopen(request)
        print(response.read().decode("utf-8"))

    def get(self, args):
        # TODO: implement get private paste (for authenticated user)
        key = args.paste_key
        if key.startswith("https://") or key.startswith("http://"):
            key = urlparse(key).path[1:]
        url = self.make_url("/raw/{key}".format(key=key))
        response = urlopen(url)
        print(response.read().decode("utf-8"))


def main():
    api = Pastebin()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level", default=os.environ.get("LOG_LEVEL", "INFO"), choices=LOG_LEVEL_CHOICES,
    )
    parser.add_argument("--api-key", default=os.environ.get("PASTEBIN_API_KEY"))
    subparsers = parser.add_subparsers(title="Subcommands")

    paste_parser = subparsers.add_parser("paste", help="Paste a file")
    paste_parser.add_argument("--expires-in", default="N", choices=EXPIRES_IN_CHOICES)
    paste_parser.add_argument("--privacy", default="private", choices=PRIVACY_CHOICES.keys())
    paste_parser.add_argument("--file-format")
    paste_parser.add_argument("filename")
    paste_parser.set_defaults(func=api.paste)

    get_parser = subparsers.add_parser("get", help="Get a specific paste")
    get_parser.add_argument("paste_key")
    get_parser.set_defaults(func=api.get)

    args = parser.parse_args()
    if not hasattr(args, "func"):  # No parameter passed
        parser.print_help()
    else:
        api.set_logger(get_logger(args.log_level))
        args.func(args)


if __name__ == "__main__":
    main()
