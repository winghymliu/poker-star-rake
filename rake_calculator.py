import sys
import re
from collections import defaultdict
from decimal import Decimal as D

print('Welcome to the Raker')
num_files = len(sys.argv) - 1

winnings = defaultdict(int)
total_rake = 0
hand_numbers = set()
duplicates = 0

print(num_files)
for arg_index in range(1, len(sys.argv)):
    file_name = sys.argv[arg_index]
    print('Opening file ' + str(file_name))
    with open(file_name, 'r', encoding='utf-8-sig') as f:

        current_rake = 0

        in_summary = False
        in_hand = False

        hand = defaultdict(int)

        for line in f:
            if line[0:10] == "PokerStars":
                # Reset hand
                print(line)
                
                current_rake = 0
                hand.clear()
                
                hand_number_line = re.search('PokerStars.*(#[0-9]*?):\s.*', line)
                if hand_number_line:
                    found = hand_number_line.group(1);
                    if found in hand_numbers:
                        in_hand = False
                        in_summary = False
                        duplicates += 1
                    else:
                        hand_numbers.add(found)
                        in_hand = False
                        in_summary = True
            elif line[0:15] == "*** SUMMARY ***" and in_hand:
                # Start processing SUMMARY
                print(line)
                in_hand = False
                in_summary = True
            elif in_summary:
                pot_rake_line = re.search('Total pot.*\| Rake ([0-9]*?)\s', line)
                seat_line = re.search('Seat [0-9]: (\S*\s).*(won|collected) \(([0-9]*?)\)', line)
                if seat_line:
                    # Capture player and won/collected amount
                    print(line)
                    player = seat_line.group(1)
                    seat_won_amount = seat_line.group(3)
                    print("Won amount: " + seat_won_amount + " by " + player)
                    hand[player] += int(seat_won_amount)
                elif pot_rake_line:
                    # Capture rake amount for the hand
                    print(line)
                    pot_rake_amount = pot_rake_line.group(1)
                    print("Rake Amount: " + pot_rake_amount)
                    current_rake = int(pot_rake_amount)
                elif len(line.strip()) == 0:
                    # End of SUMMARY, now process the rakes for the hand
                    in_summary = False
                    total_won = sum(hand.values())
                    total_rake += current_rake
                    for name, won_amount in hand.items():
                        print("Rake Amount " + str(current_rake))
                        attributed_rake = won_amount / total_won * current_rake
                        print("Attribute rake " + str(attributed_rake) + " to " + name)
                        winnings[name] += attributed_rake

print("Finished processing, showing rake takers")
for name, amount in winnings.items():
    print('Name: ' + name + " Rake winnings: " + str(amount))

print("Total Rake: " + str(total_rake))
print("Number of hands:" + str(len(hand_numbers)))
print("Duplicates: " + str(duplicates))
print("Finished!")

