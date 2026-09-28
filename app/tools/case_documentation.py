"""Case Documentation Agent Tool for Practitioner Notes & Plan Approval."""

from typing import Dict, Any, Optional

def generate_practitioner_documentation(
    chief_complaint: str,
    history_of_present_illness: str,
    associated_symptoms: str,
    relevant_history: str,
    current_medications: str,
    practitioner_observations: str,
    clinical_plan: str,
    follow_up_date: str,
    is_practitioner_approved: bool = False,
) -> Dict[str, Any]:
    """Generates practitioner clinical documentation and case notes.

    Args:
        chief_complaint: Primary complaint.
        history_of_present_illness: Onset, duration, modalities, course.
        associated_symptoms: Accompanying complaints.
        relevant_history: Medical background and allergies.
        current_medications: Active prescriptions and supplements.
        practitioner_observations: Clinical examination notes and observations.
        clinical_plan: Prescribed or advised clinical care plan.
        follow_up_date: Next review or follow-up date.
        is_practitioner_approved: Whether the practitioner has reviewed, edited, and approved the note.

    Returns:
        Structured clinical documentation dictionary.
    """
    approval_status = "APPROVED_AND_SAVED" if is_practitioner_approved else "DRAFT_PENDING_PRACTITIONER_REVIEW"

    formatted_note = (
        "=== CLINICAL CASE NOTE ===\n"
        f"Status: {approval_status}\n"
        f"Chief Complaint: {chief_complaint}\n\n"
        f"History of Present Illness:\n{history_of_present_illness}\n\n"
        f"Associated Symptoms:\n{associated_symptoms}\n\n"
        f"Relevant History & Medications:\n- History: {relevant_history}\n- Medications: {current_medications}\n\n"
        f"Practitioner Observations:\n{practitioner_observations}\n\n"
        f"Clinical Plan:\n{clinical_plan}\n\n"
        f"Follow-Up Date: {follow_up_date}\n"
        "=========================="
    )

    return {
        "status": approval_status,
        "is_approved": is_practitioner_approved,
        "clinical_note_markdown": formatted_note,
        "details": {
            "chief_complaint": chief_complaint,
            "history": history_of_present_illness,
            "associated_symptoms": associated_symptoms,
            "relevant_history": relevant_history,
            "current_medications": current_medications,
            "practitioner_observations": practitioner_observations,
            "plan": clinical_plan,
            "follow_up_date": follow_up_date,
        }
    }
