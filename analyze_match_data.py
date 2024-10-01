import os
import json
from collections import defaultdict
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Make the directory to download this dir + tests\match_logs
current_directory = os.getcwd()
match_logs_dir = os.path.join(current_directory, "tests", "match_logs")

# Initialize counters and totals
oshi_usage = defaultdict(int)
oshi_wins = defaultdict(int)
total_games = 0
first_player_wins = 0
total_turns = 0
total_time_used = 0.0
total_clocks = 0

card_usage = defaultdict(int)
card_wins = defaultdict(int)

# Iterate over all match logs
for file_name in os.listdir(match_logs_dir):
    if file_name.endswith(".json"):
        # Load the match log
        with open(os.path.join(match_logs_dir, file_name), "r") as file:
            match_data = json.load(file)

        # Extract relevant data
        player_info = match_data["player_info"]
        winner = match_data["winner"]
        starting_player = match_data["starting_player"]
        player_clocks = match_data["player_clocks"]
        turn_number = match_data["turn_number"]

        # Increment total games count
        total_games += 1

        # Track oshi usage and wins
        for player in player_info:
            oshi_id = player["oshi_id"]
            username = player["username"]

            # Count oshi usage
            oshi_usage[oshi_id] += 1

            # Check if this player won the game
            if username == winner:
                oshi_wins[oshi_id] += 1

            for card_id in player["deck"].keys():
                card_usage[card_id] += 1
                if username == winner:
                    card_wins[card_id] += 1

        # Track if the starting player won
        if starting_player == winner:
            first_player_wins += 1

        # Track total turns
        total_turns += turn_number

        # Track time used (both players' clocks)
        total_time_used += sum(player_clocks)
        total_clocks += 2  # Since player_clocks contains time for both players

# Calculate final statistics
average_turns = total_turns / total_games if total_games else 0
average_time_per_player = total_time_used / total_clocks if total_clocks else 0
first_player_win_percentage = (first_player_wins / total_games * 100) if total_games else 0

# Print results
print("Oshi Usage Totals:")
for oshi, count in oshi_usage.items():
    print(f"{oshi}: {count} times")

print("\nOshi Wins:")
for oshi, wins in oshi_wins.items():
    print(f"{oshi}: {wins} wins")

print("\nOshi Win Percentages:")
for oshi, count in oshi_usage.items():
    win_percentage = (oshi_wins[oshi] / count * 100) if count else 0
    print(f"{oshi}: {win_percentage:.2f}%")

# Calculate total oshi usage across all games
total_oshi_usage = sum(oshi_usage.values())

# Prepare and sort oshi stats by win percentage
oshi_stats = []
for oshi, count in oshi_usage.items():
    win_percentage = (oshi_wins[oshi] / count * 100) if count else 0
    usage_percentage = (count / total_oshi_usage * 100) if total_oshi_usage else 0
    oshi_stats.append((oshi, win_percentage, usage_percentage, count))

# Sort by win percentage in descending order
oshi_stats.sort(key=lambda x: x[1], reverse=True)

# Print formatted table
print("\nOshi Stats (sorted by win percentage):")
print(f"{'Oshi ID':<15} {'Win %':<10} {'Usage %':<10} {'Total Usage':<12}")
for oshi, win_percentage, usage_percentage, count in oshi_stats:
    print(f"{oshi:<15} {win_percentage:<10.2f} {usage_percentage:<10.2f} {count:<12}")

card_stats = []
for card, count in card_usage.items():
    win_percentage = (card_wins[card] / count * 100) if count else 0
    usage_percentage = (count / (total_games * 2) * 100) if (total_games * 2) else 0
    card_stats.append((card, win_percentage, usage_percentage, count))

card_stats.sort(key=lambda x: x[1], reverse=True)
print("\nCard Stats (sorted by win percentage):")
print(f"{'Card ID':<15} {'Win %':<10} {'Usage %':<10} {'Total Usage':<12}")
for card, win_percentage, usage_percentage, count in card_stats:
    print(f"{card:<15} {win_percentage:<10.2f} {usage_percentage:<10.2f} {count:<12}")


print(f"\nTotal games analyzed: {total_games}")
print(f"Average time used per player: {average_time_per_player:.2f} seconds")
print(f"First player win percentage: {first_player_win_percentage:.2f}%")
print(f"Average number of turns: {average_turns:.2f}")