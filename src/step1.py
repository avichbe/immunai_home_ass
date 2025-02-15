import logging
from typing import List
from datetime import datetime
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
            trimmed.append(trimmed_entry.model_dump())
        except ValidationError as e:
            logger.error(f"Validation error for entry: {e}. Problematic row: {entry_dict}. Skipping entry.")
    return trimmed
