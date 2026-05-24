def compare_diabetes_reports(
    previous: dict,
    current: dict
):

    trends = []

    parameters = [

        "hba1c",

        "fasting_glucose",

        "random_glucose"
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

        if current_value < previous_value:

            trends.append(

                f"{parameter.upper()} improved from "

                f"{previous_value} → "

                f"{current_value}"
            )

        elif current_value > previous_value:

            trends.append(

                f"{parameter.upper()} increased from "

                f"{previous_value} → "

                f"{current_value}"
            )

        else:

            trends.append(

                f"{parameter.upper()} remained stable "
                f"at {current_value}"
            )

    return trends