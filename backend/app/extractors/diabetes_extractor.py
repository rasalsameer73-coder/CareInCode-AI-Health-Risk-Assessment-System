import re


def extract_diabetes_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # HbA1c
    # =========================

    hba1c_match = re.search(

        r"(hba1c|glycated hemoglobin)[^\d]*([\d.]+)",

        lowered
    )

    if hba1c_match:

        biomarkers["hba1c"] = float(

            hba1c_match.group(2)
        )

    # =========================
    # FASTING GLUCOSE
    # =========================

    fasting_match = re.search(

        r"(fasting glucose|fasting sugar|fasting blood sugar)[^\d]*([\d.]+)",

        lowered
    )

    if fasting_match:

        biomarkers["fasting_glucose"] = float(

            fasting_match.group(2)
        )

    # =========================
    # RANDOM GLUCOSE
    # =========================

    random_match = re.search(

        r"(random glucose|random sugar|blood sugar)[^\d]*([\d.]+)",

        lowered
    )

    if random_match:

        biomarkers["random_glucose"] = float(

            random_match.group(2)
        )

    return biomarkers