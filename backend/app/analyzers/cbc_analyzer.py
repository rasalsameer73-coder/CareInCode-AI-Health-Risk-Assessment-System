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

        if hemoglobin < 7:

            risks.append({

                "type":
                    "Critical Low Hemoglobin",

                "severity":
                    "critical",

                "reason":
                    "Hemoglobin critically low. Seek immediate medical attention."
            })

            insights.append(
                "Hemoglobin is critically low (severe anemia)."
            )

            health_score -= 30

        elif hemoglobin < 10:

            risks.append({

                "type":
                    "Severe Low Hemoglobin",

                "severity":
                    "high",

                "reason":
                    "Hemoglobin is significantly below reference ranges."
            })

            insights.append(
                "Hemoglobin is significantly low (severe anemia)."
            )

            health_score -= 20

        elif hemoglobin < 13:

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

            health_score -= 12

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

        if wbc > 15000:

            risks.append({

                "type":
                    "Severely Elevated WBC",

                "severity":
                    "high",

                "reason":
                    "White blood cell count is significantly elevated."
            })

            insights.append(
                "WBC is significantly elevated (severe infection/inflammation)."
            )

            health_score -= 18

        elif wbc > 11000:

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

            health_score -= 10

        elif wbc < 3000:

            risks.append({

                "type":
                    "Severely Low WBC",

                "severity":
                    "high",

                "reason":
                    "White blood cell count is critically low."
            })

            insights.append(
                "Low WBC is significantly below normal (immune compromise)."
            )

            health_score -= 18

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

        if platelets < 20000:

            risks.append({

                "type":
                    "Critical Low Platelets",

                "severity":
                    "critical",

                "reason":
                    "Platelet count is critically low (bleeding risk)."
            })

            insights.append(
                "Platelets are critically low. Seek immediate medical attention."
            )

            health_score -= 30

        elif platelets < 50000:

            risks.append({

                "type":
                    "Severely Low Platelets",

                "severity":
                    "high",

                "reason":
                    "Platelet count is significantly below reference ranges."
            })

            insights.append(
                "Platelet count is significantly low (thrombocytopenia)."
            )

            health_score -= 20

        elif platelets < 150000:

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

        if severity == "critical":

            risk_level = "critical"
            break

        elif severity == "high" and risk_level != "critical":

            risk_level = "high"

        elif severity == "moderate" and risk_level not in ["critical", "high"]:

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