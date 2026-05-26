from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.validation_service import validate_file

from app.services.upload_service import save_uploaded_file

from app.services.health_record_service import (
    save_health_record_db,
    get_user_records
)

from app.services.analysis_storage_service import (
    save_report_analysis
)

from app.ocr.easyocr_engine import (
    extract_text_from_image
)

from app.ocr.pdf_parser import (
    extract_text_from_pdf
)

# =========================
# AI ORCHESTRATOR
# =========================

from app.orchestrator.health_orchestrator import (
    analyze_health_text
)

# =========================
# GENERIC HEALTH ENGINE
# =========================

from app.insight.engine import (
    analyze_health_data,
    extract_structured_metrics
)

from app.insight.doctor_prep import (
    generate_doctor_prep
)

from app.insight.trend_engine import (
    analyze_trends
)

from app.insight.report_classifier import (
    classify_medical_report
)

# =========================
# CBC IMPORTS
# =========================

from app.extractors.cbc_extractor import (
    extract_cbc_parameters
)

from app.analyzers.cbc_analyzer import (
    analyze_cbc_biomarkers
)

from app.utils.cbc_table_builder import (
    build_cbc_biomarker_table
)

from app.history.cbc_graph_data import (
    build_cbc_graph_data
)

from app.history.cbc_history_analyzer import (
    compare_cbc_reports
)

# =========================
# LIPID IMPORTS
# =========================

from app.extractors.lipid_extractor import (
    extract_lipid_parameters
)

from app.analyzers.lipid_analyzer import (
    analyze_lipid_biomarkers
)

from app.utils.lipid_table_builder import (
    build_lipid_biomarker_table
)

from app.history.lipid_history_analyzer import (
    compare_lipid_reports
)

# =========================
# DIABETES IMPORTS
# =========================

from app.extractors.diabetes_extractor import (
    extract_diabetes_parameters
)

from app.analyzers.diabetes_analyzer import (
    analyze_diabetes_biomarkers
)

from app.utils.diabetes_table_builder import (
    build_diabetes_biomarker_table
)

from app.history.diabetes_history_analyzer import (
    compare_diabetes_reports
)

# =========================
# THYROID IMPORTS
# =========================

from app.extractors.thyroid_extractor import (
    extract_thyroid_parameters
)

from app.analyzers.thyroid_analyzer import (
    analyze_thyroid_biomarkers
)

from app.utils.thyroid_table_builder import (
    build_thyroid_biomarker_table
)

from app.history.thyroid_history_analyzer import (
    compare_thyroid_reports
)

# =========================
# KIDNEY IMPORTS
# =========================

from app.extractors.kidney_extractor import (
    extract_kidney_parameters
)

from app.analyzers.kidney_analyzer import (
    analyze_kidney_biomarkers
)

from app.utils.kidney_table_builder import (
    build_kidney_biomarker_table
)

from app.history.kidney_history_analyzer import (
    compare_kidney_reports
)

# =========================
# LIVER IMPORTS
# =========================

from app.extractors.liver_extractor import (
    extract_liver_parameters
)

from app.analyzers.liver_analyzer import (
    analyze_liver_biomarkers
)

from app.utils.liver_table_builder import (
    build_liver_biomarker_table
)

from app.history.liver_history_analyzer import (
    compare_liver_reports
)

# =========================
# URINE IMPORTS
# =========================

from app.extractors.urine_extractor import (
    extract_urine_parameters
)

from app.analyzers.urine_analyzer import (
    analyze_urine_biomarkers
)

from app.utils.urine_table_builder import (
    build_urine_biomarker_table
)

from app.history.urine_history_analyzer import (
    compare_urine_reports
)

# =========================
# RESPONSE BUILDER
# =========================

