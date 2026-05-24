from datetime import datetime

import app.core.database as database
from pymongo.errors import PyMongoError


db = database.get_database()
collection = db.doctor_visit_prep_history
memory_history = {}


def save_doctor_visit_history(
    user_id: str,
    medications: list,
    symptoms: list,
    summary: dict | str | None = None,
):
    record = {
        "user_id": user_id,
        "medications": medications,
        "symptoms": symptoms,
        "summary": summary,
        "created_at": datetime.utcnow(),
    }

    try:
        collection.insert_one(record)
        return str(record["created_at"])
    except PyMongoError:
        memory_history.setdefault(user_id, []).insert(0, {
            **record,
            "created_at": record["created_at"].isoformat(),
        })
        return None


def get_doctor_visit_history(user_id: str):
    try:
        documents = list(collection.find({"user_id": user_id}).sort("created_at", -1))
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
        return documents
    except PyMongoError:
        return memory_history.get(user_id, [])
