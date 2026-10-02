
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Ripple",
    page_icon="🌊",
    layout="wide"
)
st.markdown("""
<style>
/* Main application background */
.stApp {
    background: #071426;
    color: #F2F7FF;
}

/* Main content spacing */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0B1B30;
    border-right: 1px solid #1D344D;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F2F7FF;
}

/* Headings */
h1, h2, h3 {
    color: #F2F7FF !important;
    letter-spacing: -0.5px;
}

/* Body text */
p, label, [data-testid="stCaptionContainer"] {
    color: #B4C5D9;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #10243A;
    border: 1px solid #1D3A55;
    padding: 20px;
    border-radius: 14px;
}

/* Buttons */
.stButton > button {
    background: #42D6F5;
    color: #071426;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

/* Input fields */
.stNumberInput input,
.stTextInput input {
    background: #10243A;
    color: #F2F7FF;
    border-radius: 8px;
}

/* Dividers */
hr {
    border-color: #1D344D;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #1D344D;
    border-radius: 10px;
    overflow: hidden;

}
/* Align the workspace cards */
[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}

[data-testid="stHorizontalBlock"] [data-testid="column"] {
    display: flex;
    flex-direction: column;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    height: 100%;
}

/* Keep card headings compact */
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size: 1.35rem !important;
    line-height: 1.35 !important;
}
</style>
""", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Simulation", "Analytics", "Recommendations"]
)

if page == "Overview":
    st.title("🌊 Ripple")
    st.subheader("Retail Decision Intelligence")
    st.write(
        "Turn inventory data into clearer decisions. "
        "Explore scenarios, track risk, and plan replenishment."
    )

    st.divider()
    st.subheader("📈 Simulation Overview")

    results = st.session_state.get("ripple_results", {})

    if results:
        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.metric(
                "Units Sold",
                f'{results["units_sold"]:,}'
            )

        with kpi2:
            st.metric(
                "Revenue",
                f'₹{results["revenue"]:,.0f}'
            )

        with kpi3:
            st.metric(
                "Stockout Days",
                results["stockout_days"]
            )
    else:
        st.info(
            "Run a simulation to see your inventory "
            "performance here."
        )

    st.divider()
    st.subheader("Your workspace")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("📦 Inventory")
            st.write("Understand stock levels and replenishment needs.")
            st.caption("Monitor inventory risk")

    with col2:
        with st.container(border=True):
            st.subheader("📈 Analytics")
            st.write("Explore demand, sales, and inventory trends.")
            st.caption("Understand performance")

    with col3:
        with st.container(border=True):
            st.subheader("💡 Next steps")
            st.write("Turn simulation results into practical next steps.")
            st.caption("Make informed decisions")

    st.divider()
    st.info(
        "Use **Simulation** in the sidebar to adjust your retail "
        "scenario and explore how different decisions affect outcomes."
    )

    st.caption("RIPPLE  /  RETAIL DECISION INTELLIGENCE")
    st.stop()

st.title("🌊 Ripple")
st.subheader("AI-Powered Retail Decision Simulator")

st.write(
    "Simulate retail inventory decisions and understand "
    "their impact on sales, stockouts, and profit."
)

st.sidebar.header("Retail Scenario")

starting_inventory = st.sidebar.slider(
    "Starting inventory (units)", 50, 1000, 300, step=50
)

daily_demand = st.sidebar.slider(
    "Average daily demand (units)", 5, 100, 30
)

lead_time = st.sidebar.slider(
    "Supplier delivery time (days)", 1, 14, 5
)

selling_price = st.sidebar.number_input(
    "Selling price per unit (₹)",
    min_value=1.0,
    value=500.0,
    step=50.0
)

unit_cost = st.sidebar.number_input(
    "Cost per unit (₹)",
    min_value=0.0,
    value=300.0,
    step=50.0
)

reorder_point = daily_demand * lead_time

inventory = starting_inventory
total_sold = 0
total_lost_sales = 0
total_orders = 0
pending_orders = []

records = []

rng = np.random.default_rng(42)

for day in range(1, 31):

    # Receive orders that have arrived
    arriving_orders = [
        order for order in pending_orders
        if order["arrival_day"] == day
    ]

    for order in arriving_orders:
        inventory += order["quantity"]

    pending_orders = [
        order for order in pending_orders
        if order["arrival_day"] != day
    ]

    # Simulate daily demand
    demand = max(
        0,
        int(rng.normal(daily_demand, daily_demand * 0.15))
    )

    sold = min(inventory, demand)
    lost_sales = demand - sold

    inventory -= sold
    total_sold += sold
    total_lost_sales += lost_sales

    # Reorder when inventory reaches the reorder point
    if inventory <= reorder_point and not pending_orders:
        order_quantity = daily_demand * (lead_time + 3)

        pending_orders.append({
            "quantity": order_quantity,
            "arrival_day": day + lead_time
        })

        total_orders += 1

    records.append({
        "Day": day,
        "Demand": demand,
        "Units Sold": sold,
        "Lost Sales": lost_sales,
        "Inventory": inventory
    })

