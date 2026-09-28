"""Patient Intake & Structured Case Sheet Generator."""

import json
from typing import Dict, Any, Optional

def generate_case_sheet(
    patient_name: str,
    age: int,
    contact_info: str,
    chief_complaint: str,
    onset_and_duration: str,
    severity_1_to_10: int,
    frequency: str,
    modalities_better: str,
    modalities_worse: str,
    associated_symptoms: str,
    current_medications: str,
    allergies: str,
    medical_history: str,
    lifestyle_sleep_stress: str,
    reports_or_images: Optional[str] = "None uploaded",
) -> Dict[str, Any]:
    """Generates a structured clinical intake case sheet from patient conversation data.

    Args:
        patient_name: Patient's full name.
        age: Patient's age in years.
        contact_info: Email or phone number.
        chief_complaint: Primary health issue reported.
        onset_and_duration: When symptoms began and how long they persist.
        severity_1_to_10: Subjective pain or distress score from 1 (mild) to 10 (severe).
        frequency: Constant, intermittent, periodic, etc.
        modalities_better: Factors easing symptoms (e.g. warmth, rest, cold drinks).
        modalities_worse: Factors aggravating symptoms (e.g. motion, noise, cold air).
        associated_symptoms: Related complaints (e.g. fatigue, nausea, headache).
        current_medications: Existing drugs or supplements taken.
        allergies: Known drug, food, or environmental allergies.
        medical_history: Chronic conditions or past major illnesses.
        lifestyle_sleep_stress: Sleep quality, stress levels, dietary habits.
        reports_or_images: References or descriptions of attached reports or lab images.

    Returns:
        Structured Case Sheet dictionary.
    """
    case_sheet = {
        "status": "STRUCTURED_INTAKE_COMPLETE",
        "demographics": {
            "name": patient_name,
            "age": age,
            "contact": contact_info,
        },
        "chief_complaint": {
            "primary": chief_complaint,
            "onset_duration": onset_and_duration,
            "severity": f"{severity_1_to_10}/10",
            "frequency": frequency,
        },
        "modalities": {
            "better_with": modalities_better,
            "worse_with": modalities_worse,
        },
        "associated_symptoms": associated_symptoms,
        "medical_background": {
            "current_medications": current_medications,
            "allergies": allergies,
            "past_medical_history": medical_history,
        },
        "lifestyle": lifestyle_sleep_stress,
        "attachments": reports_or_images,
    }
    return case_sheet
