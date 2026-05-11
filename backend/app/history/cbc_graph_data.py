def build_cbc_graph_data(
    history: list
):

    graph_data = {

        "hemoglobin": [],

        "wbc": [],

        "platelets": [],

        "pcv": []
    }

    for index, record in enumerate(history):

        biomarkers = record.get(
            "biomarkers",
            {}
        )

        for parameter in graph_data.keys():

            value = biomarkers.get(
                parameter
            )

            if value is not None:

                graph_data[
                    parameter
                ].append({

                    "report":
                        index + 1,

                    "value":
                        value
                })

    return graph_data