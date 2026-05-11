def compare_kidney_reports(
    previous: dict,
    current: dict
):

    trends = []

    parameters = [

        "creatinine",

        "urea",

        "bun",

        "egfr"
    ]

    for parameter in parameters:

        previous_value = previous.get(
            parameter
        )

        current_value = current.get(
            parameter
        )

        if (
            previous_value is None
            or
            current_value is None
        ):

            continue

        # =========================
        # eGFR IMPROVEMENT
        # =========================

        if parameter == "egfr":

            if current_value > previous_value:

                trends.append(

                    f"eGFR improved from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

            elif current_value < previous_value:

                trends.append(

                    f"eGFR decreased from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

            else:

                trends.append(
                    f"eGFR remained stable at "
                    f"{current_value}"
                )

        # =========================
        # OTHER PARAMETERS
        # =========================

        else:

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