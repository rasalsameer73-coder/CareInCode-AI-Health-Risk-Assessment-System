from datetime import datetime

import app.core.database as database
from pymongo.errors import PyMongoError


db = database.get_database()
collection = db.vitals_history
memory_vitals_history = {}


def save_vitals_history(
    user_id: str,
    vitals: dict,
    analysis: dict
):
    record = {
        "user_id": user_id,
        "vitals": vitals,
        "analysis": analysis,
        "created_at": datetime.utcnow(),
    }

    try:
        result = collection.insert_one(record)
        return str(result.inserted_id)
    except PyMongoError:
        memory_vitals_history.setdefault(user_id, []).append({
            **record,
            "created_at": record["created_at"].isoformat(),
        })
        return None


def get_user_vitals_history(
    user_id: str,
):
    try:
        documents = list(collection.find({"user_id": user_id}).sort("created_at", -1))
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
        return documents
    except PyMongoError:
        return memory_vitals_history.get(user_id, [])
