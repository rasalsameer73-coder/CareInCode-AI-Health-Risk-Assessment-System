from app.insight.vitals_engine import (
    analyze_vitals
)

from app.rag.vitals_rag_service import (
    get_vitals_evidence
)

from app.insight.vitals_doctor_prep import (
    generate_vitals_questions
)

from app.formatter.response_builder import (
    build_structured_response
)

from app.services.analysis_storage_service import (
    save_vitals_analysis
)


def process_vitals(
    vitals_data: dict
):

    cleaned_vitals_data = {
        key: value
        for key, value in vitals_data.items()
        if value is not None
    }

    # =========================
    # ANALYZE VITALS
    # =========================

    analysis = analyze_vitals(
        cleaned_vitals_data
    )

    risks = analysis["risks"]

    insights = analysis["insights"]

    # =========================
    # RAG EVIDENCE
    # =========================

    evidence = get_vitals_evidence(
        risks
    )

    if not evidence:
        evidence = [
            "Provided vital sign values fall within normal healthy ranges."
        ]

    # =========================
    # DOCTOR PREP
    # =========================

    doctor_prep = generate_vitals_questions(
        vitals_data,
        risks
    )

    doctor_questions = (
        doctor_prep.get(
            "questions",
            []
        )
    )

    # =========================
    # NEXT STEPS
    # =========================

    next_steps = []

    for risk in risks:

        risk_type = risk.get(
            "type",
            ""
        )

        # HEART RATE
        if risk_type == "heart_rate":

            next_steps.append(
                "Monitor heart rate regularly"
            )

        # SPO2
        elif risk_type == "spo2":

            next_steps.append(
                "Monitor oxygen levels closely"
            )

        # BLOOD PRESSURE
        elif risk_type == "blood_pressure":

            next_steps.append(
                "Track blood pressure daily"
            )

        # TEMPERATURE
        elif risk_type == "temperature":

            next_steps.append(
                "Monitor temperature changes"
            )

    # DEFAULT NEXT STEPS
    if not next_steps:

        next_steps = [

            "Maintain healthy lifestyle habits",

            "Continue monitoring vitals regularly"
        ]

    # =========================
    # SUMMARY
    # =========================

    if not risks:
        summary = (
            "All provided vital signs are healthy and within expected ranges."
        )
    else:
        summary = (
            "Vital signs were analyzed for "
            "potential health pattern changes."
        )

    # =========================
    # BUILD STRUCTURED RESPONSE
    # =========================

    response = build_structured_response(

        summary=summary,

        risk_indicators=risks,

        evidence=evidence,

        doctor_questions=doctor_questions,

        next_steps=next_steps,

        confidence=0.82,

        insights=insights
    )

    # =========================
    # SAVE FOR EXPORTS
    # =========================

    save_vitals_analysis(response)

    return response