"""Red-flag safety & triage screening module."""

import re
from typing import Dict, Any

RED_FLAG_PATTERNS = [
    (r"\bchest\s+pain\b|\bcrushing\s+chest\b|\bchest\s+tightness\b", "Chest Pain / Possible Cardiac Event"),
    (r"\bbreathing\s+difficulty\b|\bshortness\s+of\b|\bcannot\s+breathe\b|\bsevere\s+dyspnea\b", "Severe Respiratory Distress"),
    (r"\bloss\s+of\s+consciousness\b|\bfainted\b|\bpassed\bout\b|\bunresponsive\b", "Loss of Consciousness / Syncope"),
    (r"\bstroke\b|\bface\s+droop\b|\bsudden\s+numbness\b|\barm\s+weakness\b|\bslurred\s+speech\b", "Stroke / Acute Neurological Deficit"),
    (r"\banaphylaxis\b|\bswollen\bthroat\b|\ballergic\s+shock\b|\bcannot\s+swallow\b", "Severe Anaphylactic Reaction"),
    (r"\buncontrolled\s+bleeding\b|\bsevere\s+hemorrhage\b|\bhead\s+trauma\b", "Severe Trauma / Uncontrolled Bleeding"),
]

def screen_red_flags(patient_message: str) -> Dict[str, Any]:
    """Screens patient description for high-risk red-flag emergency symptoms.

    Args:
        patient_message: The symptom or situation description provided by the patient.

    Returns:
        A dictionary indicating whether red flags were detected, identified concerns, and emergency instructions if required.
    """
    detected_flags = []
    text_lower = patient_message.lower()

    for pattern, description in RED_FLAG_PATTERNS:
        if re.search(pattern, text_lower):
            detected_flags.append(description)

    if detected_flags:
        return {
            "is_emergency": True,
            "status": "RED_FLAG_ALERT",
            "detected_concerns": detected_flags,
            "action_required": "IMMEDIATE_EMERGENCY_EVALUATION",
            "message": (
                "🚨 EMERGENCY NOTICE: Your description includes symptoms that require immediate medical evaluation "
                f"({', '.join(detected_flags)}). Please call emergency services (e.g. 911) or proceed immediately "
                "to the nearest hospital Emergency Department. Do not delay evaluation for a routine consultation."
            ),
        }

    return {
        "is_emergency": False,
        "status": "CLEAR",
        "message": "No immediate red-flag emergency criteria detected. Safe to proceed with standard intake.",
    }
