#!/usr/bin/env python3
import os
import json
import logging
import threading
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydantic import BaseModel, ValidationError

logging.basicConfig(level=logging.INFO, format='[Step3] %(asctime)s - %(levelname)s - %(message)s')

# --- Pydantic Models ---

class HypothesisDetails(BaseModel):
    num_in_vivo: int
    num_neuron: int
    num_other: int
    neuron_avg: Optional[float]
    other_avg: Optional[float]

class HypothesisResult(BaseModel):
    hypothesis_valid: bool
    details: HypothesisDetails

STAGE2_DIR = "stage2_data"

# --- Helper Function (also used in tests) ---

def recalculate_summary_from_dir(directory: str) -> str:
    """
    Read all stage2 JSON files from the given directory, validate their content, and calculate
    the overall percentage of experiments where the hypothesis was validated.
    Returns the summary string.
    """
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.json')]
        if not files:
            logging.info("No stage2 files to process for summary.")
            summary = "hypothesis is true for: 0.00%"
            print(summary)
            return summary
        total = 0
        valid_count = 0
        for filename in files:
            path = os.path.join(directory, filename)
            with open(path, 'r') as f:
                data = json.load(f)
            try:
                result = HypothesisResult.parse_obj(data)
                total += 1
                if result.hypothesis_valid:
                    valid_count += 1
            except ValidationError as e:
                logging.error(f"Validation error in stage2 file {filename}: {e}")
        percentage = (valid_count / total * 100) if total > 0 else 0
        summary = f"hypothesis is true for: {percentage:.2f}%"
        print(summary)
        logging.info(summary)
        return summary
    except Exception as e:
        logging.exception(f"Failed to recalculate summary: {e}")
        return "Error in calculating summary"

# --- Filesystem Event Handler for Step 3 ---

# class Step3Handler(FileSystemEventHandler):
#     def on_created(self, event):
#         if event.is_directory:
#             return
#         if event.src_path.endswith('.json'):
#             logging.info(f"New stage2 file detected: {event.src_path}. Recalculating hypothesis summary...")
#             recalculate_summary_from_dir(STAGE2_DIR)

# # --- Main Function to Watch the Directory ---

# def main():
#     event_handler = Step3Handler()
#     observer = Observer()
#     observer.schedule(event_handler, path=STAGE2_DIR, recursive=False)
#     observer.start()
#     logging.info(f"Watching for new files in {STAGE2_DIR} for global summary...")
#     try:
#         while True:
#             threading.Event().wait(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# if __name__ == "__main__":
#     main()
