"""Follow-Up Agent Tool for longitudinal patient progress tracking."""

from typing import Dict, Any, Optional

def analyze_follow_up_progress(
    patient_name: str,
    previous_severity_1_to_10: int,
    current_severity_1_to_10: int,
    previous_frequency: str,
    current_frequency: str,
    new_symptoms: Optional[str] = "None",
    treatment_adherence: str = "Compliant",
    side_effects_or_adverse_events: Optional[str] = "None reported",
    additional_notes: Optional[str] = "None",
) -> Dict[str, Any]:
    """Evaluates symptom trajectory and builds a longitudinal follow-up summary.

    Args:
        patient_name: Name of the patient.
        previous_severity_1_to_10: Severity recorded at previous visit (1-10).
        current_severity_1_to_10: Severity reported today (1-10).
        previous_frequency: Symptom frequency at last visit.
        current_frequency: Symptom frequency today.
        new_symptoms: Any new complaints that emerged since last visit.
        treatment_adherence: Adherence level (e.g. 'Compliant', 'Partial', 'Missed doses').
        side_effects_or_adverse_events: Any reported side effects or reactions.
        additional_notes: Additional observations or patient comments.

    Returns:
        Structured follow-up progress assessment dictionary.
    """
    delta_severity = current_severity_1_to_10 - previous_severity_1_to_10
    if delta_severity < 0:
        overall_trend = f"IMPROVED (Severity reduced by {abs(delta_severity)} points)"
    elif delta_severity > 0:
        overall_trend = f"WORSENED (Severity increased by {delta_severity} points)"
    else:
        overall_trend = "UNCHANGED (Severity score constant)"

    summary = {
        "status": "FOLLOW_UP_ANALYSIS_COMPLETE",
        "patient": patient_name,
        "symptom_progression": {
            "previous_severity": f"{previous_severity_1_to_10}/10",
            "current_severity": f"{current_severity_1_to_10}/10",
            "severity_delta": delta_severity,
            "previous_frequency": previous_frequency,
            "current_frequency": current_frequency,
            "overall_trend": overall_trend,
        },
        "safety_and_adherence": {
            "adherence": treatment_adherence,
            "new_symptoms": new_symptoms,
            "adverse_events": side_effects_or_adverse_events,
        },
        "practitioner_summary": (
            f"Follow-up Progress for {patient_name}:\n"
            f"- Symptom Trend: {overall_trend}\n"
            f"- Previous Severity: {previous_severity_1_to_10}/10 | Current Severity: {current_severity_1_to_10}/10\n"
            f"- Frequency Shift: '{previous_frequency}' → '{current_frequency}'\n"
            f"- Treatment Adherence: {treatment_adherence}\n"
            f"- New Symptoms: {new_symptoms}\n"
            f"- Side Effects / Adverse Events: {side_effects_or_adverse_events}\n"
            f"- Notes: {additional_notes}"
        )
    }
    return summary
