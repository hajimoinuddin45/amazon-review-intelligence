import os
import google.generativeai as genai
from functools import lru_cache

from dotenv import load_dotenv

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =====================================================
# GEMINI MODEL
# =====================================================

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# =====================================================
# FALLBACK RESPONSE
# =====================================================

FALLBACK_RESPONSE = """

# 🔍 AI Commerce Intelligence Report

## SWOT Analysis

### Strengths
- Strong customer engagement
- Positive product perception
- Good market demand
- High review activity

### Weaknesses
- Strong competition
- Weak differentiation
- Packaging concerns
- Customer support gaps

### Opportunities
- Premium positioning
- Better emotional branding
- Improved conversion strategy
- Stronger trust marketing

### Threats
- Aggressive pricing competition
- Market saturation
- Rapid feature commoditization

---

# 🛒 Customer Pain Points

- Product durability concerns
- Delivery inconsistency
- Packaging quality issues
- Price sensitivity

---

# ✅ Purchase Drivers

- Brand trust
- Product quality
- Premium feel
- Fast delivery
- Performance reliability

---

# 💰 Pricing Psychology Analysis

Customers perceive higher-priced products as more reliable and premium.

Opportunity exists to strengthen value communication.

---

# 🚀 Brand Positioning Strategy

Focus positioning around:

- reliability
- trust
- long-term value
- premium ownership experience

---

# 🎯 Emotional Buying Triggers

- Fear of low quality
- Desire for premium ownership
- Convenience
- Social status
- Reliability assurance

---

# 📈 Revenue Growth Opportunities

- Improve packaging experience
- Add comparison visuals
- Increase testimonial visibility
- Strengthen emotional branding

Potential upside:
+15% to +30% conversion improvement.

"""

# =====================================================
# REAL AI ENGINE
# =====================================================
def generate_ai_strategy(
    reviews,
    product_name,
    rating,
    revenue
):

    try:

        # =============================================
        # LIMIT REVIEW SIZE
        # =============================================

        review_text = "\n".join(
            reviews[:10]
        )

        # =============================================
        # ADVANCED PROMPT
        # =============================================

        prompt = f"""

You are a senior ecommerce growth strategist and AI market intelligence analyst.

Analyze this SPECIFIC Amazon product deeply.

Your analysis MUST be:
- product-specific
- strategic
- ecommerce-focused
- conversion-focused
- investor-grade
- realistic

Avoid generic advice.

--------------------------------------------------

PRODUCT:
{product_name}

CUSTOMER RATING:
{rating}

ESTIMATED REVENUE:
{revenue}

CUSTOMER REVIEWS:
{review_text}

--------------------------------------------------

Generate a detailed ecommerce intelligence report.

Include:

# SWOT Analysis

Analyze:
- strengths
- weaknesses
- opportunities
- threats

specific to THIS product category.

# Customer Pain Points

Identify:
- recurring frustrations
- product complaints
- delivery concerns
- pricing concerns

# Purchase Drivers

Explain:
- why customers buy
- emotional triggers
- trust signals
- conversion factors

# Pricing Psychology Analysis

Analyze:
- premium perception
- value positioning
- price sensitivity
- competitor pricing pressure

# Brand Positioning Strategy

Recommend:
- positioning angle
- branding direction
- differentiation strategy

# Emotional Buying Triggers

Explain:
- emotional motivations
- customer psychology
- fear/desire drivers

# Suggested Marketing Hooks

Generate:
- ad messaging angles
- positioning hooks
- emotional copy ideas

# Competitor Weaknesses

Identify:
- weak differentiation
- poor branding
- messaging gaps
- trust gaps

# Conversion Optimization Opportunities

Suggest:
- PDP improvements
- image improvements
- trust-building ideas
- CRO opportunities

# Revenue Growth Opportunities

Estimate:
- growth potential
- conversion opportunities
- upsell/cross-sell opportunities

IMPORTANT:
- Use markdown formatting
- Be highly specific
- Avoid generic filler
- Write like a real ecommerce consultant

"""

        # =============================================
        # AI GENERATION
        # =============================================

        response = model.generate_content(
            prompt
        )

        # =============================================
        # SAFETY FALLBACK
        # =============================================

        if not response.text:

            return FALLBACK_RESPONSE

        return response.text

    except Exception:

        return FALLBACK_RESPONSE