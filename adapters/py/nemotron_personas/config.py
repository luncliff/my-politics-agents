"""Shared constants for nemotron_personas fetch + sample."""

from __future__ import annotations
import pathlib

# config.py path: <repo>/adapters/py/nemotron_personas/config.py
# parents: [0]=adapters/py/nemotron_personas, [1]=adapters/py, [2]=adapters, [3]=repo root
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]

DATASET_REPO = "nvidia/Nemotron-Personas-Korea"
HF_RESOLVE_BASE = f"https://huggingface.co/datasets/{DATASET_REPO}/resolve/main"

LICENSE = "CC BY 4.0"
ATTRIBUTION = "NVIDIA Nemotron-Personas-Korea (https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea)"

RAW_DIR = (
    REPO_ROOT
    / "archive"
    / "raw"
    / "huggingface.co"
    / "datasets"
    / "nvidia"
    / "Nemotron-Personas-Korea"
)
PROCESSED_DIR = REPO_ROOT / "archive" / "processed" / "nemotron-personas"

# Fields kept in panel cards. Names are excluded by policy: although synthetic,
# they may collide with real persons. Card library focuses on demographics + persona text.
DEFAULT_FIELDS = [
    "uuid",
    "sex",
    "age",
    "age_group",
    "marital_status",
    "education_level",
    "occupation",
    "province",
    "district",
    "household_type",
    "professional_persona",
    "concise_persona",
    "hobbies_and_interests",
    "cultural_background",
    "skills_and_expertise",
    "goals_and_ambitions",
]
