import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from pocket import Pocket

# Player parameters:
balance = 0
bet_amount = 0

# Simulation parameters:
num_games = 1000
num_win = 0

# American wheel:
AMERICAN = set([
        Pocket(1, "Red"), Pocket(2, "Black"), Pocket(3, "Red"), Pocket(4, "Black"),
        Pocket(5, "Red"), Pocket(6, "Black"), Pocket(7, "Red"), Pocket(8, "Black"),
        Pocket(9, "Red"), Pocket(10, "Black"), Pocket(11, "Black"), Pocket(12, "Red"),
        Pocket(13, "Black"), Pocket(14, "Red"), Pocket(15, "Black"), Pocket(16, "Red"),
        Pocket(17, "Black"), Pocket(18, "Red"), Pocket(19, "Red"), Pocket(20, "Black"),
        Pocket(21, "Red"), Pocket(22, "Black"), Pocket(23, "Red"), Pocket(24, "Black"),
        Pocket(25, "Red"), Pocket(26, "Black"), Pocket(27, "Red"), Pocket(28, "Black"),
        Pocket(29, "Black"), Pocket(30, "Red"), Pocket(31, "Black"), Pocket(32, "Red"),
        Pocket(33, "Black"), Pocket(34, "Red"), Pocket(35, "Black"), Pocket(36, "Red"),
        Pocket(0, "Green"), Pocket(-1, "Green")
    ])

# Resets player parameters to desired values:
def reset_player_param(amount, bet):
    global balance, bet_amount
    balance = amount
    bet_amount = bet

# Resets simulation parameters to desired values:
def reset_sim_param(rounds, games):
    global num_rounds, num_games, num_win
    num_rounds = rounds
    num_games = games
    num_win = 0

# Returns a random pocket object from a wheel.
def spin_wheel(wheel):
    return random.choice(tuple(wheel))

# Returns which section a number corresponds to. 
# 1: (1-12), 2: (13-24), and 3: (25-36)
def get_section(number):
    if number <= 12:
        return 1
    elif number >= 13 and number <= 24:
        return 2
    else:
        return 3

# Returns an array of n samples for a roulette table.
def sample_table(num_samples):
    global AMERICAN
    samples = []
    for n in range(num_samples):
        value = spin_wheel(AMERICAN)
        samples.append(value.get_number())
    return samples

# Iterates over an array of samples and determines which frequency is the largest.
# Returns the largest fequency and its probability as a tuple
def get_frequency(samples):
    freq = [0, 0, 0]
    for s in samples:
        section = get_section(s)
        index = section - 1
        freq[index] = freq[index] + 1
    largest_section = freq.index(max(freq))
    p_largest_section = freq[largest_section]/len(samples)
    return (largest_section + 1, p_largest_section)
    

"""
Strategy 1:
Similar to Martingale betting strategy. The steps:
1. Choose a (approximate) 50/50 bet such as color, odd/even, or low/high and stick with this
   choice for n rounds. In this particular case, we are choosing one color, red.
2. Place a bet k for that choice.
3. If that bet is successful keep k the same. If the bet is not successful increase your bet
   for the next round to k = 2 * k (double it)
4. Quit if your bet amount is greater than your current balance.
5. Leave the game if current balance is greater than your starting balance by a difference of 'd'. 
"""
def strategy_one(sbal, sbet, numr):
    global balance, bet_amount, num_win, AMERICAN
    starting_balance = sbal
    starting_bet = sbet
    num_rounds = numr
    bet_choice = "Red"

    reset_player_param(starting_balance, starting_bet)

    for r in range(num_rounds):
        # Place bet:
        balance = balance - bet_amount

        # Spin wheel:
        spin_result = spin_wheel(AMERICAN)

        # Checking the color of the pocket:
        if bet_choice != spin_result.get_color():
            # Loss:
            bet_amount = bet_amount * 2
            if bet_amount > balance:
                break
        else:
            # Won:
            balance = balance + (bet_amount * 2)
            bet_amount = starting_bet
    return balance

"""
Strategy 2:
Even though spins are independent to one another, here are the steps to this strategy:
1. Sample a table n times and determine which section is most fequent. 
2. If largest frequency is greater than 0.6, continue. Otherwise, repeat step 1.
3. Place bet k on the seciton determined from steps 1 and 2.
4. If successful repeat 3 with same bet k. If loss, increase k to k + 10.
5. If losses are greater than 4, stop playing. 
"""
def strategy_two(sbal, sbet, nums, p):
    global balance, bet_amount, num_win, AMERICAN
    starting_balance = sbal
    starting_bet = sbet
    num_samples = nums
    freq_p = p
    chosen_section = 0

    reset_player_param(starting_balance, starting_bet)

    while True:
        section = get_frequency(sample_table(num_samples))
        if section[1] >= freq_p:
            chosen_section = section[0]
            break
    
    while True:
        balance = balance - bet_amount
        spin_result = spin_wheel(AMERICAN)
        if chosen_section == get_section(spin_result.get_number()):
            balance = balance + (bet_amount * 3)
            bet_amount = starting_bet
            break
        else:
            bet_amount = bet_amount + 100
            if bet_amount > 500:
                break
    return balance

# Simulator workhorse:
if __name__ == "__main__":
    # Local parameters:
    starting_balance = 2000
    starting_bet = 100
    num_rounds = 30

    total = 0
    highest_return = 0
    data = []

    print("Game Summary")
    print("Starting Balance: ", '${:,.2f}'.format(starting_balance))
    print("Starting Bet Amount: ", '${:,.2f}'.format(starting_bet))
    print("Number of Rounds: ", num_rounds)
    print("Bet Choice: Red")
    print()

    for g in range(num_games):
        game = strategy_two(starting_balance, starting_bet, 10, 0.7)
        data.append(game)
        if game > highest_return:
            highest_return = game
        total = total + game
        if game > starting_balance:
            num_win = num_win + 1
    
    new_data = np.array(data)
    avg = total/num_games

    print(num_win)
    print("Average balance: ", '${:,.2f}'.format(avg))
    print("Highest return: ", '${:,.2f}'.format(highest_return))

    plt.plot(new_data)
    plt.show()


