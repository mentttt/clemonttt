import random

# List of roulette numbers with colors
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

# Function to spin the wheel
def spin_roulette():
    return random.choice(roulette_wheel)

# Game variables
money = 100
history = []

while money > 0:
    print("\n--- Roulette ---")
    print(f"You have ${money}")
    print("Bet types:")
    print(" - Type a number (0–36) to bet on a number (35x payout)")
    print(" - Type 'red' or 'black' to bet on a color (2x payout)")
    print(" - Type 'q' to quit")
    
    bet = input("What is your bet? ").lower()
    if bet == 'q':
        print("Thanks for playing!")
        break

    amount = input("How much do you want to bet? $")
    if not amount.isdigit():
        print("Please enter a valid number.")
        continue

    amount = int(amount)
    if amount > money or amount <= 0:
        print("You can't bet that amount.")
        continue

    result_number, result_color = spin_roulette()
    print(f"The ball landed on {result_number} ({result_color})")

    win = False
    payout = 0
    result = ""

    if bet.isdigit():
        if int(bet) < 0 or int(bet) > 36:
            print("Invalid number.")
            continue
        if bet == result_number:
            win = True
            payout = amount * 35
    elif bet in ["red", "black"]:
        if bet == result_color:
            win = True
            payout = amount * 2
    else:
        print("Invalid bet.")
        continue

    if win:
        print(f"🎉 You won ${payout}!")
        money += payout
        result = "WIN"
    else:
        print("❌ You lost.")
        money -= amount
        result = "LOSE"

    # Save the round to history
    history.append({
        "bet": bet,
        "amount": amount,
        "result_number": result_number,
        "result_color": result_color,
        "outcome": result,
        "money_left": money
    })

if money <= 0:
    print("You're out of money! Game over.")

# Show history
print("\n--- Betting History ---")
for i, round in enumerate(history, 1):
    print(f"Round {i}: Bet = {round['bet']}, Amount = ${round['amount']}, "
          f"Result = {round['result_number']} ({round['result_color']}), "
          f"Outcome = {round['outcome']}, Money left = ${round['money_left']}")
