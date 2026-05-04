# =====================================================
# MONTHLY SALES ESTIMATION
# =====================================================

def estimate_monthly_sales(
    review_count,
    rating
):

    # Conservative ecommerce estimate
    estimated_sales = int(
        review_count * 0.003
    )

    return estimated_sales


# =====================================================
# REVENUE ESTIMATION
# =====================================================

def estimate_revenue(
    price,
    estimated_sales
):

    estimated_revenue = int(
        price * estimated_sales
    )

    return estimated_revenue