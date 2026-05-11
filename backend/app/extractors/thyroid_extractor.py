import re


def extract_thyroid_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # TSH
    # =========================

    tsh_match = re.search(

        r"(tsh)[^\d]*([\d.]+)",

        lowered
    )

    if tsh_match:

        biomarkers["tsh"] = float(

            tsh_match.group(2)
        )

    # =========================
    # T3
    # =========================

    t3_match = re.search(

        r"(t3)[^\d]*([\d.]+)",

        lowered
    )

    if t3_match:

        biomarkers["t3"] = float(

            t3_match.group(2)
        )

    # =========================
    # T4
    # =========================

    t4_match = re.search(

        r"(t4)[^\d]*([\d.]+)",

        lowered
    )

    if t4_match:

        biomarkers["t4"] = float(

            t4_match.group(2)
        )

    return biomarkers