df = pd.DataFrame(records)

revenue = total_sold * selling_price
cost_of_goods = total_sold * unit_cost
profit = revenue - cost_of_goods
stockout_days = int((df["Lost Sales"] > 0).sum())
st.session_state["ripple_results"] = {
    "units_sold": int(total_sold),
    "revenue": float(revenue),
    "stockout_days": int(stockout_days),
}
if page == "Analytics":
    st.title("📈 Analytics")
    st.write(
        "Understand sales performance, inventory movement, "
        "and unmet customer demand."
    )

    st.divider()

    # Key performance indicators
    col1, col2, col3 = st.columns(3)

    col1.metric("Units Sold", f"{total_sold:,}")
    col2.metric("Revenue", f"₹{revenue:,.0f}")
    col3.metric("Gross Profit", f"₹{profit:,.0f}")

    st.divider()

    # Inventory trend
    st.subheader("📦 Inventory Trend")
    st.line_chart(
        df,
        x="Day",
        y="Inventory"
    )

    # Demand versus sales
    st.subheader("📊 Demand vs Units Sold")
    st.line_chart(
        df,
        x="Day",
        y=["Demand", "Units Sold"]
    )

    # Lost sales
    st.subheader("⚠️ Unfulfilled Demand")
    st.bar_chart(
        df,
        x="Day",
        y="Lost Sales"
    )

    # Summary table
    st.subheader("Daily Performance")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Analytics are based on the current 30-day simulation. "
        "Change the scenario inputs to explore different outcomes."
    )

    st.stop()
st.divider()

st.subheader("30-Day Simulation Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Units Sold", f"{total_sold:,}")
col2.metric("Lost Sales (units)", f"{total_lost_sales:,}")
col3.metric("Revenue", f"₹{revenue:,.0f}")
col4.metric("Gross Profit", f"₹{profit:,.0f}")

st.subheader("Inventory Over Time")

st.line_chart(
    df,
    x="Day",
    y="Inventory"
)

st.subheader("Daily Simulation Data")

st.dataframe(df, use_container_width=True)

st.subheader("Scenario Insights")

st.write(f"**Reorder point:** {reorder_point} units")
st.write(f"**Supplier lead time:** {lead_time} days")
st.write(f"**Days with stockouts:** {stockout_days} out of 30")
st.write(f"**Orders placed:** {total_orders}")

if total_lost_sales > 0:
    st.warning(
        "Some customer demand could not be fulfilled. "
        "Consider increasing starting inventory or "
        "reducing supplier lead time."
    )
else:
    st.success(
        "All simulated customer demand was fulfilled."
    )

st.caption(
    "This is a simplified simulation. Demand is stochastic, "
    "and operating expenses, holding costs, and supplier "
    "capacity are not yet included."
)
st.subheader("Scenario Insights")

st.write(f"**Reorder point:** {reorder_point} units")
st.write(f"**Supplier lead time:** {lead_time} days")
st.write(f"**Days with stockouts:** {stockout_days} out of 30")
st.write(f"**Orders placed:** {total_orders}")
st.divider()

if page == "Recommendations":
    st.title("💡 Recommendations")
    st.write(
        "Actionable suggestions based on your 30-day "
        "retail simulation."
    )
    st.divider()
    st.subheader("📊 Ripple's Decision Recommendation")

    ending_inventory = int(df["Inventory"].iloc[-1])

    if total_lost_sales > 0:
        st.error("Stockout Risk Detected")

        st.write(
            f"Customers wanted to buy {total_lost_sales:,} "
            "more units than the store could supply."
        )

        st.write(
            "**Recommendation:** Consider increasing "
            "starting inventory or reducing supplier "
            "delivery time."
        )

    elif ending_inventory <= reorder_point:
        st.warning("Inventory Is Running Low")

        st.write(
            f"Your ending inventory is {ending_inventory:,} "
            "units, at or below the reorder point."
        )

        st.write(
            "**Recommendation:** Consider placing a "
            "replenishment order."
        )

    else:
        st.success("Inventory Levels Are Sufficient")

        st.write(
            f"The store fulfilled all simulated demand "
            f"and ended with {ending_inventory:,} units."
        )

        st.write(
            "**Recommendation:** Continue monitoring "
            "demand and inventory levels."
        )