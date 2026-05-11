import re


def extract_lipid_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # TOTAL CHOLESTEROL
    # =========================

    cholesterol_match = re.search(

        r"(total cholesterol|cholesterol)[^\d]*([\d.]+)",

        lowered
    )

    if cholesterol_match:

        biomarkers["cholesterol"] = float(

            cholesterol_match.group(2)
        )

    # =========================
    # HDL
    # =========================

    hdl_match = re.search(

        r"(hdl)[^\d]*([\d.]+)",

        lowered
    )

    if hdl_match:

        biomarkers["hdl"] = float(
            hdl_match.group(2)
        )

    # =========================
    # LDL
    # =========================

    ldl_match = re.search(

        r"(ldl)[^\d]*([\d.]+)",

        lowered
    )

    if ldl_match:

        biomarkers["ldl"] = float(
            ldl_match.group(2)
        )

    # =========================
    # TRIGLYCERIDES
    # =========================

    triglycerides_match = re.search(

        r"(triglycerides)[^\d]*([\d.]+)",

        lowered
    )

    if triglycerides_match:

        biomarkers["triglycerides"] = float(

            triglycerides_match.group(2)
        )

    return biomarkers