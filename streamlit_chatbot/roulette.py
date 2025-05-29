import streamlit as st
import random
import time

# Roulette numbers and their colors
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

# Initialize game state
if 'money' not in st.session_state:
    st.session_state.money = 100
if 'bets' not in st.session_state:
    st.session_state.bets = {}
if 'history' not in st.session_state:
    st.session_state.history = []

# Game title
st.title("🎰 Simple Roulette Game")

# Show player's money
st.write(f"**Money: ${st.session_state.money}**")

# BETTING SECTION
st.markdown("### Place your bets")

bet_types = {
    "Number (0-36)": [str(i) for i in range(37)],
    "Color": ["red", "black"],
    "Odd/Even": ["odd", "even"],
    "Low/High": ["1-18", "19-36"]
}

new_bets = {}

# Function to check if the input is a positive number
def is_valid_amount(value):
    try:
        amount = int(value)
        return amount > 0
    except:
        return False

# Collect bets
for category, options in bet_types.items():
    st.markdown(f"**{category}**")
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        with cols[i]:
            check = st.checkbox(option, key=f"{category}_{option}")
            if check:
                value = st.text_input(f"${option}", key=f"{option}_input", value="0")
                if is_valid_amount(value):
                    new_bets[option] = int(value)
                else:
                    st.error("Enter a positive number")

# Show total bets
total_bet = sum(new_bets.values())
if total_bet > st.session_state.money:
    st.error("You don't have enough money for these bets!")

# Button to place bets
if st.button("Place Bets"):
    if total_bet == 0:
        st.warning("Please bet something.")
    elif total_bet > st.session_state.money:
        st.error("Not enough money!")
    else:
        for bet, amount in new_bets.items():
            st.session_state.bets[bet] = amount
        st.success("Bets placed!")
        st.experimental_rerun()

# Show current bets
if st.session_state.bets:
    st.write("### Current Bets:")
    for bet, amt in st.session_state.bets.items():
        st.write(f"- {bet}: ${amt}")

# SPIN BUTTON
if st.button("Spin the Wheel"):
    if not st.session_state.bets:
        st.warning("Please place bets first!")
    else:
        # Show fake spinning animation
        with st.spinner("Spinning the wheel..."):
            time.sleep(2)

        # Choose random number from wheel
        result_number, result_color = random.choice(roulette_wheel)
        st.success(f"🎯 Ball landed on **{result_number}** ({result_color})")

        # Calculate winnings
        total_win = 0
        results = []

        def is_odd(n): return int(n) % 2 == 1
        def is_low(n): return 1 <= int(n) <= 18

        for bet, amt in st.session_state.bets.items():
            win = False
            payout = 0

            # Number bet
            if bet.isdigit() and bet == result_number:
                win = True
                payout = amt * 35

            # Color
            elif bet in ["red", "black"] and bet == result_color:
                win = True
                payout = amt * 2

            # Odd/Even
            elif bet == "odd" and result_number.isdigit() and is_odd(result_number):
                win = True
                payout = amt * 2
            elif bet == "even" and result_number.isdigit() and not is_odd(result_number):
                win = True
                payout = amt * 2

            # Low/High
            elif bet == "1-18" and result_number.isdigit() and is_low(result_number):
                win = True
                payout = amt * 2
            elif bet == "19-36" and result_number.isdigit() and not is_low(result_number):
                win = True
                payout = amt * 2

            if win:
                total_win += payout
                results.append(f"✅ Bet on {bet} → Win ${payout}")
            else:
                total_win -= amt
                results.append(f"❌ Bet on {bet} → Lose ${amt}")

        # Show results
        st.markdown("### Round Results")
        for r in results:
            st.write(r)

        # Update money
        st.session_state.money += total_win
        st.write(f"**Money now: ${st.session_state.money}**")

        # Save history
        st.session_state.history.append({
            "bets": st.session_state.bets.copy(),
            "result": f"{result_number} ({result_color})",
            "total_win": total_win,
            "money": st.session_state.money
        })

        # Reset bets
        st.session_state.bets.clear()

        # Game over
        if st.session_state.money <= 0:
            st.error("You're out of money! Game over.")

# Show game history
if st.session_state.history:
    st.markdown("## History")
    for i, h in enumerate(st.session_state.history, 1):
        st.write(f"Round {i}: {h['result']} | Win: ${h['total_win']} | Money: ${h['money']}")

