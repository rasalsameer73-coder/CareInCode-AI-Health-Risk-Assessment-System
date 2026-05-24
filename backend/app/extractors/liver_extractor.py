import re


def extract_liver_parameters(
    text: str
):

    lowered = text.lower()

    biomarkers = {}

    # =========================
    # ALT
    # =========================

    alt_match = re.search(

        r"(alt)[^\d]*([\d.]+)",

        lowered
    )

    if alt_match:

        biomarkers["alt"] = float(

            alt_match.group(2)
        )

    # =========================
    # AST
    # =========================

    ast_match = re.search(

        r"(ast)[^\d]*([\d.]+)",

        lowered
    )

    if ast_match:

        biomarkers["ast"] = float(

            ast_match.group(2)
        )

    # =========================
    # BILIRUBIN
    # =========================

    bilirubin_match = re.search(

        r"(bilirubin)[^\d]*([\d.]+)",

        lowered
    )

    if bilirubin_match:

        biomarkers["bilirubin"] = float(

            bilirubin_match.group(2)
        )

    return biomarkers