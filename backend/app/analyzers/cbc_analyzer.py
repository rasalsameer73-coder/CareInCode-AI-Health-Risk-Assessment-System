def analyze_cbc_biomarkers(
    biomarkers: dict
):

    risks = []

    insights = []

    evidence = []

    next_steps = []

    doctor_questions = []

    health_score = 100

    # =========================
    # HEMOGLOBIN
    # =========================

    hemoglobin = biomarkers.get(
        "hemoglobin"
    )

    if hemoglobin is not None:

        evidence.append(
            f"Hemoglobin: {hemoglobin}"
        )

        if hemoglobin < 13:

            risks.append({

                "type":
                    "Low Hemoglobin",

                "severity":
                    "moderate",

                "reason":
                    "Hemoglobin appears below common reference ranges."
            })

            insights.append(
                "Hemoglobin levels appear lower than expected."
            )

            doctor_questions.extend([

                "Could this indicate anemia?",

                "Should iron studies be performed?",

                "Would vitamin B12 or folate testing help?"
            ])

            next_steps.append(
                "Discuss low hemoglobin findings with your doctor."
            )

            health_score -= 15

        else:

            insights.append(
                "Hemoglobin is within common reference ranges."
            )

    # =========================
    # WBC
    # =========================

    wbc = biomarkers.get(
        "wbc"
    )

    if wbc is not None:

        evidence.append(
            f"WBC: {wbc}"
        )

        if wbc > 11000:

            risks.append({

                "type":
                    "Elevated WBC",

                "severity":
                    "moderate",

                "reason":
                    "White blood cell count appears elevated."
            })

            insights.append(
                "Elevated WBC may reflect inflammation or infection."
            )

            next_steps.append(
                "Monitor for signs of infection or inflammation."
            )

            health_score -= 10

        elif wbc < 4000:

            risks.append({

                "type":
                    "Low WBC",

                "severity":
                    "moderate",

                "reason":
                    "White blood cell count appears below common ranges."
            })

            insights.append(
                "Low WBC may require clinical evaluation."
            )

            health_score -= 10

    # =========================
    # PLATELETS
    # =========================

    platelets = biomarkers.get(
        "platelets"
    )

    if platelets is not None:

        evidence.append(
            f"Platelets: {platelets}"
        )

        if platelets < 150000:

            risks.append({

                "type":
                    "Low Platelets",

                "severity":
                    "moderate",

                "reason":
                    "Platelet count appears below common reference ranges."
            })

            insights.append(
                "Platelet levels are lower than expected."
            )

            next_steps.append(
                "Discuss platelet levels with your healthcare provider."
            )

            health_score -= 10

    # =========================
    # PCV
    # =========================

    pcv = biomarkers.get(
        "pcv"
    )

    if pcv is not None:

        evidence.append(
            f"PCV: {pcv}"
        )

        if pcv > 50:

            risks.append({

                "type":
                    "Elevated PCV",

                "severity":
                    "low",

                "reason":
                    "Packed Cell Volume appears elevated."
            })

            insights.append(
                "Elevated PCV may require clinical correlation."
            )

            health_score -= 5

    # =========================
    # DETERMINE RISK LEVEL
    # =========================

    risk_level = "low"

    for risk in risks:

        severity = risk.get(
            "severity",
            "low"
        )

        if severity == "high":

            risk_level = "high"
            break

        elif severity == "moderate":

            risk_level = "moderate"

    # =========================
    # SUMMARY
    # =========================

    if risks:

        summary = (
            "CBC analysis detected some parameters "
            "outside common reference ranges."
        )

    else:

        summary = (
            "CBC parameters appear largely within "
            "common reference ranges."
        )

    # =========================
    # FINAL RESPONSE
    # =========================

    return {

        "summary":
            summary,

        "risk_level":
            risk_level,

        "risk_indicators":
            risks,

        "insights":
            insights,

        "evidence":
            evidence,

        "doctor_questions":
            doctor_questions,

        "next_steps":
            next_steps,

        "health_score":
            max(health_score, 0)
    }