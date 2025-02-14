#!/usr/bin/env python3
import os
import json
import logging
import threading
from typing import List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydantic import BaseModel, ValidationError

# Import configuration
import config

# --- Pydantic Models ---

class CellType(BaseModel):
    id: int
    name: str
    location: str
    function: str

class Environment(BaseModel):
    id: int
    name: str
    condition: str
    medium: str
    temperature: str

class ExperimentEntry(BaseModel):
    date: datetime
    cell_type: CellType
    environment: Environment
    cell_response: float
    duration: int
    treatment: str
    status: str

class ExperimentTrimmed(BaseModel):
    cell_response: float
    cell_type: str
    environment: str

# --- Logging Setup ---
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger("Step1")

# --- Helper Function (also used in tests) ---

def extract_trimmed_data(raw_experiments: List[dict]) -> List[dict]:
    """
    Validate each raw experiment entry using pydantic and extract only the fields needed 
    for the hypothesis (cell_response, cell_type name, environment name).
    """
    trimmed = []
    for entry_dict in raw_experiments:
        try:
            # Validate the raw entry.
            entry = ExperimentEntry.model_validate(entry_dict)
            # Create the trimmed version.
            trimmed_entry = ExperimentTrimmed(
                cell_response=entry.cell_response,
                cell_type=entry.cell_type.name,
                environment=entry.environment.name
            )
            trimmed.append(trimmed_entry.dict())
        except ValidationError as e:
            logger.error(f"Validation error for entry: {e}. Skipping entry.")
    return trimmed

# --- Filesystem Event Handler for Step 1 ---

class Step1Handler(FileSystemEventHandler):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(config.FILE_EXTENSION):
            logger.info(f"New raw data file detected: {event.src_path}")
            self.executor.submit(self.process_file, event.src_path)

    def process_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                experiments = json.load(f)
            logger.info(f"Processing {len(experiments)} experiment entries from {filepath}")
            trimmed_data = extract_trimmed_data(experiments)
            filename = os.path.basename(filepath)
            output_path = os.path.join(config.STAGE1_DIR, filename)
            with open(output_path, 'w') as f_out:
                json.dump(trimmed_data, f_out, indent=2)
            logger.info(f"Step 1 output written to: {output_path}")
        except Exception as e:
            logger.exception(f"Failed processing file {filepath}: {e}")

# # --- Main Function to Watch the Directory ---

# def main():
#     executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
#     event_handler = Step1Handler(executor)
#     observer = Observer()
#     observer.schedule(event_handler, path=config.RAW_EXPERIMENT_DIR, recursive=False)
#     observer.start()
#     logger.info(f"Watching for new files in {config.RAW_EXPERIMENT_DIR} ...")
#     try:
#         while True:
#             threading.Event().wait(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#     executor.shutdown()

# #run simple test
# if __name__ == "__main__":
#     main()
