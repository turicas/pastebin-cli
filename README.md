# pastebin-cli

Command-line interface to paste code/text to pastebin.com, written in pure
Python without any external dependency. If your operating system has an old
Python version: this software works from Python 3.5 to 3.8.

> Note: the command-line works fine but still needs some API features, like
> listing user pastes.


## Installation

You can either install it using `pip`:

```shell
pip install pastebin-cli
```

or download `pastebin.py` executable and put in your `$PATH` (you can rename it
to `pastebin`).


## Usage

```shell
$ pastebin --help
usage: pastebin [-h] [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}]
                [--api-key API_KEY]
                {paste,get} ...

optional arguments:
  -h, --help            show this help message and exit
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
  --api-key API_KEY

Subcommands:
  {paste,get}
    paste               Paste a file
    get                 Get a specific paste
```

```shell
$ ./pastebin paste --help
usage: pastebin paste [-h] [--expires-in {N,10M,1H,1D,1W,2W,1M,6M,1Y}]
                      [--privacy {public,unlisted,private}]
                      [--file-format FILE_FORMAT]
                      filename

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  --expires-in {N,10M,1H,1D,1W,2W,1M,6M,1Y}
  --privacy {public,unlisted,private}
  --file-format FILE_FORMAT
```