from app.formatter.response_builder import (
    build_structured_response
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/report")
async def upload_report(
    file: UploadFile = File(...),
    user_id: str = "demo_user"
):

    # =========================
    # SAFETY CHECK
    # =========================

    if not file.filename:

        return {
            "error": "Filename missing"
        }

    filename = file.filename.lower()

    # =========================
    # FILE VALIDATION
    # =========================

    if not validate_file(filename):

        return {
            "error": "Invalid file type"
        }

    # =========================
    # SAVE FILE
    # =========================

    file_path = save_uploaded_file(file)

    # =========================
    # OCR / PDF EXTRACTION
    # =========================

    if filename.endswith(".pdf"):

        extracted = extract_text_from_pdf(
            file_path
        )

    else:

        extracted = extract_text_from_image(
            file_path
        )

    extracted_text = extracted.get(
        "text",
        ""
    )

    # =========================
    # REPORT CLASSIFICATION
    # =========================

    report_type = classify_medical_report(
        extracted_text
    )

    # =========================
    # STRUCTURED METRICS
    # =========================

    metrics = extract_structured_metrics(
        extracted_text
    )

    # =========================
    # DEFAULT VALUES
    # =========================

    biomarkers = {}

    history_trends = []

    biomarker_table = []

    summary = ""

    risk_level = "low"

    risk_indicators = []

    insights = []

    evidence = []

    doctor_questions = []

    next_steps = []

    health_score = 100

    # =========================
    # USER HISTORY
    # =========================

    history = get_user_records(
        user_id
    )

    # =========================
    # CBC PIPELINE
    # =========================

    if report_type == "cbc":

        biomarkers = extract_cbc_parameters(
            extracted_text
        )

        cbc_analysis = analyze_cbc_biomarkers(
            biomarkers
        )

        summary = cbc_analysis.get(
            "summary",
            "CBC report analyzed successfully."
        )

        risk_level = cbc_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = cbc_analysis.get(
            "risk_indicators",
            []
        )

        insights = cbc_analysis.get(
            "insights",
            []
        )

        evidence = cbc_analysis.get(
            "evidence",
            []
        )

        doctor_questions = cbc_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = cbc_analysis.get(
            "next_steps",
            []
        )

        health_score = cbc_analysis.get(
            "health_score",
            100
        )

        biomarker_table = build_cbc_biomarker_table(
            biomarkers
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_cbc_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # LIPID PIPELINE
    # =========================

    elif report_type == "lipid":

        biomarkers = extract_lipid_parameters(
            extracted_text
        )

        lipid_analysis = analyze_lipid_biomarkers(
            biomarkers
        )

        summary = lipid_analysis.get(
            "summary",
            "Lipid profile analyzed successfully."
        )

        risk_level = lipid_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = lipid_analysis.get(
            "risk_indicators",
            []
        )

        insights = lipid_analysis.get(
            "insights",
            []
        )

        evidence = lipid_analysis.get(
            "evidence",
            []
        )

        doctor_questions = lipid_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = lipid_analysis.get(
            "next_steps",
            []
        )

        health_score = lipid_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_lipid_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_lipid_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # DIABETES PIPELINE
    # =========================

    elif report_type == "diabetes":

        biomarkers = extract_diabetes_parameters(
            extracted_text
        )

        diabetes_analysis = analyze_diabetes_biomarkers(
            biomarkers
        )

        summary = diabetes_analysis.get(
            "summary",
            "Diabetes report analyzed successfully."
        )

        risk_level = diabetes_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = diabetes_analysis.get(
            "risk_indicators",
            []
        )

        insights = diabetes_analysis.get(
            "insights",
            []
        )

        evidence = diabetes_analysis.get(
            "evidence",
            []
        )

        doctor_questions = diabetes_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = diabetes_analysis.get(
            "next_steps",
            []
        )

        health_score = diabetes_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_diabetes_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_diabetes_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # THYROID PIPELINE
    # =========================

    elif report_type == "thyroid":

        biomarkers = extract_thyroid_parameters(
            extracted_text
        )

        thyroid_analysis = analyze_thyroid_biomarkers(
            biomarkers
        )

        summary = thyroid_analysis.get(
            "summary",
            "Thyroid report analyzed successfully."
        )

        risk_level = thyroid_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = thyroid_analysis.get(
            "risk_indicators",
            []
        )

        insights = thyroid_analysis.get(
            "insights",
            []
        )

        evidence = thyroid_analysis.get(
            "evidence",
            []
        )

        doctor_questions = thyroid_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = thyroid_analysis.get(
            "next_steps",
            []
        )

        health_score = thyroid_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_thyroid_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_thyroid_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # KIDNEY PIPELINE
    # =========================

    elif report_type == "kidney":

        biomarkers = extract_kidney_parameters(
            extracted_text
        )

        kidney_analysis = analyze_kidney_biomarkers(
            biomarkers
        )

        summary = kidney_analysis.get(
            "summary",
            "Kidney report analyzed successfully."
        )

        risk_level = kidney_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = kidney_analysis.get(
            "risk_indicators",
            []
        )

        insights = kidney_analysis.get(
            "insights",
            []
        )

        evidence = kidney_analysis.get(
            "evidence",
            []
        )

        doctor_questions = kidney_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = kidney_analysis.get(
            "next_steps",
            []
        )

        health_score = kidney_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_kidney_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_kidney_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # LIVER PIPELINE
    # =========================

    elif report_type == "liver":

        biomarkers = extract_liver_parameters(
            extracted_text
        )

        liver_analysis = analyze_liver_biomarkers(
            biomarkers
        )

        summary = liver_analysis.get(
            "summary",
            "Liver report analyzed successfully."
        )

        risk_level = liver_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = liver_analysis.get(
            "risk_indicators",
            []
        )

        insights = liver_analysis.get(
            "insights",
            []
        )

        evidence = liver_analysis.get(
            "evidence",
            []
        )

        doctor_questions = liver_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = liver_analysis.get(
            "next_steps",
            []
        )

        health_score = liver_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_liver_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_liver_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # URINE PIPELINE
    # =========================

    elif report_type == "urine":

        biomarkers = extract_urine_parameters(
            extracted_text
        )

        urine_analysis = analyze_urine_biomarkers(
            biomarkers
        )

        summary = urine_analysis.get(
            "summary",
            "Urine report analyzed successfully."
        )

        risk_level = urine_analysis.get(
            "risk_level",
            "low"
        )

        risk_indicators = urine_analysis.get(
            "risk_indicators",
            []
        )

        insights = urine_analysis.get(
            "insights",
            []
        )

        evidence = urine_analysis.get(
            "evidence",
            []
        )

        doctor_questions = urine_analysis.get(
            "doctor_questions",
            []
        )

        next_steps = urine_analysis.get(
            "next_steps",
            []
        )

        health_score = urine_analysis.get(
            "health_score",
            100
        )

        biomarker_table = (
            build_urine_biomarker_table(
                biomarkers
            )
        )

        previous_biomarkers = None

        if history:

            latest_record = history[-1]

            previous_biomarkers = latest_record.get(
                "biomarkers",
                {}
            )

        if previous_biomarkers:

            history_trends = compare_urine_reports(

                previous_biomarkers,

                biomarkers
            )

    # =========================
    # GENERIC AI PIPELINE
    # =========================

    else:

        risk_indicators = analyze_health_data(
            extracted_text
        )

        doctor_prep = generate_doctor_prep(
            risk_indicators
        )

        doctor_questions = doctor_prep.get(
            "questions",
            []
        )

        ai_result = analyze_health_text(
            extracted_text
        )

        summary = ai_result.get(
            "summary",
            "Health report analyzed successfully."
        )

        evidence = ai_result.get(
            "evidence",
            []
        )

        insights = ai_result.get(
            "insights",
            []
        )

        next_steps = [

            "Monitor symptoms closely",

            "Consult a healthcare professional if symptoms worsen"
        ]

    trend_analysis = analyze_trends(
        history
    )

    graph_data = build_cbc_graph_data(
        history
    )

    analysis = build_structured_response(

        summary=summary,

        insights=insights,

        risk_indicators=risk_indicators,

        evidence=evidence,

        doctor_questions=doctor_questions,

        next_steps=next_steps,

        confidence=0.90
    )

    analysis["risk_level"] = risk_level
    analysis["health_score"] = health_score
    analysis["history_trends"] = history_trends
    analysis["biomarker_table"] = biomarker_table
    analysis["graph_data"] = graph_data
    analysis["report_type"] = report_type.upper()

# VERY IMPORTANT
    analysis["biomarkers"] = biomarkers
    
    analysis["disclaimer"] = (
        "Educational information only. "
        "Not a medical diagnosis."
    )

    save_report_analysis(
        analysis
    )

    save_health_record_db(
        user_id=user_id,
        report_text=extracted_text,
        analysis=analysis,
        file_name=file.filename,
    )

    return {

        "report_type":
            report_type,

        "biomarkers":
            biomarkers,

        "history_trends":
            history_trends,

        "ocr":
            extracted,

            "analysis":
            analysis,

        "trend_analysis":
            trend_analysis,

        "graph_data":
            graph_data
    }