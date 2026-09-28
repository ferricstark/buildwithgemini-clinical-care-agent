# Project Brief: Homeopathy Clinic AI Assistant (`clinical-care-agent`)

## Overview
A stateful clinical agent for patient intake, red-flag emergency triage, practitioner documentation, grounded remedy research, appointment scheduling, and longitudinal follow-up tracking.

## Database Collection: `patient_cases`
Backend storage in Google Cloud Firestore storing structured patient clinical cases.

### Collection Schema
- `patient_id` (string): Unique identifier for patient (e.g., `PT-1001`).
- `patient_name` (string): Patient's full name.
- `chief_complaint` (string): Primary complaint (e.g., "Chronic Eczema on hands").
- `symptoms` (list of strings): List of reported key symptoms.
- `severity` (integer): Pain or distress scale from 1 (mild) to 10 (severe).
- `modalities` (map): `better_with` and `worse_with` environmental/physical factors.
- `status` (string): Case state (`ACTIVE`, `PRACTITIONER_REVIEWED`, `FOLLOW_UP_SCHEDULED`, `RESOLVED`).
- `created_at` (string): ISO timestamp of case creation.
- `updated_at` (string): ISO timestamp of last case update.

## Firestore Project ID
Hardcoded GCP Project ID: `"qwiklabs-gcp-03-41628e12aca2"`
