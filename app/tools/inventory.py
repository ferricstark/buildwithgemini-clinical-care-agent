"""Clinic Pharmacy Remedy Inventory Tool for Clinical Care Agent."""

from typing import Dict, Any, Optional

# Minimal in-memory inventory database for clinic pharmacy
REMEDY_INVENTORY_CATALOG = {
    "rhus toxicodendron": {
        "remedy_name": "Rhus Toxicodendron",
        "stock": {
            "6C": {"quantity": 15, "form": "globule pills", "status": "IN_STOCK"},
            "30C": {"quantity": 42, "form": "globule pills", "status": "IN_STOCK"},
            "200C": {"quantity": 8, "form": "liquid dilution", "status": "LOW_STOCK"},
            "1M": {"quantity": 0, "form": "globule pills", "status": "OUT_OF_STOCK"},
        },
    },
    "arnica montana": {
        "remedy_name": "Arnica Montana",
        "stock": {
            "6C": {"quantity": 20, "form": "globule pills", "status": "IN_STOCK"},
            "30C": {"quantity": 50, "form": "globule pills", "status": "IN_STOCK"},
            "200C": {"quantity": 18, "form": "globule pills", "status": "IN_STOCK"},
            "1M": {"quantity": 5, "form": "liquid dilution", "status": "LOW_STOCK"},
        },
    },
    "nux vomica": {
        "remedy_name": "Nux Vomica",
        "stock": {
            "30C": {"quantity": 30, "form": "globule pills", "status": "IN_STOCK"},
            "200C": {"quantity": 12, "form": "globule pills", "status": "IN_STOCK"},
        },
    },
    "pulsatilla": {
        "remedy_name": "Pulsatilla",
        "stock": {
            "30C": {"quantity": 25, "form": "globule pills", "status": "IN_STOCK"},
            "200C": {"quantity": 4, "form": "liquid dilution", "status": "LOW_STOCK"},
        },
    },
    "bryonia alba": {
        "remedy_name": "Bryonia Alba",
        "stock": {
            "30C": {"quantity": 19, "form": "globule pills", "status": "IN_STOCK"},
            "200C": {"quantity": 0, "form": "globule pills", "status": "OUT_OF_STOCK"},
        },
    },
}

def check_remedy_inventory(remedy_name: str, potency: Optional[str] = None) -> Dict[str, Any]:
    """Checks clinic pharmacy stock availability for a specific homeopathy remedy and potency.

    Args:
        remedy_name: Name of the homeopathy remedy (e.g., 'Rhus Toxicodendron' or 'Arnica').
        potency: Optional potency strength (e.g., '30C', '200C', '6C', '1M').

    Returns:
        Dictionary containing stock levels, availability status, and dosage form.
    """
    query = remedy_name.lower().strip()
    matched_key = None

    for key in REMEDY_INVENTORY_CATALOG:
        if query in key or key in query:
            matched_key = key
            break

    if not matched_key:
        return {
            "status": "NOT_FOUND",
            "query": remedy_name,
            "message": f"Remedy '{remedy_name}' was not found in the clinic pharmacy inventory catalog.",
        }

    remedy_info = REMEDY_INVENTORY_CATALOG[matched_key]
    stock_data = remedy_info["stock"]

    if potency:
        potency_clean = potency.upper().strip()
        if potency_clean in stock_data:
            details = stock_data[potency_clean]
            return {
                "status": "SUCCESS",
                "remedy_name": remedy_info["remedy_name"],
                "potency": potency_clean,
                "quantity": details["quantity"],
                "form": details["form"],
                "availability": details["status"],
            }
        return {
            "status": "POTENCY_NOT_AVAILABLE",
            "remedy_name": remedy_info["remedy_name"],
            "requested_potency": potency_clean,
            "available_potencies": list(stock_data.keys()),
            "message": f"Potency '{potency_clean}' for '{remedy_info['remedy_name']}' is not available in pharmacy stock.",
        }

    return {
        "status": "SUCCESS",
        "remedy_name": remedy_info["remedy_name"],
        "stock_overview": stock_data,
    }
