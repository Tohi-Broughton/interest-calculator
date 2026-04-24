import streamlit as st

st.set_page_config(page_title="Interest Calculator", page_icon="💰", layout="wide")

CURRENCY_OPTIONS = {
    "GBP (£)": {"symbol": "£"},
    "USD ($)": {"symbol": "$"},
    "EUR (€)": {"symbol": "€"},
    "JPY (¥)": {"symbol": "¥"},
    "CAD (C$)": {"symbol": "C$"},
    "AUD (A$)": {"symbol": "A$"},
    "NZD (NZ$)": {"symbol": "NZ$"},
    "CHF (CHF)": {"symbol": "CHF "},
    "SEK (kr)": {"symbol": "kr "},
    "NOK (kr)": {"symbol": "kr "},
    "DKK (kr)": {"symbol": "kr "},
    "INR (₹)": {"symbol": "₹"},
    "CNY (¥)": {"symbol": "¥"},
    "HKD (HK$)": {"symbol": "HK$"},
    "SGD (S$)": {"symbol": "S$"},
    "ZAR (R)": {"symbol": "R "},
}

COMPOUNDING_FREQUENCIES = {
    "Annually": 1,
    "Semi-annually": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365,
}

PAYMENT_FREQUENCIES = {
    "Annually": 1,
    "Semi-annually": 2,
    "Quarterly": 4,
    "Monthly": 12,
}

INTEREST_TYPES = ["Simple", "Compound"]
PAYMENT_TIMINGS = ["End of Period", "Beginning of Period"]


def simple_lump_sum(p, r, t):
    return p * (1 + r * t)


def compound_lump_sum(p, r, t, n):
    return p * (1 + r / n) ** (n * t)


def compound_payments_end(pmt, r, t, n, m):
    g = (1 + r / n) ** (n / m)
    return pmt * ((g ** (m * t)) - 1) / (g - 1)


def compound_payments_beginning(pmt, r, t, n, m):
    g = (1 + r / n) ** (n / m)
    return compound_payments_end(pmt, r, t, n, m) * g


# Initialize session state defaults
defaults = {
    "interest_type": "Simple",
    "currency_label": "GBP (£)",
    "payment_timing": "End of Period",
    "compounding_frequency_label": "Annually",
    "payment_frequency_label": "Monthly",
    "initial_amount": 200.0,
    "years": 5.0,
    "interest_rate_pct": 10.0,
    "recurring_payments": 0.0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def handle_interest_type_change():
    if st.session_state.interest_type == "Simple":
        st.session_state.recurring_payments = 0.0


st.title("💰 Interest Calculator")
st.caption("Use the calculator below to calculate potential earnings on your investments.")

left_col, right_col = st.columns([1.25, 0.95], gap="large")

with left_col:
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox(
            "Interest Type",
            INTEREST_TYPES,
            key="interest_type",
            on_change=handle_interest_type_change,
        )
    with c2:
        st.selectbox(
            "Currency",
            list(CURRENCY_OPTIONS.keys()),
            key="currency_label",
        )

    c3, c4, c5 = st.columns(3)
    with c3:
        st.selectbox(
            "Payment Timing",
            PAYMENT_TIMINGS,
            key="payment_timing",
            disabled=(st.session_state.interest_type == "Simple"),
            help="Only used for compound calculations with recurring payments.",
        )
    with c4:
        st.selectbox(
            "Compounding Frequency",
            list(COMPOUNDING_FREQUENCIES.keys()),
            key="compounding_frequency_label",
            disabled=(st.session_state.interest_type == "Simple"),
            help="Only used for compound calculations.",
        )
    with c5:
        st.selectbox(
            "Payment Frequency",
            list(PAYMENT_FREQUENCIES.keys()),
            key="payment_frequency_label",
            disabled=(st.session_state.interest_type == "Simple"),
            help="Only used for compound calculations with recurring payments.",
        )

    c6, c7 = st.columns(2)
    with c6:
        st.number_input(
            "Initial Amount",
            min_value=0.0,
            step=50.0,
            key="initial_amount",
        )
    with c7:
        st.number_input(
            "Years",
            min_value=0.0,
            step=1.0,
            key="years",
        )

    c8, c9 = st.columns(2)
    with c8:
        st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            step=1.0,
            key="interest_rate_pct",
        )
    with c9:
        st.number_input(
            "Recurring Payments",
            min_value=0.0,
            step=50.0,
            key="recurring_payments",
            disabled=(st.session_state.interest_type == "Simple"),
        )

