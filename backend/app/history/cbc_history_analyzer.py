def compare_cbc_reports(
    previous: dict,
    current: dict
):

    trends = []

    # =========================
    # PARAMETERS TO TRACK
    # =========================

    parameters = [

        "hemoglobin",

        "wbc",

        "platelets",

        "pcv",

        "rbc",

        "mcv",

        "mch",

        "mchc",

        "rdw"
    ]

    for parameter in parameters:

        previous_value = previous.get(
            parameter
        )

        current_value = current.get(
            parameter
        )

        # =========================
        # SKIP MISSING VALUES
        # =========================

        if (
            previous_value is None
            or
            current_value is None
        ):

            continue

        # =========================
        # TREND DETECTION
        # =========================

        if current_value > previous_value:

            if parameter == "hemoglobin":

                trends.append(

                    f"Hemoglobin improved from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

            else:

                trends.append(

                    f"{parameter.upper()} increased from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

        elif current_value < previous_value:

            trends.append(

                f"{parameter.upper()} decreased from "

                f"{previous_value} → "

                f"{current_value}"
            )

        else:

            trends.append(

                f"{parameter.upper()} remained stable "
                f"at {current_value}"
            )

    return trends