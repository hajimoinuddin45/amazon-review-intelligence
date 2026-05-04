from fpdf import FPDF
from datetime import datetime
import re


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r'[^\x00-\x7F]+',
        ' ',
        text
    )

    text = text.replace("#", "")
    text = text.replace("*", "")
    text = text.replace("•", "-")
    text = text.replace("```", "")
    text = text.replace(">", "")

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


# =====================================================
# PDF CLASS
# =====================================================

class PDF(FPDF):

    def header(self):

        self.set_fill_color(
            8,
            15,
            35
        )

        self.rect(
            0,
            0,
            210,
            22,
            style="F"
        )

        self.set_text_color(
            255,
            255,
            255
        )

        self.set_font(
            "Arial",
            "B",
            18
        )

        self.cell(
            0,
            14,
            "PIXII.AI COMMERCE REPORT",
            ln=True,
            align="C"
        )

        self.ln(10)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Arial",
            "I",
            8
        )

        self.set_text_color(
            120,
            120,
            120
        )

        self.cell(
            0,
            10,
            f"Page {self.page_no()}",
            align="C"
        )

    def section_title(self, title):

        self.set_fill_color(
            79,
            70,
            229
        )

        self.set_text_color(
            255,
            255,
            255
        )

        self.set_font(
            "Arial",
            "B",
            13
        )

        self.cell(
            0,
            10,
            clean_text(title),
            ln=True,
            fill=True
        )

        self.ln(5)

    def section_text(self, text):

        self.set_text_color(
            45,
            45,
            45
        )

        self.set_font(
            "Arial",
            "",
            11
        )

        self.multi_cell(
            180,
            7,
            clean_text(text)
        )

        self.ln(4)


# =====================================================
# MAIN REPORT
# =====================================================

