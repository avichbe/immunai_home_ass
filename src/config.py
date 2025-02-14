import os
import logging

# --- Directories ---
RAW_EXPERIMENT_DIR = "data"
STAGE1_DIR = "stage1_data"
STAGE2_DIR = "stage2_data"

# Ensure that the directories exist.
os.makedirs(RAW_EXPERIMENT_DIR, exist_ok=True)
os.makedirs(STAGE1_DIR, exist_ok=True)
os.makedirs(STAGE2_DIR, exist_ok=True)

# --- Logging Configuration ---
LOG_LEVEL = logging.INFO
LOG_FORMAT = '[%(name)s] %(asctime)s - %(levelname)s - %(message)s'

# --- ThreadPool Settings ---
MAX_WORKERS = 2

# --- File Extension ---
FILE_EXTENSION = ".json"