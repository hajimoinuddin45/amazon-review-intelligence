def competitor_comparison(df):

    comparisons = []

    for _, row in df.iterrows():

        title = row["title"].lower()

        if "iphone" in title:

            best_at = "Premium Branding"
            weakness = "High Pricing"

        elif "samsung" in title:

            best_at = "Display & Performance"
            weakness = "Highly Competitive Market"

        elif "pixel" in title:

            best_at = "Camera & AI Features"
            weakness = "Lower Brand Perception"

        else:

            best_at = "General Product Quality"
            weakness = "Low Differentiation"

        comparisons.append({

            "Product": row["title"][:30],

            "Best At": best_at,

            "Weakness": weakness
        })

    return comparisons