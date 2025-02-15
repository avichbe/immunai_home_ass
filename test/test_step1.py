import json
import pytest
from src.step1 import extract_trimmed_data

def test_extract_trimmed_data_valid():
    raw_experiments = [
        {
            "date": "2022-04-05T10:30:00Z",
            "cell_type": {"id": 1, "name": "Neuron", "location": "Brain", "function": "Signal processing"},
            "environment": {"id": 10, "name": "In vivo", "condition": "Healthy", "medium": "Blood", "temperature": "37°C"},
            "cell_response": 9.5,
            "duration": 120,
            "treatment": "Drug A",
            "status": "Completed"
        }
    ]
    result = extract_trimmed_data(raw_experiments)
    assert len(result) == 1
    entry = result[0]
    assert entry["cell_type"] == "Neuron"
    assert entry["environment"] == "In vivo"
    assert entry["cell_response"] == 9.5

def test_extract_trimmed_data_invalid():
    raw_experiments = [
        # valid entry
        {
            "date": "2022-04-05T10:30:00Z",
            "cell_type": {"id": 1, "name": "Neuron", "location": "Brain", "function": "Signal processing"},
            "environment": {"id": 10, "name": "In vivo", "condition": "Healthy", "medium": "Blood", "temperature": "37°C"},
            "cell_response": 9.5,
            "duration": 120,
            "treatment": "Drug A",
            "status": "Completed"
        },
        # invalid entry (missing cell_response)
        {
            "date": "2022-04-05T10:30:00Z",
            "cell_type": {"id": 2, "name": "Astrocyte", "location": "Brain", "function": "Support"},
            "environment": {"id": 11, "name": "In vitro", "condition": "Healthy", "medium": "Culture", "temperature": "37°C"},
            "duration": 100,
            "treatment": "Drug B",
            "status": "Completed"
        }
    ]
    result = extract_trimmed_data(raw_experiments)
    # Only the valid entry should be returned.
    assert len(result) == 1
    assert result[0]["cell_type"] == "Neuron"
