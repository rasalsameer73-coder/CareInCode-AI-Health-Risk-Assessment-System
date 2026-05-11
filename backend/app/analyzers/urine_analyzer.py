def analyze_urine_biomarkers(
    biomarkers: dict
):

    risk_indicators = []

    insights = []

    evidence = []

    doctor_questions = []

    next_steps = []

    health_score = 100

    risk_level = "low"

    # =========================
    # PROTEIN
    # =========================

    protein = biomarkers.get(
        "protein"
    )

    if protein is not None:

        evidence.append(
            f"Protein: {protein}"
        )

        if protein > 15:

            risk_indicators.append({

                "type":
                    "Elevated Urine Protein",

                "severity":
                    "moderate"
            })

            insights.append(
                "Protein appears elevated in urine."
            )

            next_steps.append(
                "Discuss kidney or urinary health with your doctor."
            )

            health_score -= 12

            risk_level = "moderate"

    # =========================
    # KETONES
    # =========================

    ketones = biomarkers.get(
        "ketones"
    )

    if ketones is not None:

        evidence.append(
            f"Ketones: {ketones}"
        )

        if ketones > 3:

            risk_indicators.append({

                "type":
                    "Elevated Ketones",

                "severity":
                    "moderate"
            })

            insights.append(
                "Ketones appear elevated in urine."
            )

            next_steps.append(
                "Discuss possible metabolic causes with your doctor."
            )

            health_score -= 10

    # =========================
    # PUS CELLS
    # =========================

    pus_cells = biomarkers.get(
        "pus_cells"
    )

    if pus_cells is not None:

        evidence.append(
            f"Pus Cells: {pus_cells}"
        )

        if pus_cells > 5:

            risk_indicators.append({

                "type":
                    "Elevated Pus Cells",

                "severity":
                    "moderate"
            })

            insights.append(
                "Pus cells appear elevated and may indicate urinary tract irritation or infection."
            )

            next_steps.append(
                "Discuss possible urinary infection evaluation with your doctor."
            )

            health_score -= 15

            risk_level = "moderate"

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    doctor_questions.extend([

        "Should urine testing be repeated?",

        "Could dehydration affect these results?",

        "Are additional kidney or urinary investigations needed?",

        "Could symptoms indicate urinary tract infection?"
    ])

    # =========================
    # MINIMUM SCORE
    # =========================

    if health_score < 0:

        health_score = 0

    # =========================
    # SUMMARY
    # =========================

    if risk_indicators:

        summary = (
            "Urine biomarkers show some "
            "values outside common reference ranges."
        )

    else:

        summary = (
            "Urine biomarkers appear "
            "within common reference ranges."
        )

    return {

        "summary":
            summary,

        "risk_level":
            risk_level,

        "risk_indicators":
            risk_indicators,

        "insights":
            insights,

        "evidence":
            evidence,

        "doctor_questions":
            doctor_questions,

        "next_steps":
            list(set(next_steps)),

        "health_score":
            health_score
    }