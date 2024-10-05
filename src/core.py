from datetime import datetime, timedelta
from colorama import Fore, Style
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
        return False  # Example: plum tree doesn't expire

    created = datetime.fromisoformat(created_at[:-1])  # Remove the 'Z' for parsing

    # Calculate expiration period
    expiration_period = timedelta(days=TREE_EXPIRATION_DAYS[tree_type])

    # Return whether the tree is expired based on the created date
    return (datetime.utcnow() - created) > expiration_period

def calculate_remaining_time(last_claimed_at, farming_session_duration):
    last_claimed = datetime.fromisoformat(last_claimed_at[:-1])
    now = datetime.utcnow()
    time_since_last_claim = now - last_claimed
    remaining_time = farming_session_duration - time_since_last_claim
    return remaining_time if remaining_time > timedelta(0) else timedelta(0)

def calculate_fruits_fall(tree_type, last_claimed_at, created_at, speed=1):
    if tree_type not in FRUIT_RATES:
        return 0

    # Check if the tree has expired
    if is_tree_expired(tree_type, created_at):
        return 0

    last_claimed = datetime.fromisoformat(last_claimed_at[:-1])
    now = datetime.utcnow()
    time_elapsed = now - last_claimed
    
    # Multiply by the boosted speed rate if applicable
    fruits_fall = FRUIT_RATES[tree_type] * speed * time_elapsed.total_seconds()
    return int(fruits_fall)

def display_user_info(username, total_gems, total_trees, remaining_time):
    print(Fore.GREEN + "----------------------------------------")
    print(Fore.GREEN + f"Username     : {username}")
    print(Fore.GREEN + f"Total Gems   : {total_gems:.2f}")
    print(Fore.GREEN + f"Number of Trees: {total_trees}")
    print(Fore.GREEN + f"Farming Session Remaining: {str(remaining_time).split('.')[0]}")  # Remove milliseconds
    print(Fore.GREEN + "----------------------------------------")

# Modify display_tree_info to determine if the tree is boosted based on speed
def display_tree_info(tree_type, fruit_total, ready_for_harvest, fruits_fall, expired, speed, created_at, started_boost_at): 
    tree_type_str = tree_type

    # Determine if boosted based on speed
    boosted = speed > 1.00
    if boosted:
        tree_type_str += f" {Fore.GREEN}(Boosted){Style.RESET_ALL}"

    # Print tree details first
    print(f"Tree Type: {tree_type_str}")
    print(f"Total Fruit: {fruit_total}")
    print(f"Fruits to Fall: {fruits_fall}")
    print(f"Speed: {speed:.2f}")

    # If the tree is boosted, calculate expiration time
    if boosted:
        expiration_days = TREE_EXPIRATION_DAYS.get(tree_type, 30)  # Assuming 30 days for boosted trees
        boost_start = datetime.fromisoformat(started_boost_at[:-1])
        boost_expiration = boost_start + timedelta(days=expiration_days)

        remaining_time = boost_expiration - datetime.utcnow()

        if remaining_time > timedelta(0):
            days_left = remaining_time.days
            hours_left, remainder = divmod(remaining_time.seconds, 3600)
            minutes_left, _ = divmod(remainder, 60)

            print(f"Tree will expire in: {days_left} days, {hours_left} hours, {minutes_left} minutes")
        else:
            print(f"{Fore.RED}Tree {tree_type} is Expired{Style.RESET_ALL}")
    else:
        # For non-boosted trees, check standard expiration
        expiration_days = TREE_EXPIRATION_DAYS.get(tree_type)
        if expiration_days is not None:
            creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            days_until_expiry = (creation_date + timedelta(days=expiration_days) - datetime.utcnow()).days
            
            if days_until_expiry <= 0:
                print(f"{Fore.RED}Tree {tree_type} is Expired{Style.RESET_ALL}")
            else:
                print(f"Tree will expire in: {days_until_expiry} days")
        else:
            print(f"Tree {tree_type} {Fore.YELLOW}(Doesn't Expire){Style.RESET_ALL}")

    # Display harvest status
    print(f"Tree {tree_type} is {'ready for harvest' if ready_for_harvest else 'not ready for harvest'}.")
    print("-" * 60)

def countdown_timer(seconds):
    while seconds > 0:
        time_left = str(timedelta(seconds=seconds)).split(".")[0]  # Display only HH:MM:SS
        print(Fore.YELLOW + f"\rWaiting for the next session: {time_left}", end="")
        time.sleep(1)
        seconds -= 1
    print()  # Newline after the countdown ends 