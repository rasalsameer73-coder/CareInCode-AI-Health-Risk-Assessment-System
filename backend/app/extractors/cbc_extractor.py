import re


def safe_extract(
    pattern: str,
    text: str
):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        try:

            return float(
                match.group(1)
            )

        except:

            return None

    return None


def extract_cbc_parameters(
    text: str
):

    extracted = {}

    # =========================
    # HEMOGLOBIN
    # =========================

    extracted["hemoglobin"] = safe_extract(

        r"hemoglobin.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # RBC
    # =========================

    extracted["rbc"] = safe_extract(

        r"rbc.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # WBC
    # =========================

    extracted["wbc"] = safe_extract(

        r"wbc.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # PCV
    # =========================

    extracted["pcv"] = safe_extract(

        r"packed cell volume.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # MCV
    # =========================

    extracted["mcv"] = safe_extract(

        r"mean corpuscular volume.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # MCH
    # =========================

    extracted["mch"] = safe_extract(

        r"\bmch\b.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # MCHC
    # =========================

    extracted["mchc"] = safe_extract(

        r"mchc.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # RDW
    # =========================

    extracted["rdw"] = safe_extract(

        r"rdw.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # PLATELETS
    # =========================

    extracted["platelets"] = safe_extract(

        r"platelet.*?([0-9]+\.?[0-9]*)",

        text
    )

    # =========================
    # REMOVE NONE VALUES
    # =========================

    cleaned = {}

    for key, value in extracted.items():

        if value is not None:

            cleaned[key] = value

    return cleaned