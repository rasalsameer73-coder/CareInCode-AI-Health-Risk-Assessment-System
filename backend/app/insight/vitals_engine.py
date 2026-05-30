def analyze_vitals(
    data: dict
):

    risks = []

    insights = []

    # HEART RATE

    heart_rate = data.get("heart_rate")
    if heart_rate is None:
        heart_rate = 0

    if heart_rate > 130:
        # Dangerous tachycardia
        risks.append({
            "type": "heart_rate",
            "severity": "high",
            "confidence": 0.85,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Heart rate is significantly elevated (tachycardia). Monitor closely."
        )

    elif heart_rate > 100:
        # Mild to moderate tachycardia
        risks.append({
            "type": "heart_rate",
            "severity": "moderate",
            "confidence": 0.75,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Heart rate appears elevated above normal resting rate."
        )

    elif heart_rate < 40:
        # Severe bradycardia
        risks.append({
            "type": "heart_rate",
            "severity": "high",
            "confidence": 0.80,
            "source": "rule-based"
        })

        insights.append(
            "Heart rate is significantly lower than normal (bradycardia). Seek medical attention."
        )

    elif heart_rate < 50:
        # Mild to moderate bradycardia
        risks.append({
            "type": "heart_rate",
            "severity": "moderate",
            "confidence": 0.70,
            "source": "rule-based"
        })

        insights.append(
            "Heart rate appears lower than typical resting rate."
        )
    
    elif heart_rate >= 60 and heart_rate <= 100:
        # Normal resting heart rate - no risk but we can add insight
        insights.append(
            "Heart rate is within normal resting range."
        )

    # SPO2

    spo2 = data.get("spo2")
    if spo2 is None:
        spo2 = 100

    if spo2 < 90:
        # Critical hypoxemia
        risks.append({
            "type": "spo2",
            "severity": "critical",
            "confidence": 0.95,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Oxygen saturation is critically low. Seek immediate medical attention."
        )

    elif spo2 < 95:
        # Low oxygen saturation
        risks.append({
            "type": "spo2",
            "severity": "high",
            "confidence": 0.85,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Oxygen saturation is lower than optimal. Monitor closely."
        )

    elif spo2 >= 95 and spo2 <= 100:
        # Normal oxygen saturation
        insights.append(
            "Oxygen saturation is in normal healthy range."
        )

    # TEMPERATURE

    temperature = data.get("temperature")
    if temperature is None:
        temperature = 0

    if temperature < 35:
        # Severe hypothermia
        risks.append({
            "type": "temperature",
            "severity": "critical",
            "confidence": 0.95,
            "source": "rule-based"
        })

        insights.append(
            "Body temperature is critically low (hypothermia). Seek immediate medical attention."
        )

    elif temperature < 36:
        # Mild hypothermia
        risks.append({
            "type": "temperature",
            "severity": "high",
            "confidence": 0.85,
            "source": "rule-based"
        })

        insights.append(
            "Body temperature is lower than normal range."
        )

    elif temperature > 40:
        # Severe fever/heat stroke
        risks.append({
            "type": "temperature",
            "severity": "critical",
            "confidence": 0.95,
            "source": "rule-based"
        })

        insights.append(
            "Body temperature is critically high. Seek immediate medical attention."
        )

    elif temperature > 39:
        # High fever
        risks.append({
            "type": "temperature",
            "severity": "high",
            "confidence": 0.90,
            "source": "rule-based"
        })

        insights.append(
            "Body temperature indicates significant fever."
        )

    elif temperature > 37.5:
        # Mild fever
        risks.append({
            "type": "temperature",
            "severity": "moderate",
            "confidence": 0.80,
            "source": "rule-based"
        })

        insights.append(
            "Body temperature appears slightly elevated."
        )

    # BLOOD PRESSURE

    systolic = data.get("systolic_bp")
    if systolic is None:
        systolic = 0

    diastolic = data.get("diastolic_bp")
    if diastolic is None:
        diastolic = 0

    if systolic > 140 or diastolic > 90:
        # Stage 2 Hypertension
        risks.append({
            "type": "blood_pressure",
            "severity": "high",
            "confidence": 0.85,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Blood pressure is significantly elevated (Stage 2 Hypertension)."
        )

    elif systolic > 130 or diastolic > 85:
        # Stage 1 Hypertension
        risks.append({
            "type": "blood_pressure",
            "severity": "moderate",
            "confidence": 0.80,
            "source": "hybrid (rule + RAG)"
        })

        insights.append(
            "Blood pressure readings are elevated (Stage 1 Hypertension)."
        )

    elif systolic >= 120 and diastolic < 80:
        # Elevated (not hypertension yet)
        risks.append({
            "type": "blood_pressure",
            "severity": "low",
            "confidence": 0.70,
            "source": "rule-based"
        })

        insights.append(
            "Blood pressure is in the elevated range. Monitor regularly."
        )

    elif systolic < 90 and diastolic < 60:
        # Hypotension
        risks.append({
            "type": "blood_pressure",
            "severity": "moderate",
            "confidence": 0.75,
            "source": "rule-based"
        })

        insights.append(
            "Blood pressure is lower than normal. Ensure proper hydration and rest."
        )

    # SLEEP

    sleep_hours = data.get("sleep_hours")
    if sleep_hours is None:
        sleep_hours = 8

    if sleep_hours < 5:

        risks.append({
            "type": "sleep",
            "severity": "moderate",
            "confidence": 0.72,
            "source": "rule-based"
        })

        insights.append(
            "Sleep duration appears lower than recommended."
        )

    elif sleep_hours < 6:

        risks.append({
            "type": "sleep",
            "severity": "low",
            "confidence": 0.68,
            "source": "rule-based"
        })

        insights.append(
            "Sleep duration appears slightly below recommended levels."
        )

    # ACTIVITY

    steps = data.get("steps")
    if steps is None:
        steps = 10000

    if steps < 3000:

        risks.append({
            "type": "activity",
            "severity": "low",
            "confidence": 0.68,
            "source": "rule-based"
        })

        insights.append(
            "Physical activity appears lower than common recommendations."
        )

    if not risks:
        insights.append(
            "All provided vital signs fall within healthy ranges."
        )

    return {

        "risks":
            risks,

        "insights":
            insights
    }