"""Grounded Remedy Research Assistant Tool.

Maintains strict clinician autonomy boundary:
- Never auto-prescribes or orders remedies.
- Grounds results in approved clinical reference material.
- Provides match correspondence, source citations, and uncertainty indications.
"""

from typing import Dict, Any, List

# Simulated curated reference corpus (e.g. Boericke / Kent Repertory & Materia Medica entries)
REFERENCE_MATERIA_MEDICA = [
    {
        "remedy_name": "Arnica Montana",
        "source": "Boericke Materia Medica (p. 82)",
        "key_symptoms": ["soreness", "bruised feeling", "after trauma", "worse from touch", "better lying down"],
        "indications": "Produces feeling as if bruised and beaten. Useful in acute post-strain or muscular overexertion.",
    },
    {
        "remedy_name": "Rhus Toxicodendron",
        "source": "Boericke Materia Medica (p. 540)",
        "key_symptoms": ["stiffness", "joint pain", "worse first motion", "better continued motion", "better warm applications"],
        "indications": "Affects fibrous tissue, joints, tendons. Marked restlessness; stiffness relieved by motion.",
    },
    {
        "remedy_name": "Bryonia Alba",
        "source": "Boericke Materia Medica (p. 130)",
        "key_symptoms": ["dryness", "stitching pain", "worse least motion", "better rest", "better firm pressure"],
        "indications": "Excessive dryness of mucous membranes and stitching pains aggravated by motion.",
    },
    {
        "remedy_name": "Belladonna",
        "source": "Boericke Materia Medica (p. 105)",
        "key_symptoms": ["sudden onset", "throbbing", "heat", "redness", "worse noise and light"],
        "indications": "Suddenness of onset, vascular congestion, intense heat and redness.",
    },
    {
        "remedy_name": "Nux Vomica",
        "source": "Boericke Materia Medica (p. 465)",
        "key_symptoms": ["irritability", "digestive heaviness", "overwork", "chilly", "worse morning"],
        "indications": "Suited to zealous, nervous, irritable individuals with digestive sluggishness.",
    }
]

def research_remedy_reference(symptoms_list: str) -> Dict[str, Any]:
    """Queries approved homeopathic reference materials based on practitioner-entered symptoms.

    Args:
        symptoms_list: A string of key symptoms or modalities entered or validated by the practitioner.

    Returns:
        A dictionary containing relevant reference entries, symptom correspondence details,
        confidence/uncertainty metrics, and a safety boundary statement.
    """
    query_terms = [s.strip().lower() for s in symptoms_list.replace(",", " ").split() if len(s.strip()) > 2]
    matched_entries: List[Dict[str, Any]] = []

    for entry in REFERENCE_MATERIA_MEDICA:
        match_count = 0
        matching_symptoms = []
        for term in query_terms:
            for symptom in entry["key_symptoms"]:
                if term in symptom or symptom in term:
                    match_count += 1
                    matching_symptoms.append(symptom)

        if match_count > 0:
            score = min(100, int((match_count / max(1, len(entry["key_symptoms"]))) * 100))
            matched_entries.append({
                "remedy_reference": entry["remedy_name"],
                "source_citation": entry["source"],
                "key_indications": entry["indications"],
                "matching_symptoms": list(set(matching_symptoms)),
                "correspondence_score": f"{score}%",
            })

    # Sort by correspondence score
    matched_entries.sort(key=lambda x: int(x["correspondence_score"].replace("%", "")), reverse=True)

    uncertainty_note = "High symptom overlap" if len(matched_entries) == 1 else (
        "Multiple potential correspondences found — requires individualizing clinical differentiation."
        if matched_entries else "No direct keyword matches in local reference corpus. Further repertorization suggested."
    )

    return {
        "disclaimer": "SAFETY BOUNDARY: Information presented is extracted strictly from approved reference materials for practitioner review. It does NOT constitute an automated prescription or diagnostic decision.",
        "practitioner_query": symptoms_list,
        "matched_references": matched_entries,
        "uncertainty_assessment": uncertainty_note,
    }
