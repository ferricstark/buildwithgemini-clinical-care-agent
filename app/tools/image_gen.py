"""Image Generation and Cloud Storage Upload Tool for Clinical Care Agent."""

import uuid
from typing import Dict, Any
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# Hardcoded GCP Project ID and Cloud Storage Bucket Name
PROJECT_ID = "qwiklabs-gcp-03-41628e12aca2"
BUCKET_NAME = "clinical-care-assets-41628e"

def generate_remedy_illustration(
    remedy_name: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generates a botanical remedy illustration for patient education using gemini-3.1-flash-lite-image in the global region.

    Saves the generated image as an artifact in Playground and uploads the image bytes directly to public Cloud Storage.

    Args:
        remedy_name: Name of the homeopathy remedy or botanical plant (e.g., 'Arnica Montana', 'Rhus Tox', 'Calendula').
        tool_context: ADK ToolContext injected automatically by the framework.

    Returns:
        Dictionary containing the public Cloud Storage HTTPS URL and artifact confirmation.
    """
    clean_name = remedy_name.strip()
    prompt = (
        f"A clean, elegant botanical illustration of {clean_name} flower and medicinal plant "
        "suitable for a homeopathy medical education card. Soft studio lighting, high resolution, white background."
    )

    # 1. Generate image bytes using gemini-3.1-flash-lite-image in location='global'
    genai_client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )

    response = genai_client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    image_bytes = None
    mime_type = "image/jpeg"

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/jpeg"
                break

    if not image_bytes:
        return {
            "status": "ERROR",
            "remedy_name": clean_name,
            "message": "Failed to generate image bytes from gemini-3.1-flash-lite-image model.",
        }

    # Generate unique filename
    file_ext = "png" if "png" in mime_type else "jpg"
    filename = f"remedy_{clean_name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.{file_ext}"

    # (1) Save with tool_context.save_artifact for Playground Artifacts panel
    artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # (2) Upload image bytes directly to public Cloud Storage bucket (without writing to local file)
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "status": "SUCCESS",
        "remedy_name": clean_name,
        "filename": filename,
        "mime_type": mime_type,
        "public_url": public_url,
        "artifact_saved": True,
        "message": f"Successfully generated botanical illustration for {clean_name}, saved artifact, and published to Cloud Storage.",
    }
