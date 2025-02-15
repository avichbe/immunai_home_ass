#!/usr/bin/env python3
import os
import json
import logging
import config
import pipelines_bl
from typing import Optional

from pydantic import BaseModel, ValidationError

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

#region pydantic

class HypothesisDetails(BaseModel):
    num_in_vivo: int
    num_neuron: int
    num_other: int
    neuron_avg: Optional[float]
    other_avg: Optional[float]

class HypothesisResult(BaseModel):
    hypothesis_valid: bool
    details: HypothesisDetails

#endregion

STAGE2_DIR = config.STAGE2_DIR

# --- Helper Function (also used in tests) ---

def recalculate_summary_from_dir(directory: str) -> str:
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
            data = pipelines_bl.read_json_data(path)
            try:
                result = HypothesisResult.model_validate(data)
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
