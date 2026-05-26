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


def build_biomarker_table(vitals_data, risks):
    risk_map = {
        risk['type']: risk.get('severity', 'low')
        for risk in risks
    }

    biomarker_fields = [
        ('heart_rate', 'Heart Rate', 'bpm', '60-100'),
        ('spo2', 'Oxygen Saturation', '%', '95-100'),
        ('temperature', 'Temperature', '°C', '36.1-37.5'),
        ('systolic_bp', 'Systolic BP', 'mmHg', '90-120'),
        ('diastolic_bp', 'Diastolic BP', 'mmHg', '60-80'),
        ('sleep_hours', 'Sleep Hours', 'hrs', '7-9'),
        ('steps', 'Activity Steps', 'steps', '>=3000')
    ]

    table = []
    for key, label, unit, range_text in biomarker_fields:
        if key not in vitals_data:
            continue

        value = vitals_data[key]
        if value is None:
            continue

        status = 'Normal'
        severity = risk_map.get(key)
        if severity == 'moderate':
            status = 'Moderate'
        elif severity == 'high':
            status = 'High'

        table.append({
            'parameter': label,
            'value': f'{value} {unit}',
            'range': range_text,
            'status': status
        })

    return table


def compute_health_score(risks):
    if not risks:
        return 98

    score = 100
    for risk in risks:
        severity = risk.get('severity', 'low')
        if severity == 'high':
            score -= 25
        elif severity == 'moderate':
            score -= 12
        elif severity == 'low':
            score -= 5

    return max(40, score)


def process_vitals(vitals_data: dict):

    cleaned_vitals_data = {
        key: value
        for key, value in vitals_data.items()
        if value is not None
    }

    # =========================
    # ANALYZE VITALS

    analysis = analyze_vitals(
        cleaned_vitals_data
    )

    risks = analysis['risks']

    insights = analysis['insights']

    # =========================
    # RAG EVIDENCE

    evidence = get_vitals_evidence(
        risks
    )

    if not evidence:
        evidence = [
            'Provided vital sign values fall within normal healthy ranges.'
        ]

    # =========================
    # DOCTOR PREP

    doctor_prep = generate_vitals_questions(
        vitals_data,
        risks
    )

    doctor_questions = (
        doctor_prep.get(
            'questions',
            []
        )
    )

    # =========================
    # NEXT STEPS

    next_steps = []

    for risk in risks:

        risk_type = risk.get(
            'type',
            ''
        )

        if risk_type == 'heart_rate':
            next_steps.append(
                'Monitor heart rate regularly'
            )
        elif risk_type == 'spo2':
            next_steps.append(
                'Monitor oxygen levels closely'
            )
        elif risk_type == 'blood_pressure':
            next_steps.append(
                'Track blood pressure daily'
            )
        elif risk_type == 'temperature':
            next_steps.append(
                'Monitor temperature changes'
            )

    if not next_steps:
        next_steps = [
            'Maintain healthy lifestyle habits',
            'Continue monitoring vitals regularly'
        ]

    # =========================
    # SUMMARY

    if not risks:
        summary = (
            'All provided vital signs are healthy and within expected ranges.'
        )
    else:
        summary = (
            'Vital signs were analyzed for '
            'potential health pattern changes.'
        )

    biomarker_table = build_biomarker_table(cleaned_vitals_data, risks)
    health_score = compute_health_score(risks)

    # =========================
    # BUILD STRUCTURED RESPONSE

    response = build_structured_response(
        summary=summary,
        risk_indicators=risks,
        evidence=evidence,
        doctor_questions=doctor_questions,
        next_steps=next_steps,
        confidence=0.82,
        insights=insights,
        biomarker_table=biomarker_table,
        health_score=health_score
    )

    # =========================
    # SAVE FOR EXPORTS

    save_vitals_analysis(response)

    return response
