import re


def extract_urine_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # PROTEIN
    # =========================

    protein_match = re.search(

        r"(protein)[^\d]*([\d.]+)",

        lowered
    )

    if protein_match:

        biomarkers["protein"] = float(

            protein_match.group(2)
        )

    # =========================
    # KETONES
    # =========================

    ketones_match = re.search(

        r"(ketones)[^\d]*([\d.]+)",

        lowered
    )

    if ketones_match:

        biomarkers["ketones"] = float(

            ketones_match.group(2)
        )

    # =========================
    # PUS CELLS
    # =========================

    pus_match = re.search(

        r"(pus cells)[^\d]*([\d.]+)",

        lowered
    )

    if pus_match:

        biomarkers["pus_cells"] = float(

            pus_match.group(2)
        )

    return biomarkers