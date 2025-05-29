import streamlit as st
import random
import time

# Roulette wheel numbers and colors
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

# Initialize session state variables
if 'money' not in st.session_state:
    st.session_state.money = 100

if 'history' not in st.session_state:
    st.session_state.history = []

if 'bets' not in st.session_state:
    st.session_state.bets = {}

st.title("🎰 Advanced Roulette Game (Streamlit)")

st.write(f"Your money: **${st.session_state.money}**")

st.markdown("### Place your bets (enter amount for each bet):")

# BET TYPES
bet_types = {
    "Numbers (0-36)": [str(i) for i in range(37)],
    "Colors": ["red", "black"],
    "Odd/Even": ["odd", "even"],
    "Low/High": ["1-18", "19-36"]
}

new_bets = {}

def validate_amount(amount_str):
    try:
        amount = int(amount_str)
        if amount > 0:
            return amount
        else:
            return None
    except:
        return None

# For each bet type, let user input bets and amounts
for category, options in bet_types.items():
    if category == "Numbers (0-36)":
        continue  # Skip this part; we already rendered a better grid above

    st.markdown(f"**{category}**")
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        with cols[i]:
            selected = st.checkbox(option, key=f"{category}_{option}")
            if selected:
                amt = st.text_input(f"Bet amount for {option}", key=f"amt_{category}_{option}", value="0", max_chars=5)
                amount = validate_amount(amt)
                if amount is None:
                    st.error("Enter a positive integer")
                else:
                    new_bets[option] = amount


total_bet_amount = sum(new_bets.values())

if total_bet_amount > st.session_state.money:
    st.error(f"Total bet amount ${total_bet_amount} exceeds your money ${st.session_state.money}!")

if st.button("Place Bets"):
    if total_bet_amount == 0:
        st.warning("Please place at least one bet with positive amount.")
    elif total_bet_amount > st.session_state.money:
        st.error("Not enough money for these bets.")
    else:
        for bet, amt in new_bets.items():
            if bet in st.session_state.bets:
                st.session_state.bets[bet] += amt
            else:
                st.session_state.bets[bet] = amt
        st.success(f"Placed bets totaling ${total_bet_amount}.")
        st.rerun()  # Updated from experimental_rerun

# Show current bets
if st.session_state.bets:
    st.write("### Current Bets:")
    for bet, amt in st.session_state.bets.items():
        st.write(f"- {bet}: ${amt}")

# Main spin button
if st.button("Spin"):
    if not st.session_state.bets:
        st.warning("Place some bets first!")
    else:
        # ✅ FIXED spinning text (one line animation)
        placeholder = st.empty()
        for i in range(6):
            dots = '⚫' * (i % 4)
            placeholder.markdown(f"### Spinning... {dots}")
            time.sleep(0.3)

        result_number, result_color = spin_roulette()
        st.write(f"🎉 The ball landed on **{result_number}** ({result_color})")

        total_win = 0
        round_results = []

        def is_odd(n):
            return int(n) % 2 == 1

        def is_low(n):
            return 1 <= int(n) <= 18

        for bet, amt in st.session_state.bets.items():
            win = False
            payout = 0

            if bet.isdigit():
                if bet == result_number:
                    win = True
                    payout = amt * 35
            elif bet in ["red", "black"]:
                if bet == result_color:
                    win = True
                    payout = amt * 2
            elif bet == "odd":
                if result_number.isdigit() and is_odd(result_number) and result_number != "0":
                    win = True
                    payout = amt * 2
            elif bet == "even":
                if result_number.isdigit() and not is_odd(result_number) and result_number != "0":
                    win = True
                    payout = amt * 2
            elif bet == "1-18":
                if result_number.isdigit() and is_low(result_number):
                    win = True
                    payout = amt * 2
            elif bet == "19-36":
                if result_number.isdigit() and not is_low(result_number) and result_number != "0":
                    win = True
                    payout = amt * 2

            if win:
                total_win += payout
                round_results.append(f"Bet on {bet} for ${amt} → WIN ${payout}")
            else:
                total_win -= amt
                round_results.append(f"Bet on {bet} for ${amt} → LOSE")

        st.write("### Round results:")
        for r in round_results:
            st.write(r)

        st.session_state.money += total_win
        st.write(f"**Total this round: {'+' if total_win >= 0 else ''}{total_win}**")
        st.write(f"**Money left: ${st.session_state.money}**")

        st.session_state.history.append({
            "bets": st.session_state.bets.copy(),
            "result_number": result_number,
            "result_color": result_color,
            "round_win": total_win,
            "money_left": st.session_state.money
        })

        st.session_state.bets.clear()

        if st.session_state.money <= 0:
            st.error("You're out of money! Game over.")
            st.stop()

# Show game history
if st.session_state.history:
    st.write("## Game History")
    for i, round in enumerate(st.session_state.history, 1):
        bets_desc = ", ".join([f"{k}: ${v}" for k, v in round["bets"].items()])
        st.write(f"Round {i}: Bets: {bets_desc} | Result: {round['result_number']} ({round['result_color']}) | "
                 f"Round Win: {round['round_win']} | Money Left: {round['money_left']}")

