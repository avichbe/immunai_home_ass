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