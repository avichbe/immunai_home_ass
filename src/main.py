import os
import json
import time
import logging
import config
import pipelines_bl as bl 

from pipeline_utils import PipelineOrchestrator
from pipe1 import extract_trimmed_data
from pipe2 import validate_hypothesis
from pipe3 import recalculate_summary_from_dir

# --- Logging Setup ---
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger("Orchestrator")

# # --- Processing Callback Functions ---
# def process_raw_file(filepath):
#     """
#     Step 1: Reads a raw JSON file, extracts the trimmed data, and writes it to the stage1 directory.
#     """
#     try:
#         with open(filepath, 'r') as f:
#             raw_data = json.load(f)
#         logger.info(f"Processing raw file {filepath} with {len(raw_data)} entries.")
#         trimmed_data = extract_trimmed_data(raw_data)
#         filename = os.path.basename(filepath)
#         output_path = os.path.join(config.STAGE1_DIR, filename)
#         with open(output_path, 'w') as f_out:
#             json.dump(trimmed_data, f_out, indent=2)
#         logger.info(f"Wrote trimmed data to {output_path}.")
#     except Exception as e:
#         logger.exception(f"Error processing raw file {filepath}: {e}")

# def process_stage1_file(filepath):
#     """
#     Step 2: Reads a stage1 file, validates the hypothesis, and writes the result to the stage2 directory.
#     """
#     try:
#         with open(filepath, 'r') as f:
#             trimmed_data = json.load(f)
#         logger.info(f"Processing stage1 file {filepath} with {len(trimmed_data)} entries.")
#         result = validate_hypothesis(trimmed_data)
#         filename = os.path.basename(filepath)
#         output_path = os.path.join(config.STAGE2_DIR, filename)
#         with open(output_path, 'w') as f_out:
#             json.dump(result, f_out, indent=2)
#         logger.info(f"Wrote hypothesis validation result to {output_path}.")
#     except Exception as e:
#         logger.exception(f"Error processing stage1 file {filepath}: {e}")

# def process_stage2_file(filepath):
#     """
#     Step 3: Processes a stage2 file by recalculating and printing the global summary.
#     """
#     try:
#         logger.info(f"Processing stage2 file {filepath}. Recalculating global summary.")
#         recalculate_summary_from_dir(config.STAGE2_DIR)
#     except Exception as e:
#         logger.exception(f"Error processing stage2 file {filepath}: {e}")

def main():
    orchestrator = PipelineOrchestrator(
        raw_dir=config.RAW_EXPERIMENT_DIR,
        stage1_dir=config.STAGE1_DIR,
        stage2_dir=config.STAGE2_DIR,
        process_raw_callback=bl.process_raw_file,
        process_stage1_callback=bl.process_stage1_file,
        process_stage2_callback=bl.process_stage2_file,
    )
    orchestrator.run()
    logger.info("All pipeline watchers started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    finally:
        orchestrator.stop_all()

if __name__ == "__main__":
    main()