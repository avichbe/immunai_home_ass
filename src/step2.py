#!/usr/bin/env python3
import os
import json
import logging
from typing import List, Optional
import config

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



STAGE1_DIR = config.STAGE1_DIR
STAGE2_DIR = config.STAGE2_DIR

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


def validate_hypothesis(trimmed_data: List[dict]) -> dict:
    # Validate each entry using pydantic.
    valid_entries = []
    for entry in trimmed_data:
        try:
            validated_entry = ExperimentTrimmed(**entry)
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
    return result.model_dump()

