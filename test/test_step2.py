import pytest
from src.step2 import validate_hypothesis

def test_validate_hypothesis_true():
    # Here, Neuron entries have a higher average response than non-Neuron entries.
    trimmed_data = [
        {"cell_response": 10.0, "cell_type": "Neuron", "environment": "In vivo"},
        {"cell_response": 12.0, "cell_type": "Neuron", "environment": "In vivo"},
        {"cell_response": 5.0, "cell_type": "Astrocyte", "environment": "In vivo"},
        {"cell_response": 6.0, "cell_type": "Astrocyte", "environment": "In vivo"}
    ]
    result = validate_hypothesis(trimmed_data)
    assert result["hypothesis_valid"] is True

def test_validate_hypothesis_false():
    # Here, the non-Neuron entries have a higher average response.
    trimmed_data = [
        {"cell_response": 5.0, "cell_type": "Neuron", "environment": "In vivo"},
        {"cell_response": 6.0, "cell_type": "Neuron", "environment": "In vivo"},
        {"cell_response": 8.0, "cell_type": "Astrocyte", "environment": "In vivo"},
        {"cell_response": 9.0, "cell_type": "Astrocyte", "environment": "In vivo"}
    ]
    result = validate_hypothesis(trimmed_data)
    assert result["hypothesis_valid"] is False