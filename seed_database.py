#!/usr/bin/env python3
"""Standalone script to seed initial patient case items into Firestore."""

import sys
from app.tools.firestore_db import seed_firestore_data

def main():
    print("🌱 Seeding Firestore database for clinical-care-agent...")
    try:
        result = seed_firestore_data()
        print(f"✅ {result['message']}")
        print(f"   Project ID: {result['project_id']}")
        print(f"   Collection: {result['collection']}")
        print(f"   Seeded IDs: {', '.join(result['seeded_patient_ids'])}")
    except Exception as e:
        print(f"❌ Error seeding Firestore: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