interest_type = st.session_state.interest_type
currency_label = st.session_state.currency_label
payment_timing = st.session_state.payment_timing
compounding_frequency_label = st.session_state.compounding_frequency_label
payment_frequency_label = st.session_state.payment_frequency_label
initial_amount = st.session_state.initial_amount
years = st.session_state.years
interest_rate_pct = st.session_state.interest_rate_pct
recurring_payments = st.session_state.recurring_payments

has_payments = recurring_payments > 0

r = interest_rate_pct / 100
n = COMPOUNDING_FREQUENCIES[compounding_frequency_label]
m = PAYMENT_FREQUENCIES[payment_frequency_label]
currency_symbol = CURRENCY_OPTIONS[currency_label]["symbol"]

result = None
message = ""
formula_used = ""

if interest_rate_pct <= 0:
    message = "Enter an interest rate greater than 0."
elif years <= 0:
    message = "Enter years greater than 0."
elif initial_amount == 0 and recurring_payments == 0:
    message = "Enter an Initial Amount or Recurring Payments."
else:
    if interest_type == "Simple":
        if initial_amount > 0:
            result = simple_lump_sum(initial_amount, r, years)
            formula_used = "Simple lump sum"
        else:
            message = "Enter an Initial Amount greater than 0 for Simple interest."
    else:
        if initial_amount > 0 and recurring_payments == 0:
            result = compound_lump_sum(initial_amount, r, years, n)
            formula_used = "Compound lump sum"
        elif initial_amount == 0 and recurring_payments > 0:
            if payment_timing == "End of Period":
                result = compound_payments_end(recurring_payments, r, years, n, m)
                formula_used = "Compound recurring payments (end of period)"
            else:
                result = compound_payments_beginning(recurring_payments, r, years, n, m)
                formula_used = "Compound recurring payments (beginning of period)"
        elif initial_amount > 0 and recurring_payments > 0:
            if payment_timing == "End of Period":
                result = compound_lump_sum(initial_amount, r, years, n) + compound_payments_end(
                    recurring_payments, r, years, n, m
                )
                formula_used = "Compound lump sum + recurring payments (end of period)"
            else:
                result = compound_lump_sum(initial_amount, r, years, n) + compound_payments_beginning(
                    recurring_payments, r, years, n, m
                )
                formula_used = "Compound lump sum + recurring payments (beginning of period)"

total_contributed = initial_amount
if interest_type == "Compound" and recurring_payments > 0:
    total_contributed += recurring_payments * m * years

with right_col:
    if result is not None:
        profit = result - total_contributed

        st.subheader("Results")
        st.metric("Future Value", f"{currency_symbol}{result:,.2f}")
        st.metric("Total Contributed", f"{currency_symbol}{total_contributed:,.2f}")
        st.metric("Profit", f"{currency_symbol}{profit:,.2f}")

    else:
        st.info(message or "Enter values to calculate.")

st.divider()

with st.expander("How it works"):
    st.markdown(
        """
- Choose **Simple** or **Compound** first.
- **Simple** works for lump sums only.
- **Compound** works for an initial amount, recurring payments, or both.
- **Recurring Payments** is disabled and reset to 0 when **Simple** is selected.
- **Payment Timing** only matters when recurring payments are above 0 for compound calculations.
- **Compounding Frequency** only matters for compound calculations.
- **Payment Frequency** only matters when recurring payments are above 0 for compound calculations.
- **Total Contributed** = Initial Amount + all recurring payments made.
- **Profit** = Future Value − Total Contributed.
- **Currency** changes the display symbol only. It does not convert values.
        """
    )