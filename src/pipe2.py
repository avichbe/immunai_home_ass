#!/usr/bin/env python3
import os
import json
import logging
import threading
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydantic import BaseModel, ValidationError

# --- Pydantic Models ---

class ExperimentTrimmed(BaseModel):
    cell_response: float
    cell_type: str
    environment: str

class HypothesisDetails(BaseModel):
    num_in_vivo: int
    num_neuron: int
    num_other: int
    neuron_avg: Optional[float]
    other_avg: Optional[float]

class HypothesisResult(BaseModel):
    hypothesis_valid: bool
    details: HypothesisDetails

# --- Directories and Logging Setup ---

STAGE1_DIR = "stage1_data"
STAGE2_DIR = "stage2_data"
os.makedirs(STAGE2_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='[Step2] %(asctime)s - %(levelname)s - %(message)s')

# --- Helper Function (also used in tests) ---

def validate_hypothesis(trimmed_data: List[dict]) -> dict:
    """
    For the given trimmed experiment entries, filter for those run "In vivo", 
    group by whether the cell type is "Neuron" or not, compute the average cell_response 
    for each group, and then decide if the hypothesis is validated (i.e. Neuron average > other average).
    """
    # Validate each entry using pydantic.
    valid_entries = []
    for entry in trimmed_data:
        try:
            validated_entry = ExperimentTrimmed.parse_obj(entry)
            valid_entries.append(validated_entry)
        except ValidationError as e:
            logging.error(f"Validation error in trimmed data: {e}. Skipping entry.")
    
    in_vivo_entries = [e for e in valid_entries if e.environment == "In vivo"]
    neuron_entries = [e for e in in_vivo_entries if e.cell_type == "Neuron"]
    other_entries = [e for e in in_vivo_entries if e.cell_type != "Neuron"]

    def average_response(entries):
        return sum(e.cell_response for e in entries) / len(entries) if entries else None

    neuron_avg = average_response(neuron_entries)
    other_avg = average_response(other_entries)

    # Both groups must be present to validate the hypothesis.
    valid = (neuron_avg is not None and other_avg is not None and neuron_avg > other_avg)
    
    details = HypothesisDetails(
        num_in_vivo=len(in_vivo_entries),
        num_neuron=len(neuron_entries),
        num_other=len(other_entries),
        neuron_avg=neuron_avg,
        other_avg=other_avg
    )
    
    result = HypothesisResult(
        hypothesis_valid=valid,
        details=details
    )
    return result.dict()

# # --- Filesystem Event Handler for Step 2 ---

# class Step2Handler(FileSystemEventHandler):
#     def __init__(self, executor):
#         super().__init__()
#         self.executor = executor
    
#     def on_created(self, event):
#         if event.is_directory:
#             return
#         if event.src_path.endswith('.json'):
#             logging.info(f"New stage1 file detected: {event.src_path}")
#             self.executor.submit(self.process_file, event.src_path)
    
#     def process_file(self, filepath):
#         try:
#             with open(filepath, 'r') as f:
#                 trimmed_data = json.load(f)
#             logging.info(f"Processing {len(trimmed_data)} trimmed entries from {filepath}")
#             result = validate_hypothesis(trimmed_data)
#             filename = os.path.basename(filepath)
#             output_path = os.path.join(STAGE2_DIR, filename)
#             with open(output_path, 'w') as f_out:
#                 json.dump(result, f_out, indent=2)
#             logging.info(f"Step 2 output written to: {output_path}")
#         except Exception as e:
#             logging.exception(f"Failed processing file {filepath}: {e}")

# # --- Main Function to Watch the Directory ---

# def main():
#     executor = ThreadPoolExecutor(max_workers=4)
#     event_handler = Step2Handler(executor)
#     observer = Observer()
#     observer.schedule(event_handler, path=STAGE1_DIR, recursive=False)
#     observer.start()
#     logging.info(f"Watching for new files in {STAGE1_DIR} ...")
#     try:
#         while True:
#             threading.Event().wait(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#     executor.shutdown()

# if __name__ == "__main__":
#     main()
