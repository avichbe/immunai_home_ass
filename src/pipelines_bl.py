import os
import json
import logging
import config
import time

from step1 import extract_trimmed_data
from step2 import validate_hypothesis
from step3 import recalculate_summary_from_dir


# --- Logging Setup ---
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger("pipeline_bl")


def read_json_data(filepath, max_retries=3, initial_delay=1):
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            start_time = time.perf_counter()
            with open(filepath, 'r') as f:
                data = json.load(f)
            elapsed = time.perf_counter() - start_time
            logger.info(f"Successfully read JSON data from {filepath} succeeded in {elapsed:.3f} seconds on attempt {attempt}.")
            return data
        except Exception as e:
            logger.exception(f"Attempt {attempt} failed to read file {filepath}: {e}")
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
    logger.error(f"All attempts failed to read file {filepath}.")
    return None

def write_json_data(data, output_path, max_retries=3, initial_delay=1):

    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            start_time = time.perf_counter()
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            elapsed = time.perf_counter() - start_time
            logger.info(f"Successfully wrote JSON data to {output_path} succeeded in {elapsed:.3f} seconds on attempt {attempt}.")
            return True
        except Exception as e:
            logger.exception(f"Attempt {attempt} failed to write file {output_path}: {e}")
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
    logger.error(f"All attempts failed to write file {output_path}.")
    return False

def process_raw_file(filepath):
    """
    Step 1: Reads a raw JSON file, extracts the trimmed data, and writes it to the stage1 directory.
    """
    try:
        raw_data = read_json_data(filepath)
        logger.info(f"Processing raw file {filepath} with {len(raw_data)} entries.")
        trimmed_data = extract_trimmed_data(raw_data)

        filename = os.path.basename(filepath)
        output_path = os.path.join(config.STAGE1_DIR, filename)

        write_json_data(trimmed_data,output_path)
        logger.info(f"Wrote trimmed data to {output_path}.")
    except Exception as e:
        logger.exception(f"Error processing raw file {filepath}: {e}")

def process_stage1_file(filepath):
    """
    Step 2: Reads a stage1 file, validates the hypothesis, and writes the result to the stage2 directory.
    """
    try:
        with open(filepath, 'r') as f:
            trimmed_data = json.load(f)
        trimmed_data = read_json_data(filepath)
        logger.info(f"Processing stage1 file {filepath} with {len(trimmed_data)} entries.")
        result = validate_hypothesis(trimmed_data)

        filename = os.path.basename(filepath)
        output_path = os.path.join(config.STAGE2_DIR, filename)

        write_json_data(result, output_path)
        logger.info(f"Wrote hypothesis validation result to {output_path}.")
    except Exception as e:
        logger.exception(f"Error processing stage1 file {filepath}: {e}")


def process_stage2_file(filepath):
    """
    Step 3: Processes a stage2 file by recalculating and printing the global summary.
    """
    try:
        logger.info(f"Processing stage2 file {filepath}. Recalculating global summary.")
        recalculate_summary_from_dir(config.STAGE2_DIR)
    except Exception as e:
        logger.exception(f"Error processing stage2 file {filepath}: {e}")