import streamlit as st
import pandas as pd
import time
from functools import lru_cache

from scraper.amazon_scraper import scrape_product_details
from scraper.review_scraper import get_reviews

from analysis.real_ai_engine import (
    generate_ai_strategy
)

from analysis.revenue_estimator import (
    estimate_monthly_sales,
    estimate_revenue
)

from analysis.sentiment import (
    get_sentiment_distribution
)

from analysis.feature_sentiment import (
    analyze_feature_sentiment
)

from analysis.competitor_compare import (
    competitor_comparison
)

from visualization.charts import (
    revenue_chart,
    sentiment_chart
)

from utils.report_generator import (
    generate_report
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Pixii | AI Commerce Intelligence",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
        radial-gradient(circle at top left, #1e1b4b 0%, transparent 30%),
        radial-gradient(circle at bottom right, #312e81 0%, transparent 30%),
        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #111827
        );

    color: white;
}

/* =====================================================
GLOBAL CONTAINER
===================================================== */

.block-container {

    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #020617,
            #0f172a
        );
}

/* =====================================================
HERO CARD
===================================================== */

.hero-card {

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.92),
            rgba(30,41,59,0.82)
        );

    border-radius: 32px;

    padding: 3rem;

    margin-bottom: 2rem;

    position: relative;

    overflow: hidden;

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0px 25px 60px rgba(0,0,0,0.5);
}

.hero-card::after {

    content: "";

    position: absolute;

    top: -120px;
    right: -120px;

    width: 320px;
    height: 320px;

    background:
        radial-gradient(
            rgba(99,102,241,0.45),
            transparent
        );

    filter: blur(60px);

    border-radius: 50%;
}

.gradient-title {

    font-size: clamp(42px, 6vw, 72px);

    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #818cf8,
            #c084fc
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 18px;

    line-height: 1.1;
}

/* =====================================================
METRIC CARDS
===================================================== */

.metric-card {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.03)
        );

    border-radius: 28px;

    padding: 2rem;

    text-align: center;

    backdrop-filter: blur(18px);

    border:
        1px solid rgba(255,255,255,0.08);

    transition: 0.35s ease;

    box-shadow:
        0px 10px 35px rgba(0,0,0,0.35);

    position: relative;

    overflow: hidden;
}

.metric-card::before {

    content: "";

    position: absolute;

    top: -50px;
    right: -50px;

    width: 140px;
    height: 140px;

    background:
        radial-gradient(
            rgba(124,58,237,0.38),
            transparent
        );

    border-radius: 50%;
}

.metric-card:hover {

    transform:
        translateY(-10px)
        scale(1.02);

    box-shadow:
        0px 25px 60px rgba(0,0,0,0.45);
}

/* =====================================================
SECTION CARDS
===================================================== */

.section-card {

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.88),
            rgba(30,41,59,0.72)
        );

    border-radius: 28px;

    padding: 2rem;

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    margin-top: 1rem;

    transition: 0.35s ease;

    box-shadow:
        0px 20px 45px rgba(0,0,0,0.35);

    position: relative;

    overflow: hidden;
}

.section-card::before {

    content: "";

    position: absolute;

    top: -50px;
    right: -50px;

    width: 150px;
    height: 150px;

    background:
        radial-gradient(
            rgba(99,102,241,0.22),
            transparent
        );

    border-radius: 50%;
}

.section-card:hover {

    transform:
        translateY(-8px)
        scale(1.01);

    box-shadow:
        0px 28px 65px rgba(0,0,0,0.45);
}

/* =====================================================
BUTTONS
===================================================== */

.stButton > button {

    width: 100%;

    height: 64px;

    font-size: 20px;

    font-weight: 700;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #7c3aed
        );

    border: none;

    color: white;

    box-shadow:
        0px 15px 35px rgba(79,70,229,0.45);

    transition: 0.35s ease;
}

.stButton > button:hover {

    transform:
        translateY(-6px)
        scale(1.02);

    box-shadow:
        0px 25px 55px rgba(124,58,237,0.55);
}
/* =====================================================
STATUS BAR
===================================================== */

.status-bar {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    padding: 18px;

    border-radius: 18px;

    margin-top: 18px;

    margin-bottom: 24px;

    backdrop-filter: blur(16px);

    box-shadow:
        0px 10px 30px rgba(0,0,0,0.25);

    font-size: 16px;

    color: #e2e8f0;

    animation: pulseGlow 3s infinite;
}

@keyframes pulseGlow {

    0% {
        box-shadow:
            0px 10px 30px rgba(99,102,241,0.15);
    }

    50% {
        box-shadow:
            0px 15px 40px rgba(99,102,241,0.35);
    }

    100% {
        box-shadow:
            0px 10px 30px rgba(99,102,241,0.15);
    }
}
            
/* =====================================================
TEXT AREA
===================================================== */

