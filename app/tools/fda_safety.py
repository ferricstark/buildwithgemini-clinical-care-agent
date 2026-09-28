"""openFDA Public Drug & Substance Safety Tool for Clinical Care Agent."""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any

def fetch_fda_label_safety_info(substance_name: str) -> Dict[str, Any]:
    """Fetches real-time drug label, purpose, and safety warning information from the U.S. FDA (openFDA) public API.

    Args:
        substance_name: Name of the active botanical or medicinal substance (e.g. 'Arnica', 'Rhus', 'Aconite', 'Calendula').

    Returns:
        Dictionary containing FDA label purpose, indications, warnings, and active ingredient details.
    """
    clean_substance = substance_name.strip()
    encoded_substance = urllib.parse.quote(f'"{clean_substance}"')
    url = f"https://api.fda.gov/drug/label.json?search=active_ingredient:{encoded_substance}&limit=1"

    # Optional API key support from environment variable
    api_key = os.environ.get("OPENFDA_API_KEY")
    if api_key:
        url += f"&api_key={api_key}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ClinicalCareAgent/1.0 (HomeopathyClinicAssistant)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                results = payload.get("results", [])
                if not results:
                    return {
                        "status": "NOT_FOUND",
                        "substance": clean_substance,
                        "message": f"No openFDA label record found for substance '{clean_substance}'.",
                    }

                label = results[0]
                return {
                    "status": "SUCCESS",
                    "substance": clean_substance,
                    "purpose": label.get("purpose", ["No purpose specified"])[0],
                    "indications": label.get("indications_and_usage", ["No indications listed"])[0],
                    "warnings": label.get("warnings", ["No explicit warnings listed"])[0],
                    "active_ingredients": label.get("active_ingredient", [clean_substance]),
                    "source": "U.S. Food and Drug Administration (openFDA) Public API",
                }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                "status": "NOT_FOUND",
                "substance": clean_substance,
                "message": f"No FDA label record found for substance '{clean_substance}'.",
            }
        return {
            "status": "ERROR",
            "substance": clean_substance,
            "error": f"HTTP {e.code}: {e.reason}",
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "substance": clean_substance,
            "error": str(e),
        }

    return {
        "status": "NOT_FOUND",
        "substance": clean_substance,
        "message": f"Could not retrieve FDA safety data for '{clean_substance}'.",
    }
