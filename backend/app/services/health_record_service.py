from datetime import datetime

import app.core.database as database

from pymongo.errors import PyMongoError

from app.services.encryption_service import (
    encrypt_data,
    decrypt_data
)

# =========================
# DATABASE
# =========================

db = database.get_database()

collection = db.health_records

# =========================
# SAVE RECORD
# =========================

def save_health_record_db(

    user_id: str,

    report_text: str,

    analysis: dict,

    file_name: str | None = None
):

    # =========================
    # ENCRYPT REPORT
    # =========================

    encrypted_report = encrypt_data(
        report_text
    )

    # =========================
    # DOCUMENT
    # =========================

    document = {

        "user_id":
            user_id,

        "report_text":
            encrypted_report,

        "analysis":
            analysis,

        # CRITICAL FOR HISTORY/TRENDS
        "biomarkers":
            analysis.get(
                "biomarkers",
                {}
            ),

        "file_name":
            file_name,

        "created_at":
            datetime.utcnow()
    }

    # =========================
    # SAVE TO MONGODB
    # =========================

    try:

        result = collection.insert_one(
            document
        )

        print(
            "Inserted:",
            result.inserted_id
        )

        return str(
            result.inserted_id
        )

    except PyMongoError as e:

        print(
            "Mongo Save Error:",
            str(e)
        )

        return None

# =========================
# GET USER RECORDS
# =========================

def get_user_records(
    user_id: str
):

    records = list(

        collection.find({

            "user_id":
                user_id

        }).sort(

            "created_at",
            1
        )
    )

    for record in records:

        # =========================
        # DECRYPT REPORT
        # =========================

        try:

            record["report_text"] = decrypt_data(
                record["report_text"]
            )

        except Exception:

            record["report_text"] = (
                "Unable to decrypt report"
            )

        record["_id"] = str(
            record["_id"]
        )

    return records