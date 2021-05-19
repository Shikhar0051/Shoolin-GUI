"""
Usage:
  anubis (-t TARGET | -f FILE) [-o FILENAME]  [-abinoprsSv] [-w SCAN] [-q NUM]
  anubis -h
  anubis --version
  
Options:
  -h --help                       show this help message and exit
  -t --target                     set target (comma separated, no spaces, if multiple)
  -f --file                       set target (reads from file, one domain per line)
  -n --with-nmap                  perform an nmap service/script scan
  -o --output                     save to filename
  -i --additional-info            show additional information about the host from Shodan (requires API key)
  -p --ip                         outputs the resolved IPs for each subdomain, and a full list of unique ips
  -a --send-to-anubis-db          send results to Anubis-DB
  -r --recursive                  recursively search over all subdomains
  -s --ssl                        run an ssl scan and output cipher + chain info
  -S --silent                     only out put subdomains, one per line
  -w --overwrite-nmap-scan SCAN   overwrite default nmap scan (default -nPn -sV -sC)
  -v --verbose                    print debug info and full request output
  -q --queue-workers NUM          override number of queue workers (default: 10, max: 100)
  --version                       show version and exit

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/jonluca/anubis
"""

import sys
import time
from functools import reduce

from docopt import docopt

# noinspection PyPep8Naming
from . import __version__ as VERSION


# Overload stdout to save output and change colors on filewrite
class StdOutHook:
  lines = []
  filename = ""

  def __init__(self, filename, silent, output):
    self.filename = filename
    self.silent = silent
    self.output = output

  def write(self, text, override=False, **kwargs):
    if not self.silent or override:
      sys.__stdout__.write(text)
    self.lines.append(text)

  def write_out(self):
    if self.output:
      with open(self.filename, "w") as file:
        for line in self.lines:
          # remove stdout colors
          line = line.replace('\033[91m', '')
          line = line.replace('\033[92m', '')
          line = line.replace('\033[93m', '')
          line = line.replace('\033[94m', '')
          line = line.replace('\033[95m', '')
          line = line.replace('\033[0m', '')
          file.write(line)

  def flush(self):
    # python3 compatability, does nothing
    pass


# credit to https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
def seconds_to_str(t):
  return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                                      [(t * 1000,), 1000, 60, 60])


def main(options):
  try:
    start_time = time.time()

    import anubis.commands

    #options = docopt(__doc__, version=VERSION)

    if options["--output"] or options['--silent']:
      sys.stdout = StdOutHook(options["FILENAME"], options['--silent'],
                              options['--output'])

    command = anubis.commands.Target(options)
    command.run()
    print("Subdomain search took %s" % seconds_to_str(time.time() - start_time))
    if options["--output"]:
      sys.stdout.write_out()
  except KeyboardInterrupt:
    print("\nQuitting...")
    sys.exit(0)
