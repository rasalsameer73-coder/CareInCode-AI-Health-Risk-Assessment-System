def compare_urine_reports(
    previous: dict,
    current: dict
):

    trends = []

    parameters = [

        "protein",

        "ketones",

        "pus_cells"
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
        # LOWER IS BETTER
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