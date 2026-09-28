"""Firestore Database Integration for Clinical Care Agent.

CRITICAL DIRECTIVE: Project ID is explicitly hardcoded as a string ('qwiklabs-gcp-03-41628e12aca2')
to prevent Agent Platform deployment runtime errors where google.auth.default() returns project numbers.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from google.cloud import firestore

# Hardcoded GCP Project ID (DO NOT read from environment variables or auth defaults)
PROJECT_ID = "qwiklabs-gcp-03-41628e12aca2"
COLLECTION_NAME = "patient_cases"

def _get_firestore_client() -> firestore.Client:
    """Creates a Firestore client bound explicitly to the hardcoded project ID."""
    return firestore.Client(project=PROJECT_ID)

def seed_firestore_data() -> Dict[str, Any]:
    """Seeds the Firestore 'patient_cases' collection with initial sample records."""
    db = _get_firestore_client()
    sample_cases = [
        {
            "patient_id": "PT-1001",
            "patient_name": "Jane Doe",
            "chief_complaint": "Chronic Eczema on hands",
            "symptoms": ["itching", "redness", "dry skin", "cracking"],
            "severity": 7,
            "modalities": {
                "better_with": "cool water",
                "worse_with": "harsh soap, cold wind",
            },
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "patient_id": "PT-1002",
            "patient_name": "Robert Smith",
            "chief_complaint": "Morning joint stiffness",
            "symptoms": ["stiffness", "joint aching", "slight swelling"],
            "severity": 6,
            "modalities": {
                "better_with": "warm bath, gentle movement",
                "worse_with": "first motion, cold weather",
            },
            "status": "PRACTITIONER_REVIEWED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "patient_id": "PT-1003",
            "patient_name": "Alice Johnson",
            "chief_complaint": "Periodic migraine headache",
            "symptoms": ["throbbing pain", "nausea", "light sensitivity"],
            "severity": 8,
            "modalities": {
                "better_with": "dark room, firm pressure",
                "worse_with": "bright light, loud noise",
            },
            "status": "FOLLOW_UP_SCHEDULED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

    seeded_ids = []
    for case in sample_cases:
        doc_ref = db.collection(COLLECTION_NAME).document(case["patient_id"])
        doc_ref.set(case, merge=True)
        seeded_ids.append(case["patient_id"])

    return {
        "status": "SUCCESS",
        "project_id": PROJECT_ID,
        "collection": COLLECTION_NAME,
        "seeded_count": len(seeded_ids),
        "seeded_patient_ids": seeded_ids,
        "message": f"Successfully seeded {len(seeded_ids)} patient case records into Firestore collection '{COLLECTION_NAME}'.",
    }

def get_patient_case(patient_id: str) -> Dict[str, Any]:
    """Retrieves a single patient case record from Firestore by patient_id.

    Args:
        patient_id: The unique patient identifier (e.g. 'PT-1001').

    Returns:
        The patient case record or a NOT_FOUND status.
    """
    db = _get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(patient_id)
    doc = doc_ref.get()

    if doc.exists:
        return {
            "status": "FOUND",
            "patient_id": patient_id,
            "data": doc.to_dict(),
        }
    return {
        "status": "NOT_FOUND",
        "patient_id": patient_id,
        "message": f"No case record found for patient ID '{patient_id}'.",
    }

def list_patient_cases() -> Dict[str, Any]:
    """Lists all patient case records stored in the Firestore database.

    Returns:
        A dictionary containing all active patient case records.
    """
    db = _get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()
    cases = [doc.to_dict() for doc in docs]

    return {
        "status": "SUCCESS",
        "count": len(cases),
        "cases": cases,
    }

def save_patient_case(
    patient_id: str,
    patient_name: str,
    chief_complaint: str,
    symptoms: str,
    severity: int,
    modalities_better: str,
    modalities_worse: str,
    status: str = "ACTIVE",
) -> Dict[str, Any]:
    """Saves or updates a patient case record in Firestore.

    Args:
        patient_id: Unique patient identifier (e.g. 'PT-1004').
        patient_name: Patient's full name.
        chief_complaint: Main complaint description.
        symptoms: Comma-separated list of key symptoms.
        severity: Pain/distress score from 1 to 10.
        modalities_better: Factors easing symptoms.
        modalities_worse: Factors aggravating symptoms.
        status: Case status ('ACTIVE', 'PRACTITIONER_REVIEWED', 'RESOLVED').

    Returns:
        Status object confirming creation/update.
    """
    db = _get_firestore_client()
    symptoms_list = [s.strip() for s in symptoms.split(",") if s.strip()]

    now_iso = datetime.now(timezone.utc).isoformat()
    doc_ref = db.collection(COLLECTION_NAME).document(patient_id)
    existing_doc = doc_ref.get()

    created_at = existing_doc.to_dict().get("created_at", now_iso) if existing_doc.exists else now_iso

    data = {
        "patient_id": patient_id,
        "patient_name": patient_name,
        "chief_complaint": chief_complaint,
        "symptoms": symptoms_list,
        "severity": severity,
        "modalities": {
            "better_with": modalities_better,
            "worse_with": modalities_worse,
        },
        "status": status,
        "created_at": created_at,
        "updated_at": now_iso,
    }

    doc_ref.set(data, merge=True)

    return {
        "status": "SUCCESS",
        "patient_id": patient_id,
        "record": data,
        "message": f"Successfully saved case record for {patient_name} ({patient_id}) in Firestore.",
    }
