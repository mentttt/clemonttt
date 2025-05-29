import streamlit as st
import random

st.title("🎰 Roulette Game")

# Initialize session state
if "money" not in st.session_state:
    st.session_state.money = 100
    st.session_state.history = []

# Roulette wheel
roulette_wheel = [
    ("0", "green"), ("1", "red"), ("2", "black"), ("3", "red"), ("4", "black"),
    ("5", "red"), ("6", "black"), ("7", "red"), ("8", "black"), ("9", "red"),
    ("10", "black"), ("11", "black"), ("12", "red"), ("13", "black"), ("14", "red"),
    ("15", "black"), ("16", "red"), ("17", "black"), ("18", "red"), ("19", "red"),
    ("20", "black"), ("21", "red"), ("22", "black"), ("23", "red"), ("24", "black"),
    ("25", "red"), ("26", "black"), ("27", "red"), ("28", "black"), ("29", "black"),
    ("30", "red"), ("31", "black"), ("32", "red"), ("33", "black"), ("34", "red"),
    ("35", "black"), ("36", "red")
]

def spin_roulette():
    return random.choice(roulette_wheel)

st.write(f"💰 You have **${st.session_state.money}**")

bet_type = st.radio("Choose your bet type:", ["Number (0–36)", "Color (red/black)"])
if bet_type == "Number (0–36)":
    bet = st.number_input("Enter a number to bet on:", min_value=0, max_value=36, step=1)
    bet = str(bet)
else:
    bet = st.selectbox("Choose a color:", ["red", "black"])

amount = st.number_input("Enter bet amount:", min_value=1, max_value=st.session_state.money, step=1)

if st.button("Spin the Wheel 🎡"):
    result_number, result_color = spin_roulette()
    win = False
    payout = 0
    result = ""

    if bet.isdigit():
        if bet == result_number:
            win = True
            payout = amount * 35
    elif bet in ["red", "black"]:
        if bet == result_color:
            win = True
            payout = amount * 2

    st.write(f"The ball landed on **{result_number} ({result_color})**")

    if win:
        st.success(f"🎉 You won ${payout}!")
        st.session_state.money += payout
        result = "WIN"
    else:
        st.error("❌ You lost.")
        st.session_state.money -= amount
        result = "LOSE"

    st.session_state.history.append({
        "bet": bet,
        "amount": amount,
        "result_number": result_number,
        "result_color": result_color,
        "outcome": result,
        "money_left": st.session_state.money
    })

# Game Over
if st.session_state.money <= 0:
    st.warning("You're out of money! Game over.")

# Betting history
if st.session_state.history:
    st.subheader("📜 Betting History")
    for i, round in enumerate(st.session_state.history, 1):
        st.markdown(f"**Round {i}:** Bet = {round['bet']}, Amount = ${round['amount']}, "
                    f"Result = {round['result_number']} ({round['result_color']}), "
                    f"Outcome = {round['outcome']}, Money left = ${round['money_left']}")
