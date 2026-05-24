import re


def extract_kidney_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # CREATININE
    # =========================

    creatinine_match = re.search(

        r"(creatinine)[^\d]*([\d.]+)",

        lowered
    )

    if creatinine_match:

        biomarkers["creatinine"] = float(

            creatinine_match.group(2)
        )

    # =========================
    # UREA
    # =========================

    urea_match = re.search(

        r"(urea)[^\d]*([\d.]+)",

        lowered
    )

    if urea_match:

        biomarkers["urea"] = float(

            urea_match.group(2)
        )

    # =========================
    # BUN
    # =========================

    bun_match = re.search(

        r"(bun)[^\d]*([\d.]+)",

        lowered
    )

    if bun_match:

        biomarkers["bun"] = float(

            bun_match.group(2)
        )

    # =========================
    # eGFR
    # =========================

    egfr_match = re.search(

        r"(egfr)[^\d]*([\d.]+)",

        lowered
    )

    if egfr_match:

        biomarkers["egfr"] = float(

            egfr_match.group(2)
        )

    return biomarkers