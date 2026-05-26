from datetime import datetime, timedelta, timezone

import app.core.database as database
from pymongo.errors import PyMongoError
from app.services.doctor_visit_history_service import (
    save_doctor_visit_history,
)


db = database.get_database()
collection = db.doctor_visit_prep

memory_store = {}


def generate_doctor_visit_summary(medications: list, symptoms: list):
    medication_count = len(medications)
    symptom_count = len(symptoms)

    facts = [
        f"{medication_count} medication{'s' if medication_count != 1 else ''} listed",
        f"{symptom_count} symptom log{'s' if symptom_count != 1 else ''} recorded",
    ]

    ist = timezone(timedelta(hours=5, minutes=30))
    summary_lines = [
        "Doctor Visit Preparation Summary",
        "",
        f"Generated on: {datetime.now(tz=ist).strftime('%A, %d %B %Y %H:%M IST')}",
        "",
        "Current medications:",
    ]

    if medications:
        summary_lines.extend(
            [
                f"{index + 1}. {med.get('name', 'Unknown medication')}{' - ' + med.get('dosage', '') if med.get('dosage') else ''}{' | for ' + med.get('reason', '') if med.get('reason') else ''}"
                for index, med in enumerate(medications)
            ]
        )
    else:
        summary_lines.append("None added")

    summary_lines.extend([
        "",
        "Symptom timeline:",
    ])

    if symptoms:
        sorted_symptoms = sorted(symptoms, key=lambda item: item.get("date", ""))
        summary_lines.extend(
            [
                f"{index + 1}. {item.get('date', 'Unknown date')}: {item.get('location', 'General discomfort')} - intensity {item.get('intensity', 'N/A')}/10" +
                (f" | triggers: {item.get('triggers')}" if item.get('triggers') else "") +
                (f" | notes: {item.get('notes')}" if item.get('notes') else "")
                for index, item in enumerate(sorted_symptoms)
            ]
        )
    else:
        summary_lines.append("No symptom entries added yet.")

    questions = [
        "What patterns should I keep tracking at home before the next appointment?",
    ]

    if medications:
        questions.append("Could any of my current medications be affecting these symptoms or masking them?")

    if symptoms:
        questions.append(
            "How do the symptom changes between the earliest and latest entries affect what you think is going on?"
        )

    questions.append("Are there tests, scans, or lifestyle changes I should prioritize first?")

    return {
        "headline": "A structured summary has been prepared for your consultation.",
        "facts": facts,
        "summaryText": "\n".join(summary_lines),
        "questions": questions,
    }


def get_doctor_visit_data(user_id: str):
    try:
        document = collection.find_one({"user_id": user_id})
        if not document:
            return None

        document["_id"] = str(document["_id"])
        for timestamp_key in ("created_at", "updated_at"):
            if timestamp_key in document and hasattr(document[timestamp_key], "isoformat"):
                document[timestamp_key] = document[timestamp_key].isoformat()
        return document
    except PyMongoError:
        return memory_store.get(user_id)


def save_doctor_visit_data(
    user_id: str,
    medications: list,
    symptoms: list,
    summary: dict | str | None = None
):
    generated_summary = generate_doctor_visit_summary(medications, symptoms)
    record = {
        "user_id": user_id,
        "medications": medications,
        "symptoms": symptoms,
        "summary": generated_summary,
        "updated_at": datetime.utcnow(),
    }

    try:
        collection.update_one(
            {"user_id": user_id},
            {
                "$set": record,
                "$setOnInsert": {"created_at": datetime.utcnow()},
            },
            upsert=True,
        )
        save_doctor_visit_history(user_id, medications, symptoms, generated_summary)
        return get_doctor_visit_data(user_id)
    except PyMongoError:
        fallback = {
            **record,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": record["updated_at"].isoformat(),
        }
        memory_store[user_id] = fallback
        return fallback