def generate_report(df, insights):

    pdf = PDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    pdf.set_left_margin(15)
    pdf.set_right_margin(15)

    total_products = len(df)

    avg_rating = round(
        df["rating"].mean(),
        2
    )

    total_revenue = int(
        df["estimated_revenue"].sum()
    )

    # =====================================================
    # COVER SECTION
    # =====================================================

    pdf.ln(18)

    pdf.set_font(
        "Arial",
        "B",
        30
    )

    pdf.set_text_color(
        15,
        23,
        42
    )

    pdf.cell(
        0,
        14,
        "AI COMMERCE",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        14,
        "INTELLIGENCE REPORT",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        "",
        14
    )

    pdf.set_text_color(
        90,
        90,
        90
    )

    pdf.multi_cell(
        0,
        8,
        clean_text(
            """
AI-powered competitor benchmarking,
customer sentiment analysis,
revenue estimation,
and market opportunity detection.
"""
        ),
        align="C"
    )

    pdf.ln(15)

    # =====================================================
    # KPI CARDS
    # =====================================================

    card_y = pdf.get_y()

    cards = [

        ("Products", str(total_products), (79,70,229)),
        ("Avg Rating", str(avg_rating), (16,185,129)),
        ("Revenue", f"${total_revenue:,}", (245,158,11))
    ]

    x_positions = [15, 75, 135]

    for i, (title, value, color) in enumerate(cards):

        x = x_positions[i]

        pdf.set_fill_color(*color)

        pdf.rect(
            x,
            card_y,
            55,
            34,
            style="F"
        )

        pdf.set_xy(
            x,
            card_y + 6
        )

        pdf.set_text_color(
            255,
            255,
            255
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.cell(
            55,
            6,
            title,
            align="C"
        )

        pdf.set_xy(
            x,
            card_y + 16
        )

        pdf.set_font(
            "Arial",
            "B",
            17
        )

        pdf.cell(
            55,
            8,
            value,
            align="C"
        )

    pdf.ln(50)

    current_date = datetime.now().strftime(
        "%d %B %Y"
    )

    pdf.set_font(
        "Arial",
        "I",
        10
    )

    pdf.set_text_color(
        120,
        120,
        120
    )

    pdf.cell(
        0,
        8,
        f"Generated on {current_date}",
        ln=True,
        align="C"
    )

    # =====================================================
    # EXEC SUMMARY
    # =====================================================

    pdf.add_page()

    pdf.section_title(
        "Executive Summary"
    )

    summary = f"""
This report analyzes {total_products} Amazon product listings.

Estimated market revenue:
${total_revenue:,}

Average customer rating:
{avg_rating}

AI analysis identified:
- customer purchase drivers
- competitor weaknesses
- pricing opportunities
- growth strategies
- revenue expansion opportunities
"""

    pdf.section_text(summary)

    # =====================================================
    # COMPETITOR TABLE
    # =====================================================

    pdf.section_title(
        "Competitor Benchmarking"
    )

    pdf.set_fill_color(
        15,
        23,
        42
    )

    pdf.set_text_color(
        255,
        255,
        255
    )

    pdf.set_font(
        "Arial",
        "B",
        11
    )

    pdf.cell(
        90,
        12,
        "Product",
        border=1,
        fill=True
    )

    pdf.cell(
        30,
        12,
        "Rating",
        border=1,
        align="C",
        fill=True
    )

    pdf.cell(
        50,
        12,
        "Revenue",
        border=1,
        align="C",
        fill=True
    )

    pdf.ln()

    pdf.set_font(
        "Arial",
        "",
        10
    )

    alternate = False

    for _, row in df.iterrows():

        if alternate:

            pdf.set_fill_color(
                245,
                247,
                250
            )

        else:

            pdf.set_fill_color(
                255,
                255,
                255
            )

        alternate = not alternate

        pdf.set_text_color(
            40,
            40,
            40
        )

        title = clean_text(
            str(row["title"])[:40]
        )

        revenue = f"${int(row['estimated_revenue']):,}"

        pdf.cell(
            90,
            11,
            title,
            border=1,
            fill=True
        )

        pdf.cell(
            30,
            11,
            str(row["rating"]),
            border=1,
            align="C",
            fill=True
        )

        pdf.cell(
            50,
            11,
            revenue,
            border=1,
            align="C",
            fill=True
        )

        pdf.ln()

    pdf.ln(8)

    # =====================================================
    # AI INSIGHTS
    # =====================================================

    pdf.section_title(
        "AI Review Intelligence"
    )

    insights = insights.split(
        "AI API Notice"
    )[0]

    insights = clean_text(
        insights
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.set_text_color(
        40,
        40,
        40
    )

    insight_lines = insights.split(".")

    for line in insight_lines:

        line = clean_text(line)

        if len(line) < 5:
            continue

        pdf.cell(
            6,
            7,
            "-"
        )

        pdf.multi_cell(
            170,
            7,
            line
        )

        pdf.ln(1)

    pdf.ln(5)

    # =====================================================
    # SWOT ANALYSIS
    # =====================================================

    pdf.section_title(
        "Strategic SWOT Analysis"
    )

    swot_items = [

        ("Strengths",
         "Strong performance and trusted branding",
         (16,185,129)),

        ("Weaknesses",
         "Packaging complaints and heating concerns",
         (239,68,68)),

        ("Opportunities",
         "Battery-focused marketing opportunity",
         (59,130,246)),

        ("Threats",
         "Aggressive competitor pricing",
         (245,158,11))
    ]

    for title, text, color in swot_items:

        pdf.set_fill_color(*color)

        current_y = pdf.get_y()

        pdf.rect(
            15,
            current_y,
            180,
            18,
            style="F"
        )

        pdf.set_xy(
            20,
            current_y + 3
        )

        pdf.set_text_color(
            255,
            255,
            255
        )

        pdf.set_font(
            "Arial",
            "B",
            11
        )

        pdf.cell(
            0,
            5,
            clean_text(title),
            ln=True
        )

        pdf.set_x(20)

        pdf.set_font(
            "Arial",
            "",
            10
        )

        pdf.cell(
            0,
            5,
            clean_text(text),
            ln=True
        )

        pdf.ln(6)

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    pdf.section_title(
        "Strategic Recommendations"
    )

    recommendations = [

        "Improve packaging quality",
        "Focus marketing on reliability",
        "Improve customer trust messaging",
        "Highlight battery optimization",
        "Improve delivery experience"
    ]

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.set_text_color(
        40,
        40,
        40
    )

    for rec in recommendations:

        pdf.set_fill_color(
            243,
            244,
            246
        )

        current_y = pdf.get_y()

        pdf.rect(
            15,
            current_y,
            180,
            10,
            style="F"
        )

        pdf.set_xy(
            20,
            current_y + 2
        )

        pdf.cell(
            5,
            6,
            "-"
        )

        pdf.cell(
            160,
            6,
            clean_text(rec),
            ln=True
        )

        pdf.ln(3)

    # =====================================================
    # TOP PRODUCT
    # =====================================================

    top_product = df.loc[
        df["estimated_revenue"].idxmax()
    ]

    pdf.ln(5)

    pdf.section_title(
        "Top Performing Product"
    )

    current_y = pdf.get_y()

    pdf.set_fill_color(
        15,
        23,
        42
    )

    pdf.rect(
        15,
        current_y,
        180,
        32,
        style="F"
    )

    pdf.set_xy(
        20,
        current_y + 5
    )

    pdf.set_text_color(
        255,
        255,
        255
    )

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.multi_cell(
        160,
        6,
        clean_text(top_product["title"])
    )

    pdf.set_x(20)

    pdf.set_font(
        "Arial",
        "",
        10
    )

    pdf.cell(
        0,
        6,
        f"Revenue: ${int(top_product['estimated_revenue']):,}",
        ln=True
    )

    pdf.set_x(20)

    pdf.cell(
        0,
        6,
        f"Rating: {top_product['rating']}",
        ln=True
    )

    # =====================================================
    # SAVE
    # =====================================================

    pdf.output(
        "amazon_report.pdf"
    )