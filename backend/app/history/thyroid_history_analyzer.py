def compare_thyroid_reports(
    previous: dict,
    current: dict
):

    trends = []

    parameters = [

        "tsh",

        "t3",

        "t4"
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
        # TSH LOGIC
        # =========================

        if parameter == "tsh":

            if current_value < previous_value:

                trends.append(

                    f"TSH improved from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

            elif current_value > previous_value:

                trends.append(

                    f"TSH increased from "

                    f"{previous_value} → "

                    f"{current_value}"
                )

            else:

                trends.append(
                    f"TSH remained stable at "
                    f"{current_value}"
                )

        # =========================
        # T3 / T4
        # =========================

        else:

            if current_value > previous_value:

                trends.append(

                    f"{parameter.upper()} improved from "

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