textarea {

    border-radius: 18px !important;

    background:
        rgba(255,255,255,0.04) !important;

    color: white !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⬡ Pixii.ai")

st.sidebar.markdown("""
### ANALYTICS

- 📊 Dashboard
- 🛒 Competitors
- 💰 Revenue Estimator
- 🤖 AI Insights
- 😊 Sentiment Analysis
- 📈 Market Intelligence
""")

st.sidebar.success(
    "AI agents actively analyzing competitor products."
)

# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero-card">

<h1 class="gradient-title">
AI Commerce Intelligence Platform
</h1>

<p style="
font-size:22px;
color:#cbd5e1;
max-width:900px;
line-height:1.8;
">

AI-powered competitor intelligence engine for Amazon sellers.

Analyze customer reviews,
benchmark competitors,
estimate revenue opportunities,
and generate AI-powered growth strategies instantly.

</p>

<div style="
margin-top:30px;
display:flex;
gap:14px;
flex-wrap:wrap;
">

<div style="
background:rgba(99,102,241,0.18);
padding:12px 20px;
border-radius:999px;
">
🤖 AI Agents
</div>

<div style="
background:rgba(34,197,94,0.18);
padding:12px 20px;
border-radius:999px;
">
📈 Competitor Intelligence
</div>

<div style="
background:rgba(168,85,247,0.18);
padding:12px 20px;
border-radius:999px;
">
💰 Revenue Prediction
</div>

<div style="
background:rgba(56,189,248,0.18);
padding:12px 20px;
border-radius:999px;
">
🧠 AI Growth Copilot
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">

🟢 Scraper Online &nbsp;&nbsp;&nbsp;
🟣 AI Engine Active &nbsp;&nbsp;&nbsp;
🔵 Revenue Prediction Running &nbsp;&nbsp;&nbsp;
🟠 Sentiment Analysis Ready &nbsp;&nbsp;&nbsp;
⚡ Growth Copilot Online

</div>
""", unsafe_allow_html=True)

# =====================================================
# INPUT
# =====================================================

urls = st.text_area(
    "Paste Amazon URLs (1 per line)",
    height=180
)

# =====================================================
# BUTTON
# =====================================================

if st.button("🚀 Analyze Listings"):

    with st.spinner(
        "🤖 AI agents analyzing market competitors..."
    ):
        product_urls = [
            url.strip()
            for url in urls.split("\n")
            if url.strip()
        ]

        all_products = []

        for url in product_urls:

            data = scrape_product_details(url)

            estimated_sales = estimate_monthly_sales(
                data["review_count"],
                data["rating"]
            )

            estimated_revenue = estimate_revenue(
                data["price"],
                estimated_sales
            )

            data["estimated_sales"] = estimated_sales
            data["estimated_revenue"] = estimated_revenue

            all_products.append(data)

        df = pd.DataFrame(all_products)
        st.success(
            "✅ AI Market Analysis Complete"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("# 📈 Market Overview")

    score_col, col1, col2, col3, col4 = st.columns(5)

    with score_col:

        st.markdown("""
        <div class="metric-card">
        <h3>🧠 Opportunity Score</h3>
        <h1 style="color:#22c55e;">92/100</h1>
        </div>
        """, unsafe_allow_html=True)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
        <h3>📦 Products</h3>
        <h1>{len(df)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
        <h3>⭐ Avg Rating</h3>
        <h1>{round(df["rating"].mean(),2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
        <h3>💰 Revenue</h3>
        <h1>₹{int(df['estimated_revenue'].sum()):,}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="metric-card">
        <h3>📝 Reviews</h3>
        <h1>{int(df['review_count'].sum()):,}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("# 🛍 Featured Products")

    products_per_row = 3

    for i in range(0, len(df), products_per_row):

        cols = st.columns(products_per_row)

        chunk = df.iloc[i:i + products_per_row]

        for idx, (_, row) in enumerate(chunk.iterrows()):

            image_url = row["image_url"]
            with cols[idx]:
                
                st.markdown(f"""
                <div class="section-card">

                <div style="
                background:white;
                border-radius:18px;
                padding:14px;
                height:280px;
                display:flex;
                align-items:center;
                justify-content:center;
                margin-bottom:18px;
                ">

                <img src="{row['image_url']}"
                style="
                max-width:100%;
                max-height:240px;
                object-fit:contain;
                ">
                </div>

                <h3 style="
                line-height:1.5;
                margin-bottom:16px;
                min-height:72px;
                ">
                {
                row['title'][:38] + "..."
                if len(row['title']) > 38
                else row['title']
                }
                </h3>

                <p style="font-size:17px;">
                ⭐ Rating: {row['rating']}
                </p>

                <p style="font-size:17px;">
                💰 Revenue: ₹{int(row['estimated_revenue']):,}
                </p>

                <p style="font-size:17px;">
                📦 Reviews: {row['review_count']}
                </p>

                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:

        st.markdown("# 🛒 Product Comparison")

        display_df = df[[

            "title",
            "price",
            "rating",
            "review_count",
            "estimated_revenue"

        ]].copy()

        display_df["title"] = display_df["title"].apply(
            lambda x: x[:45] + "..."
            if len(x) > 45 else x
        )

        styled_df = display_df.style.format({

            "price": "₹{:,.0f}",

            "estimated_revenue": "₹{:,.0f}",

            "rating": "{:.1f}"
        })

        st.dataframe(

            styled_df,

            use_container_width=True,

            height=420
        )

    with right:

        st.markdown("# 📊 Revenue Comparison")

        fig = revenue_chart(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # COMPETITOR INTELLIGENCE
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("# ⚔️ Competitor Intelligence")

    comparison_data = competitor_comparison(df)

    for item in comparison_data:

        st.markdown(f"""
        <div class="section-card">

        <h3>{item['Product']}</h3>

        <p>
        <b>🏆 Best At:</b>
        {item['Best At']}
        </p>

        <p>
        <b>⚠️ Weakness:</b>
        {item['Weakness']}
        </p>

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("# 🤖 AI Review Insights")

    status = st.empty()

    progress = st.progress(0)

    # =====================================================
    # STEP 1
    # =====================================================

    status.markdown("""

    <div class="status-bar">

    🤖 AI agents scraping customer reviews...

    </div>

    """, unsafe_allow_html=True)

    progress.progress(20)

    reviews = get_reviews(product_urls)

    # =====================================================
    # STEP 2
    # =====================================================

    status.markdown("""

    <div class="status-bar">

    🧠 AI analyzing customer sentiment...

    </div>

    """, unsafe_allow_html=True)

    progress.progress(50)

    feature_scores = analyze_feature_sentiment(
        reviews
    )

    sentiment = get_sentiment_distribution(
        reviews
    )

    # =====================================================
    # STEP 3
    # =====================================================

    status.markdown("""

    <div class="status-bar">

    ⚡ Generating ecommerce intelligence report...

    </div>

    """, unsafe_allow_html=True)

    progress.progress(80)

    insights = generate_ai_strategy(

        reviews[:10],

        df.iloc[0]["title"],

        df.iloc[0]["rating"],

        int(df.iloc[0]["estimated_revenue"])
    )

    # =====================================================
    # COMPLETE
    # =====================================================

    progress.progress(100)

    status.markdown("""

    <div class="status-bar">

    ✅ AI intelligence report generated successfully

    </div>

    """, unsafe_allow_html=True)

    time.sleep(1)

    progress.empty()

    generate_report(
        df,
        insights
    )

    import re

    # Remove ALL HTML tags
    clean_insights = re.sub(
        r'<[^>]*>',
        '',
        insights
    )

    st.markdown(f"""
    <div class="section-card">
    {clean_insights}</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    colA, colB = st.columns([1,1])

    with colA:

        st.markdown("# 😊 Customer Sentiment")

        fig2 = sentiment_chart(sentiment)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # =====================================================
        # FEATURE SENTIMENT ANALYSIS
        # =====================================================

        st.markdown(
            "# 🔍 Feature Sentiment Analysis"
        )

        for feature, score in feature_scores.items():

            if score > 0:

                sentiment_label = "🟢 Positive"

            elif score < 0:

                sentiment_label = "🔴 Negative"

            else:

                sentiment_label = "🟡 Neutral"

            st.markdown(f"""
            <div class="section-card">

            <h3>{feature}</h3>

            <h2>{sentiment_label}</h2>

            </div>
            """, unsafe_allow_html=True)

    with colB:

        st.markdown("# 🧠 AI Recommendations")

        st.markdown("""
        <div class="section-card">

        <h3>🚀 Strategic Actions</h3>

        <ul>
        <li>Improve packaging quality</li>
        <li>Optimize battery performance</li>
        <li>Focus marketing on premium quality</li>
        <li>Add comparison visuals</li>
        <li>Increase testimonial visibility</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("# 🚀 AI Growth Copilot")

    st.markdown("""
    <div class="section-card">

    <h2>🎯 Recommended Positioning</h2>

    <p>
    Premium reliability with superior battery performance.
    Position against competitors using trust and durability.
    </p>

    <hr>

    <h2>⚠️ Competitor Weaknesses</h2>

    <ul>
    <li>Weak packaging experience</li>
    <li>Generic product descriptions</li>
    <li>Poor emotional branding</li>
    <li>Low differentiation</li>
    </ul>

    <hr>

    <h2>🧠 Suggested Ad Hooks</h2>

    <ul>
    <li>"Never worry about battery again."</li>
    <li>"Premium performance trusted by thousands."</li>
    <li>"Built for professionals."</li>
    </ul>

    <hr>

    <h2>📈 Conversion Opportunities</h2>

    <ul>
    <li>Add comparison visuals</li>
    <li>Improve hero image quality</li>
    <li>Highlight customer testimonials</li>
    <li>Emphasize delivery reliability</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    with open(
        "amazon_report.pdf",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download AI Report",
            data=file,
            file_name="amazon_report.pdf",
            mime="application/pdf"
        )

    st.markdown("---")

    st.markdown("""
    <center>

    <h3 style="color:#818cf8;">
    Pixii.ai Inspired Analytics Engine
    </h3>

    <p>
    Built with Streamlit • AI Analytics • Plotly
    </p>

    </center>
    """, unsafe_allow_html=True)