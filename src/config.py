import os
import logging

# --- Directories ---
RAW_EXPERIMENT_DIR = "raw_experiment_data"
STAGE1_DIR = "stage1_data"
STAGE2_DIR = "stage2_data"

# Ensure that the directories exist.
os.makedirs(RAW_EXPERIMENT_DIR, exist_ok=True)
os.makedirs(STAGE1_DIR, exist_ok=True)
os.makedirs(STAGE2_DIR, exist_ok=True)

# --- Logging Configuration ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

LOG_LEVEL = logging.INFO
LOG_FORMAT = '[%(name)s] %(asctime)s - %(levelname)s - %(message)s'

# Setup logging to output both to the file and to the console.
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Optional: Remove this if you only want file logs.
    ]
)

# --- ThreadPool Settings ---
MAX_WORKERS = 2

# --- File Extension ---
FILE_EXTENSION = ".json"