#!/usr/bin/env python3
# Author: Archit
import sys
import subprocess

if len(sys.argv) != 2:
    print("Usage: python reconator.py <target-domain>")
    sys.exit(1)

target = sys.argv[1]
subprocess.run(["bash", "reconator.sh", target])

