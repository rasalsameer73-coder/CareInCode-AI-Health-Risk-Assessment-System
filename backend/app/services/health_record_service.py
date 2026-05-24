from datetime import datetime

import app.core.database as database

from app.services.encryption_service import (
    encrypt_data,
    decrypt_data
)

db = database.get_database()

collection = db.health_records


def save_health_record_db(
    user_id: str,
    report_text: str,
    analysis: dict,
    file_name: str | None = None
):
    encrypted_report = encrypt_data(report_text)

    document = {
        "user_id": user_id,
        "report_text": encrypted_report,
        "analysis": analysis,
        "file_name": file_name,
        "created_at": datetime.utcnow(),
    }

    try:
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception:
        return None


def get_user_records(
    user_id: str
):
    records = list(
        collection.find({
            "user_id": user_id
        })
    )

    for record in records:
        record["report_text"] = decrypt_data(record["report_text"])
        record["_id"] = str(record["_id"])

    return records