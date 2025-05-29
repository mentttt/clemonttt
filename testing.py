import streamlit as st
import random
import time

# --- Constants ---
RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
ALL_NUMBERS = list(range(0, 37))
MAX_BET = 500

# --- Initialize Session State ---
if "balance" not in st.session_state:
    st.session_state.balance = 1000
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.total_spins = 0
    st.session_state.total_profit = 0

# --- Force Dark Mode Theme ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, .stText, .stMarkdown, .stCaption, .stSubheader {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🎡 Educational Roulette Game (RM Version)")
st.caption("Understand probability, risk, and gambling impact through play. Currency: RM")

# --- Sidebar Info ---
with st.sidebar:
    st.header("📘 Game Stats")
    st.write(f"💰 Balance: **RM{st.session_state.balance}**")
    st.write(f"🎯 Total Spins: {st.session_state.total_spins}")
    st.write(f"✅ Wins: {st.session_state.wins}")
    st.write(f"❌ Losses: {st.session_state.losses}")
    if st.session_state.total_spins > 0:
        win_rate = (st.session_state.wins / st.session_state.total_spins) * 100
        st.write(f"📈 Win Rate: **{win_rate:.2f}%**")
        st.write(f"📉 Profit/Loss: **RM{st.session_state.total_profit}**")

# --- Bet Controls ---
st.subheader("🎯 Place Your Bet")
bet_type = st.radio("Choose your bet type:", ["Red", "Black", "Number"])
if bet_type == "Number":
    chosen_number = st.number_input("Pick a number (0–36)", min_value=0, max_value=36)
else:
    chosen_number = None

bet_amount = st.slider("Bet amount (RM)", 1, MAX_BET, 10)

# --- Spin Button Logic ---
if st.button("🎲 Spin the Wheel"):
    if bet_amount > st.session_state.balance:
        st.warning("You don't have enough RM to place that bet.")
    else:
        with st.spinner("Spinning the wheel..."):
            spin_progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                spin_progress.progress(i + 1)

        result = random.choice(ALL_NUMBERS)
        color = "Green" if result == 0 else "Red" if result in RED_NUMBERS else "Black"
        st.write(f"🌀 The wheel landed on **{result} ({color})**")

        win = False
        payout = 0

        if bet_type == "Red" and result in RED_NUMBERS:
            win = True
            payout = bet_amount
        elif bet_type == "Black" and result in BLACK_NUMBERS:
            win = True
            payout = bet_amount
        elif bet_type == "Number" and result == chosen_number:
            win = True
            payout = bet_amount * 35

        st.session_state.total_spins += 1
        if win:
            st.session_state.wins += 1
            st.session_state.balance += payout
            st.session_state.total_profit += payout
            st.success(f"🎉 You won RM{payout}!")
        else:
            st.session_state.losses += 1
            st.session_state.balance -= bet_amount
            st.session_state.total_profit -= bet_amount
            st.error(f"❌ You lost RM{bet_amount}.")

# --- Simulation ---
if st.button("🚀 Simulate 100 Spins on Red"):
    red_hits = 0
    for _ in range(100):
        result = random.choice(ALL_NUMBERS)
        if result in RED_NUMBERS:
            red_hits += 1
    st.info(f"Out of 100 spins, Red won **{red_hits}** times (~{red_hits}%).")
    st.caption("This shows the randomness — results vary every time.")

# --- Educational Tip ---
st.markdown("---")
st.subheader("💡 Did You Know?")
fact = random.choice([
    "Roulette is called 'The Devil's Game' because numbers 1 to 36 add up to 666.",
    "European roulette has a 2.7% house edge due to the green zero.",
    "No betting system can beat the house in the long run.",
    "Gambling addiction can lead to serious personal and financial problems.",
    "Casinos are designed with no clocks or windows to keep players inside longer."
])
st.info(fact)

# --- Real-Time Gambling News (Static) ---
st.markdown("---")
st.subheader("📰 Latest Gambling News")

simple_news = [
    ("Gambling addiction concerns rise globally", "https://www.bbc.com/news/uk-56709589"),
    ("New roulette regulations discussed in EU", "https://www.theguardian.com/society/gambling"),
    ("Casinos worldwide report record revenues", "https://www.cnbc.com"),
]

for title, link in simple_news:
    st.markdown(f"- [{title}]({link})")

# --- Expected Value ---
st.markdown("---")
st.subheader("📉 Expected Value")
if bet_type == "Number":
    st.write("🎯 Betting on a single number:")
    st.latex("EV = (1/37) \\times 35 - (36/37) \\times 1 = -0.027 \\approx -2.7\\%")
else:
    st.write("🔴 Betting on red or black:")
    st.latex("EV = (18/37) \\times 1 - (19/37) \\times 1 = -0.027 \\approx -2.7\\%")
st.caption("Expected value shows you lose about RM0.027 for every RM1 bet. The house always wins in the long run.")

# --- Reset Button ---
if st.button("🔄 Reset Game"):
    st.session_state.balance = 1000
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.total_spins = 0
    st.session_state.total_profit = 0
    st.success("Game reset! Balance is now RM1000.")

# --- Real-Life Stories ---
st.markdown("---")
st.subheader("🎥 Real-Life Gambling Stories")

stories = {
    "Charles Wells": "Charles Wells 'broke the bank at Monte Carlo' in 1891, winning millions in today's money — but he lost it all and died broke.",
    "RM500,000 Loss": "In 2019, a Malaysian businessman reportedly lost RM500,000 in one night playing roulette in Marina Bay Sands, Singapore.",
    "Addiction Ruin": "A UK teacher developed a gambling addiction from online roulette, losing his house and marriage within 3 years.",
}

selected_story = st.selectbox("Choose a story", list(stories.keys()))
st.info(stories[selected_story])

# --- Quiz Section ---
st.markdown("---")
st.subheader("🎓 Roulette Knowledge Quiz")

quiz_data = [
    {
        "question": "What is the house edge in European roulette, and why does it exist?",
        "options": ["2.7%, due to the single 0", "5.26%, due to double 0", "0%, it’s a fair game", "1.35%, due to La Partage rule"],
        "answer": "2.7%, due to the single 0"
    },
    {
        "question": "If you bet RM100 on red and win, what do you walk away with?",
        "options": ["RM100 profit", "RM200 total (RM100 profit)", "RM135 total", "RM3500"],
        "answer": "RM200 total (RM100 profit)"
    },
    {
        "question": "What is the payout ratio for correctly guessing a single number?",
        "options": ["35 to 1", "17 to 1", "1 to 1", "2.7 to 1"],
        "answer": "35 to 1"
    },
    {
        "question": "Why do most players eventually lose over time?",
        "options": ["Luck runs out", "The wheel is rigged", "The house edge guarantees losses in the long run", "They don’t bet enough"],
        "answer": "The house edge guarantees losses in the long run"
    },
    {
        "question": "Which of the following is TRUE about roulette strategies?",
        "options": ["Martingale guarantees wins", "Strategies can change the odds", "No system beats the house edge", "Betting more increases your chances"],
        "answer": "No system beats the house edge"
    }
]

score = 0
for idx, quiz in enumerate(quiz_data):
    with st.expander(f"Q{idx+1}: {quiz['question']}"):
        user_answer = st.radio("Select your answer:", quiz["options"], key=f"quiz_{idx}")
        if user_answer:
            if user_answer == quiz["answer"]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error("❌ Incorrect.")
                st.info(f"✅ Correct answer: {quiz['answer']}")

st.markdown(f"### 🏑 Your Quiz Score: **{score}/{len(quiz_data)}**")

