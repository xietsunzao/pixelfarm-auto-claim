import sys
import os
import json
from datetime import timedelta
from colorama import Fore, init
import time

# Initialize colorama for colored console output
init(autoreset=True)

# Import modules from 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api import get_token, fetch_user_data, claim_rewards
from core import calculate_remaining_time, calculate_fruits_fall, countdown_timer, display_user_info, display_tree_info, get_farming_session_duration, is_tree_expired

class Session:
    def __init__(self):
        self.token = None

def main():
    session = Session()

    try:
        while True:
            print(Fore.GREEN + "Checking for harvest time...")
            
            # Load initData from config.json
            with open('src/config.json') as config_file:
                config = json.load(config_file)
                init_data = config.get('initData')
            
            # Get the token using the encoded initData if not already stored
            if not session.token:
                session.token = get_token(init_data)

            if session.token:
                # Fetch user data using the token
                try:
                    user_data = fetch_user_data(session.token)
                except Exception as e:
                    print(Fore.RED + f"Error fetching user data: {str(e)}. Retrying token...")
                    session.token = get_token(init_data)
                    continue

                if 'data' in user_data:
                    user_info = user_data['data']
                    
                    # Display specific user information
                    username = user_info.get('telegram_username', 'N/A')
                    total_gems = user_info.get('gem_amount', 0)
                    trees = user_info.get('crops', [])
                    total_trees = len(trees)

                    # Determine farming session duration based on the number of trees
                    farming_session_duration = get_farming_session_duration(total_trees)
                    
                    # Assuming all trees have the same remaining time, take it from the first tree
                    if trees:
                        last_claimed_at = trees[0].get('last_claimed_at')
                        remaining_time = calculate_remaining_time(last_claimed_at, farming_session_duration)
                    else:
                        remaining_time = "N/A"
                    
                    display_user_info(username, total_gems, total_trees, remaining_time)
                    
                    # Track if any tree is ready for harvest
                    any_ready_for_harvest = False
                    
                    # Display total fruit for each tree and check if it's ready for harvest
                    for tree in trees:
                        fruit_total = tree.get('fruit_total', 0)
                        tree_type = tree.get('tree_type', 'Unknown')
                        last_claimed_at = tree.get('last_claimed_at')
                        created_at = tree.get('created_at')
                        boosted_at = tree.get('started_boost_at')  # Boost information
                        speed = tree.get('speed', 1)  # Default to 1 if no boost

                        # Check if the tree has been boosted
                        boosted = boosted_at is not None
                        
                        # Calculate fallen fruits considering boosts
                        fruits_fall = calculate_fruits_fall(tree_type, last_claimed_at, created_at, speed)

                        # Check if the tree is expired (consider boost)
                        expired = is_tree_expired(tree_type, created_at)
                        ready_for_harvest = remaining_time == timedelta(0)
                        
                        # Display tree information, including boost status
                        display_tree_info(tree_type, fruit_total, ready_for_harvest, fruits_fall, expired, speed, created_at, boosted_at)

                        # If a tree is ready for harvest, set the flag
                        if ready_for_harvest and not expired:
                            any_ready_for_harvest = True
                    
                    # Claim rewards using the token only if any tree is ready and has claimable fruits
                    if any_ready_for_harvest:
                        try:
                            message = claim_rewards(session.token)
                            print(Fore.GREEN + f"Claim Response: {message}")
                        except Exception as e:
                            print(Fore.RED + str(e))
                    else:
                        if remaining_time > timedelta(0):
                            total_seconds = int(remaining_time.total_seconds())
                            countdown_timer(total_seconds)  # Start countdown to next session
                        else:
                            print(Fore.RED + "Farming session expired. No fruits to claim. Skipping claim.")

                        # After the countdown or session expiry, sleep for 5 seconds before next check
                        time.sleep(5)  # Short sleep to avoid constant checks
                
                else:
                    print(Fore.RED + "Failed to retrieve user data.")
            else:
                print(Fore.RED + "Failed to retrieve token.")
            
    except KeyboardInterrupt:
        print(Fore.RED + "\nBot terminated by user. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
