import streamlit as st
import pandas as pd

# -----------------------------
# Page Setup
# -----------------------------

st.set_page_config(
    page_title="ByteBeat",
    page_icon="🌾",
    layout="wide"
)

# -----------------------------
# Initial Data
# -----------------------------

if "farmers" not in st.session_state:

    st.session_state.farmers = pd.DataFrame([
        {"Farmer": "Ahmad", "Location": "Perak", "Product": "Tomatoes", "Price": 4.5, "Stock": 100},
        {"Farmer": "Siti", "Location": "Johor", "Product": "Spinach", "Price": 3.0, "Stock": 80},
        {"Farmer": "Ravi", "Location": "Pahang", "Product": "Chili", "Price": 6.0, "Stock": 60},
        {"Farmer": "Lim", "Location": "Cameron Highlands", "Product": "Strawberries", "Price": 12.0, "Stock": 40}
    ])

if "orders" not in st.session_state:
    st.session_state.orders = []

# -----------------------------
# Title
# -----------------------------

st.title("🌾 ByteBeat Platform")
st.write("Connecting Farmers Directly to Urban Consumers")

# -----------------------------
# Sidebar Navigation
# -----------------------------

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Marketplace",
        "Farmer Dashboard",
        "Logistics Hub",
        "Analytics"
    ]
)

# -----------------------------
# Marketplace
# -----------------------------

if menu == "Marketplace":

    st.header("🛒 Fresh Produce Marketplace")

    farmers = st.session_state.farmers

    for i, row in farmers.iterrows():

        with st.container():

            col1, col2, col3 = st.columns([3,2,2])

            col1.subheader(row["Product"])
            col1.write(f"Farmer: {row['Farmer']}")
            col1.write(f"Location: {row['Location']}")

            col2.write(f"💰 Price: RM{row['Price']}")
            col2.write(f"📦 Stock: {row['Stock']}")

            qty = col3.number_input(
                "Quantity",
                min_value=0,
                key=f"qty{i}"
            )

            if col3.button("Pre-Order", key=f"order{i}"):

                if qty > 0:

                    order = {
                        "Product": row["Product"],
                        "Farmer": row["Farmer"],
                        "Quantity": qty,
                        "Price": row["Price"],
                        "Total": qty * row["Price"]
                    }

                    st.session_state.orders.append(order)

                    st.success("Order placed!")

# -----------------------------
# Farmer Dashboard
# -----------------------------

elif menu == "Farmer Dashboard":

    st.header("👨‍🌾 Farmer Dashboard")

    st.subheader("Current Produce Listings")

    st.dataframe(st.session_state.farmers)

    st.subheader("Add New Produce")

    name = st.text_input("Farmer Name")
    location = st.text_input("Farm Location")
    product = st.text_input("Product Name")
    price = st.number_input("Price (RM)")
    stock = st.number_input("Stock (kg)")

    if st.button("Add Listing"):

        new_row = {
            "Farmer": name,
            "Location": location,
            "Product": product,
            "Price": price,
            "Stock": stock
        }

        st.session_state.farmers.loc[len(st.session_state.farmers)] = new_row

        st.success("New produce listed!")

# -----------------------------
# Logistics Hub
# -----------------------------

elif menu == "Logistics Hub":

    st.header("🚚 Urban Distribution Hub")

    orders = st.session_state.orders

    if len(orders) == 0:

        st.info("No orders yet")

    else:

        df = pd.DataFrame(orders)

        st.subheader("Orders to Deliver")

        st.dataframe(df)

        st.subheader("Delivery Flow")

        for order in orders:

            st.write(
                f"🌾 {order['Quantity']}kg {order['Product']} "
                f"from {order['Farmer']} → Klang Valley Hub → Customer"
            )

# -----------------------------
# Analytics
# -----------------------------

elif menu == "Analytics":

    st.header("📊 ByteBeat Analytics")

    orders = st.session_state.orders

    if len(orders) == 0:

        st.info("No analytics yet")

    else:

        df = pd.DataFrame(orders)

        total_sales = df["Total"].sum()
        total_orders = len(df)

        col1, col2 = st.columns(2)

        col1.metric("Total Revenue", f"RM {total_sales}")
        col2.metric("Total Orders", total_orders)

        st.subheader("Demand by Product")

        demand = df.groupby("Product")["Quantity"].sum()

        st.bar_chart(demand)
