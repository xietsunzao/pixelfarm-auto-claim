from datetime import datetime, timedelta
from colorama import Fore, init
import time


# Define the fruit fall rates (fruits per second) for each tree type
FRUIT_RATES = {
    'plum': 0.1,
    'orange': 0.1,
    'apple': 0.05,
    'cherry': 0.05
}

CHECK_INTERVAL = 60  # Check every 60 seconds

# Define tree expiration periods (example: 30 days for non-plum trees)
TREE_EXPIRATION_DAYS = {
    'plum': None,  # Plum tree doesn't expire
    'orange': 30,
    'apple': 30,
    'cherry': 30
}

# Get the farming session duration based on the total number of trees
def get_farming_session_duration(total_trees):
    if total_trees > 1:
        return timedelta(hours=12)
    else:
        return timedelta(hours=4)


def should_harvest(tree):
    last_claimed = datetime.fromisoformat(tree['last_claimed_at'][:-1])
    time_diff = datetime.utcnow() - last_claimed
    # Assuming trees can be harvested every hour
    return time_diff >= timedelta(hours=1)

def is_tree_expired(tree_type, created_at):
    if TREE_EXPIRATION_DAYS.get(tree_type) is None:
        return False  # Plum tree doesn't expire
    created = datetime.fromisoformat(created_at[:-1])
    expiration_period = timedelta(days=TREE_EXPIRATION_DAYS[tree_type])
    return (datetime.utcnow() - created) > expiration_period

def display_tree_info(tree_type, fruit_total, ready_for_harvest, fruits_fall, expired=False):
    label = Fore.RED + "(Expired)" if expired else ""
    print(Fore.CYAN + f"Tree Type: {tree_type.capitalize()} {label}")
    print(Fore.CYAN + f"Total Fruit: {fruit_total}")
    print(Fore.CYAN + f"Fruits to Fall: {fruits_fall}")
    if ready_for_harvest:
        print(Fore.YELLOW + f"Tree {tree_type.capitalize()} is ready for harvest.")
    else:
        print(Fore.BLUE + f"Tree {tree_type.capitalize()} is not ready for harvest.")
    print(Fore.CYAN + "----------------------------------------")


def calculate_remaining_time(last_claimed_at, farming_session_duration):
    last_claimed = datetime.fromisoformat(last_claimed_at[:-1])
    now = datetime.utcnow()
    time_since_last_claim = now - last_claimed
    remaining_time = farming_session_duration - time_since_last_claim
    return remaining_time if remaining_time > timedelta(0) else timedelta(0)

def calculate_fruits_fall(tree_type, last_claimed_at):
    if tree_type not in FRUIT_RATES:
        return 0
    last_claimed = datetime.fromisoformat(last_claimed_at[:-1])
    now = datetime.utcnow()
    time_elapsed = now - last_claimed
    fruits_fall = FRUIT_RATES[tree_type] * time_elapsed.total_seconds()
    return int(fruits_fall)

def display_user_info(username, total_gems, total_trees, remaining_time):
    print(Fore.GREEN + "----------------------------------------")
    print(Fore.GREEN + f"Username     : {username}")
    print(Fore.GREEN + f"Total Gems   : {total_gems:.2f}")
    print(Fore.GREEN + f"Number of Trees: {total_trees}")
    print(Fore.GREEN + f"Farming Session Remaining: {str(remaining_time).split('.')[0]}")  # Remove milliseconds
    print(Fore.GREEN + "----------------------------------------")

def display_tree_info(tree_type, fruit_total, ready_for_harvest, fruits_fall, expired=False):
    label = Fore.RED + "(Expired)" if expired else ""
    print(Fore.CYAN + f"Tree Type: {tree_type.capitalize()} {label}")
    print(Fore.CYAN + f"Total Fruit: {fruit_total}")
    print(Fore.CYAN + f"Fruits to Fall: {fruits_fall}")
    if ready_for_harvest:
        print(Fore.YELLOW + f"Tree {tree_type.capitalize()} is ready for harvest.")
    else:
        print(Fore.BLUE + f"Tree {tree_type.capitalize()} is not ready for harvest.")
    print(Fore.CYAN + "----------------------------------------")


def countdown_timer(seconds):
    while seconds > 0:
        time_left = str(timedelta(seconds=seconds)).split(".")[0]  # Display only HH:MM:SS
        print(Fore.YELLOW + f"\rWaiting for the next session: {time_left}", end="")
        time.sleep(1)
        seconds -= 1
    print()  # Newline after the countdown ends