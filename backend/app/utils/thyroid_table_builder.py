from app.utils.thyroid_reference_ranges import (
    THYROID_REFERENCE_RANGES
)


def build_thyroid_biomarker_table(
    biomarkers: dict
):

    table = []

    for parameter, value in biomarkers.items():

        reference = (
            THYROID_REFERENCE_RANGES.get(
                parameter
            )
        )

        if not reference:

            continue

        minimum = reference["min"]

        maximum = reference["max"]

        unit = reference["unit"]

        # =========================
        # STATUS
        # =========================

        if value < minimum:

            status = "Low"

        elif value > maximum:

            status = "High"

        else:

            status = "Normal"

        # =========================
        # RANGE TEXT
        # =========================

        range_text = (
            f"{minimum} - {maximum} {unit}"
        )

        table.append({

            "parameter":
                parameter.upper(),

            "value":
                value,

            "range":
                range_text,

            "status":
                status
        })

    return table