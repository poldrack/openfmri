#!/usr/bin/env python
"""get_betaseries.py - wrapper for pybetaseries

USAGE: get_betaseries.py <featdir>
"""

from pybetaseries import *
import sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

if len(sys.argv)<2:
    usage()

pybetaseries(sys.argv[1])
