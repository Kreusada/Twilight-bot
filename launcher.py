"""
MIT License

Copyright (c) 2020 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys

import click

from bot import twilight


def run_bot(no_cogs, dev):
    try:
        twilight.run(no_cogs=no_cogs, dev=dev)
    except KeyboardInterrupt:
        print("Exiting Twilight!")
        twilight.stop()
    finally:
        exit_code = twilight.exit_code
        sys.exit(exit_code)


@click.command(help="Run Twilight")
@click.option("--no-cogs", is_flag=True, default=False, help="Run the bot without cogs (only has ping/help/load)")
@click.option("-d", "--dev", default=False, is_flag=True, help="Run the bot and lock the commands to the Dev")
def main(no_cogs, dev):
    run_bot(no_cogs=no_cogs, dev=dev)


if __name__ == "__main__":
    main()
# TODO: More options and cli
