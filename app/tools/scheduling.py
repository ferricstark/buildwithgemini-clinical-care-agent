"""Appointment Scheduling Agent Tool."""

import uuid
from typing import Dict, Any, List

# Simulated slot store
AVAILABLE_SLOTS = [
    {"slot_id": "slot-1", "date": "Next Saturday", "time": "2:00 PM - 2:30 PM", "practitioner": "Dr. Smith", "status": "AVAILABLE"},
    {"slot_id": "slot-2", "date": "Next Saturday", "time": "3:00 PM - 3:30 PM", "practitioner": "Dr. Smith", "status": "AVAILABLE"},
    {"slot_id": "slot-3", "date": "Next Saturday", "time": "4:00 PM - 4:30 PM", "practitioner": "Dr. Smith", "status": "AVAILABLE"},
    {"slot_id": "slot-4", "date": "Next Monday", "time": "10:00 AM - 10:30 AM", "practitioner": "Dr. Patel", "status": "AVAILABLE"},
    {"slot_id": "slot-5", "date": "Next Monday", "time": "11:00 AM - 11:30 AM", "practitioner": "Dr. Patel", "status": "AVAILABLE"},
]

BOOKINGS: List[Dict[str, Any]] = []

def check_availability(preferred_day_time: str) -> Dict[str, Any]:
    """Checks practitioner appointment slot availability.

    Args:
        preferred_day_time: User's desired timing (e.g. 'Next Saturday afternoon' or 'Next Monday morning').

    Returns:
        Available slots matching criteria.
    """
    pref_lower = preferred_day_time.lower()
    matching_slots = []
    for slot in AVAILABLE_SLOTS:
        if slot["status"] == "AVAILABLE":
            if ("saturday" in pref_lower and "saturday" in slot["date"].lower()) or \
               ("monday" in pref_lower and "monday" in slot["date"].lower()) or \
               ("afternoon" in pref_lower and ("pm" in slot["time"].lower() or "2:" in slot["time"] or "3:" in slot["time"])) or \
               ("morning" in pref_lower and "am" in slot["time"].lower()):
                matching_slots.append(slot)

    if not matching_slots:
        matching_slots = [s for s in AVAILABLE_SLOTS if s["status"] == "AVAILABLE"]

    return {
        "search_preference": preferred_day_time,
        "available_slots": matching_slots,
    }

def book_appointment(
    patient_name: str,
    slot_id: str,
    appointment_type: str = "New Consultation",
    notes: str = "",
) -> Dict[str, Any]:
    """Books or schedules an appointment for a patient.

    Args:
        patient_name: Patient's name.
        slot_id: The slot ID selected from available slots (e.g. 'slot-1').
        appointment_type: 'New Consultation' or 'Follow-up'.
        notes: Special notes for the booking.

    Returns:
        Booking confirmation object.
    """
    slot = next((s for s in AVAILABLE_SLOTS if s["slot_id"] == slot_id), None)
    if not slot:
        return {"status": "ERROR", "message": f"Slot ID '{slot_id}' not found."}
    if slot["status"] != "AVAILABLE":
        return {"status": "ERROR", "message": f"Slot ID '{slot_id}' is no longer available."}

    slot["status"] = "BOOKED"
    booking_id = f"APT-{uuid.uuid4().hex[:6].upper()}"
    booking_record = {
        "booking_id": booking_id,
        "patient_name": patient_name,
        "date": slot["date"],
        "time": slot["time"],
        "practitioner": slot["practitioner"],
        "appointment_type": appointment_type,
        "notes": notes,
        "status": "CONFIRMED",
        "reminder_status": "SCHEDULED_24H_PRIOR",
    }
    BOOKINGS.append(booking_record)
    return {
        "status": "SUCCESS",
        "booking": booking_record,
        "message": f"Appointment successfully booked for {patient_name} with {slot['practitioner']} on {slot['date']} at {slot['time']}.",
    }

def reschedule_or_cancel(booking_id: str, action: str, new_slot_id: str = "") -> Dict[str, Any]:
    """Reschedules or cancels an existing appointment.

    Args:
        booking_id: The booking ID (e.g. 'APT-A1B2C3').
        action: 'RESCHEDULE' or 'CANCEL'.
        new_slot_id: Required if action is 'RESCHEDULE'.

    Returns:
        Status update object.
    """
    booking = next((b for b in BOOKINGS if b["booking_id"] == booking_id), None)
    if not booking:
        return {"status": "ERROR", "message": f"Booking ID '{booking_id}' not found."}

    if action.upper() == "CANCEL":
        booking["status"] = "CANCELLED"
        return {"status": "SUCCESS", "message": f"Booking '{booking_id}' has been cancelled."}

    if action.upper() == "RESCHEDULE":
        if not new_slot_id:
            return {"status": "ERROR", "message": "new_slot_id is required for rescheduling."}
        res_result = book_appointment(booking["patient_name"], new_slot_id, booking["appointment_type"], "Rescheduled")
        if res_result["status"] == "SUCCESS":
            booking["status"] = "RESCHEDULED"
            return {
                "status": "SUCCESS",
                "old_booking_id": booking_id,
                "new_booking": res_result["booking"],
                "message": f"Booking '{booking_id}' successfully rescheduled.",
            }
        return res_result

    return {"status": "ERROR", "message": f"Unknown action '{action}'."}
