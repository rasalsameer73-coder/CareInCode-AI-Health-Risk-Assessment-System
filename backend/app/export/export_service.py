import json
import os

from datetime import datetime, timedelta, timezone

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from app.export.graph_renderer import (
    generate_health_graph
)

from app.formatter.response_builder import (
    _resolve_health_score
)


# =========================
# EXPORT JSON
# =========================

def export_json(
    data,
    filepath: str
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

    return filepath


# =========================
# EXPORT PDF
# =========================

def export_pdf(
    data,
    filepath: str
):

    doc = SimpleDocTemplate(
        filepath
    )

    styles = getSampleStyleSheet()

    if isinstance(data, dict) and "analysis" in data and isinstance(data["analysis"], dict):
        data = data["analysis"]

    elements = []

    # =========================
    # TITLE
    # =========================

    elements.append(

        Paragraph(

            "CareInCode+ Health Report",

            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # =========================
    # GENERATED DATE
    # =========================

    ist = timezone(timedelta(hours=5, minutes=30))
    timestamp = datetime.now(tz=ist).strftime("%A, %d %B %Y %H:%M IST")

    elements.append(

        Paragraph(

            f"<b>Generated:</b> {timestamp}",

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # SUMMARY
    # =========================

    elements.append(

        Paragraph(

            "<b>Summary</b>",

            styles["Heading2"]
        )
    )

    summary_text = data.get(
        "summary",
        "No summary available."
    )
    if isinstance(summary_text, str):
        summary_text = summary_text.replace("\n", "<br/>")

    elements.append(

        Paragraph(

            summary_text,

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # HEALTH SCORE
    # =========================

    health_score = _resolve_health_score(
        data.get("health_score"),
        data.get("risk_indicators", [])
    )

    risk_level = data.get(
        "risk_level",
        "low"
    )

    score_table = Table([

        ["Health Score", str(health_score)],

        ["Risk Level", risk_level.upper()]
    ])

    score_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightblue
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    elements.append(score_table)

    elements.append(
        Spacer(1, 20)
    )

    # =========================
    # RISK INDICATORS
    # =========================

    elements.append(

        Paragraph(

            "<b>Risk Indicators</b>",

            styles["Heading2"]
        )
    )

    risks = data.get(
        "risk_indicators",
        []
    )

    if risks:

        for risk in risks:

            risk_text = (

                f"• {risk.get('type', '')} "

                f"({risk.get('severity', '')})"
            )

            elements.append(

                Paragraph(

                    risk_text,

                    styles["BodyText"]
                )
            )

    else:

        elements.append(

            Paragraph(

                "No major risk indicators detected.",

                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # BIOMARKER TABLE
    # =========================

    elements.append(

        Paragraph(

            "<b>Biomarker Analysis</b>",

            styles["Heading2"]
        )
    )

    biomarker_table = data.get(
        "biomarker_table",
        []
    )

    if biomarker_table:

        table_data = [[

            "Parameter",

            "Value",

            "Reference Range",

            "Status"
        ]]

        for row in biomarker_table:

            table_data.append([

                row.get(
                    "parameter",
                    ""
                ),

                str(
                    row.get(
                        "value",
                        ""
                    )
                ),

                row.get(
                    "range",
                    ""
                ),

                row.get(
                    "status",
                    ""
                )
            ])

        biomarker_pdf_table = Table(
            table_data
        )

        biomarker_pdf_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightblue
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.whitesmoke
                )
            ])
        )

        elements.append(
            biomarker_pdf_table
        )

    else:

        elements.append(

            Paragraph(

                "No biomarker data available.",

                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 20)
    )

    # =========================
    # INSIGHTS
    # =========================

    elements.append(

        Paragraph(

            "<b>Insights</b>",

            styles["Heading2"]
        )
    )

    insights = data.get(
        "insights",
        []
    )

    for item in insights:

        elements.append(

            Paragraph(

                f"• {item}",

                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # NEXT STEPS
    # =========================

    elements.append(

        Paragraph(

            "<b>Next Steps</b>",

            styles["Heading2"]
        )
    )

    next_steps = data.get(
        "next_steps",
        []
    )

    for step in next_steps:

        elements.append(

            Paragraph(

                f"• {step}",

                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    elements.append(

        Paragraph(

            "<b>Questions For Doctor</b>",

            styles["Heading2"]
        )
    )

    doctor_questions = data.get(
        "doctor_prep",
        {}
    ).get(
        "questions",
        []
    )

    for q in doctor_questions:

        elements.append(

            Paragraph(

                f"• {q}",

                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 15)
    )

    # =========================
    # HISTORY TRENDS
    # =========================

    history_trends = data.get(
        "history_trends",
        []
    )

    if history_trends:

        elements.append(

            Paragraph(

                "<b>Health Trends</b>",

                styles["Heading2"]
            )
        )

        for trend in history_trends:

            elements.append(

                Paragraph(

                    f"• {trend}",

                    styles["BodyText"]
                )
            )

        elements.append(
            Spacer(1, 15)
        )

    # =========================
    # HEALTH GRAPHS
    # =========================

    graph_data = data.get(
        "graph_data",
        {}
    )

    if graph_data:

        elements.append(

            Paragraph(

                "<b>Health Graphs</b>",

                styles["Heading2"]
            )
        )

        for parameter, points in graph_data.items():

            if not points:

                continue

            image_path = (
                f"{parameter}_graph.png"
            )

            generated = generate_health_graph(

                points,

                parameter,

                image_path
            )

            if generated and os.path.exists(
                generated
            ):

                elements.append(

                    Paragraph(

                        f"<b>{parameter.upper()} Trend</b>",

                        styles["BodyText"]
                    )
                )

                elements.append(

                    Image(

                        generated,

                        width=400,

                        height=200
                    )
                )

                elements.append(
                    Spacer(1, 15)
                )

    # =========================
    # DISCLAIMER
    # =========================

    elements.append(

        Paragraph(

            "<b>Disclaimer</b>",

            styles["Heading2"]
        )
    )

    elements.append(

        Paragraph(

            data.get(
                "disclaimer",
                ""
            ),

            styles["BodyText"]
        )
    )

    # =========================
    # BUILD PDF
    # =========================

    doc.build(elements)

    return filepath