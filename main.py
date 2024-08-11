# Created By : Xietsunzao

import sys
import os
import json
import time
from datetime import timedelta
from colorama import Fore, init
init(autoreset=True)


# import module src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api import get_token, fetch_user_data, claim_rewards
from core import calculate_remaining_time, calculate_fruits_fall, display_user_info, display_tree_info, get_farming_session_duration, CHECK_INTERVAL

def main():
    try:
        while True:
            print(Fore.GREEN + "Checking for harvest time...")
            
            # Load initData from config.json
            with open('src/config.json') as config_file:
                config = json.load(config_file)
                init_data = config.get('initData')
            
            # Get the token using the encoded initData
            token = get_token(init_data)
            if token:        
                # Fetch user data using the token
                user_data = fetch_user_data(token)
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
                        fruits_fall = calculate_fruits_fall(tree_type, last_claimed_at)
                        ready_for_harvest = remaining_time == timedelta(0)
                        display_tree_info(tree_type, fruit_total, ready_for_harvest, fruits_fall)
                        
                        if ready_for_harvest and fruits_fall > 0:
                            any_ready_for_harvest = True
                    
                    # Claim rewards using the token only if any tree is ready and has claimable fruits
                    if any_ready_for_harvest:
                        try:
                            message = claim_rewards(token)
                            print(Fore.GREEN + f"Claim Response: {message}")
                        except Exception as e:
                            print(Fore.RED + str(e))
                    else:
                        if remaining_time > timedelta(0):
                            print(Fore.YELLOW + "The bot will automatically claim after the farming session expires.")
                        else:
                            print(Fore.RED + "Farming session expired. No fruits to claim. Skipping claim.")
                else:
                    print(Fore.RED + "Failed to retrieve user data.")
            else:
                print(Fore.RED + "Failed to retrieve token.")
            
            # Wait for the next check
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nBot terminated by user. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()