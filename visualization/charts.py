import plotly.express as px
import pandas as pd


def revenue_chart(df):

    chart_df = df.copy()

    chart_df["short_title"] = chart_df["title"].apply(
        lambda x: x[:22] + "..."
        if len(x) > 22 else x
    )

    fig = px.bar(

        chart_df,

        x="short_title",

        y="estimated_revenue",

        text="estimated_revenue"
    )

    fig.update_traces(

        texttemplate='₹%{text:,.0f}',

        textposition='outside'
    )

    fig.update_layout(

        height=500,

        xaxis_title="Products",

        yaxis_title="Revenue (₹)",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=12
        ),

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=120
        ),

        xaxis=dict(
            tickangle=-25
        )
    )

    return fig

def sentiment_chart(sentiment):

    sentiment_df = pd.DataFrame({

        "Sentiment": list(sentiment.keys()),

        "Count": list(sentiment.values())
    })

    fig = px.pie(

        sentiment_df,

        names="Sentiment",

        values="Count",

        hole=0.45
    )

    fig.update_traces(

        textinfo="percent+label"
    )

    fig.update_layout(

        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        height=420
    )

    return fig