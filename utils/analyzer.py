import altair as alt
import pandas as pd
import streamlit as st


def account_overview(df: pd.DataFrame) -> None:
    st.markdown("## Your Account in Review")

    expensive_purchase = df.loc[df["price"].idxmax()]
    largest_purchase = df.loc[df["amount"].idxmax()]
    most_purchases_month = (
        df.filter(["date", "amount"])
        .set_index("date")
        .groupby(pd.Grouper(freq="ME"))
        .size()
        .rename("purchases")
        .reset_index()
        .max()
    )

    st.metric(
        "Largest Purchase",
        f"{largest_purchase['amount']} items in {largest_purchase['date'].strftime('%d %B, %Y')}",
    )

    st.metric(
        "Most Expensive Purchase",
        f"$ {expensive_purchase['price']:,.2f} in {expensive_purchase['date'].strftime('%d %B, %Y')}",
    )

    st.metric(
        "Most Purchases in a Month",
        f"{most_purchases_month['purchases']} purchases in {most_purchases_month['date'].strftime('%B, %Y')}",
    )


def total_spending(df: pd.DataFrame) -> None:
    currencies = df.groupby(["currency"])["price"].sum()

    st.markdown("## Total Spending")

    for currency, value in currencies.to_dict().items():
        container = st.empty()
        if currencies.nunique() > 1:
            container = st.expander(f"{currency}", expanded=True)
        else:
            container = st.container()

        with container:
            st.metric("Total Amount", f"$ {value:,.2f}")
            data = (
                df.loc[df["currency"] == currency, ["date", "price"]]
                .sort_values("date")
                .set_index("date")
            )
            data = data.groupby(pd.Grouper(freq="ME")).sum().cumsum()

            st.altair_chart(
                alt.Chart(data.reset_index())
                .mark_area()
                .encode(
                    alt.X("date", axis=alt.Axis(format="%B %Y"), title="Date"),
                    alt.Y("price", axis=alt.Axis(format="$,.2f"), title="Total Spent"),
                ),
                use_container_width=True,
            )


def total_purchases(df: pd.DataFrame) -> None:
    st.markdown("## Total Purchases")

    with st.container():
        data = df.filter(["date", "amount"]).sort_values("date").set_index("date")
        data = data.groupby([pd.Grouper(freq="ME")]).count().cumsum()
        st.metric("Purchases Made", f"{len(data)}")

        st.altair_chart(
            alt.Chart(data.reset_index())
            .mark_area()
            .encode(
                alt.X("date", axis=alt.Axis(format="%B %Y"), title="Date"),
                alt.Y("amount", title="Items Purchased"),
            ),
            use_container_width=True,
        )


def monthly_spending(df: pd.DataFrame) -> None:
    currencies = df.groupby(["currency"])["price"].sum()

    st.markdown("## Monthly Purchases")

    for currency, value in currencies.to_dict().items():
        container = st.empty()
        if currencies.nunique() > 1:
            container = st.expander(f"{currency}", expanded=True)
        else:
            container = st.container()

        with container:
            data = (
                df.loc[df["currency"] == currency, ["date", "price", "amount"]]
                .sort_values("date")
                .set_index("date")
            )
            data = data.groupby(pd.Grouper(freq="ME")).sum()
            data = data.reset_index()

            st.altair_chart(
                alt.Chart(data, title="Amount Spent")
                .mark_bar()
                .encode(
                    alt.X("date", axis=alt.Axis(format="%B %Y"), title="Date"),
                    alt.Y("price", axis=alt.Axis(format="$,.2f"), title="Total Spent"),
                ),
                use_container_width=True,
            )

            st.altair_chart(
                alt.Chart(data, title="Items Bought")
                .mark_bar()
                .encode(
                    alt.X("date", axis=alt.Axis(format="%B %Y"), title="Date"),
                    alt.Y("amount", title="Items Purchased"),
                ),
                use_container_width=True,
            )
