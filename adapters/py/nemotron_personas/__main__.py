"""`python -m nemotron_personas` -> show usage."""

from __future__ import annotations
import sys

USAGE = """nemotron_personas — civic persona panels from NVIDIA Nemotron-Personas-Korea

Subcommands:
  python -m nemotron_personas.fetch [--dry-run] [--force]
  python -m nemotron_personas.sampler --panel {national|local} [--size N] [--seed N]
"""

if __name__ == "__main__":
    print(USAGE)
    sys.exit(0)
