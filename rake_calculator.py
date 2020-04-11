import sys
import re
from collections import defaultdict
from decimal import Decimal as D

print('Welcome to the Raker')
file_name = sys.argv[1]
print('Opening file ' + file_name)

winnings = defaultdict(int)
total_rake = 0
hands = set()

with open(file_name, 'r', encoding='utf-8-sig') as f:

    current_takers = set()
    current_rake = 0

    in_summary   = True
    in_hand = True

    for line in f:
        if line[0:10] == "PokerStars":
            in_hand = True
            in_summary = False
            hand_number_search = re.search('PokerStars.*(#[0-9]*?):\s.*', line)
            if hand_number_search:
                found = hand_number_search.group(1);
                hands.add(found)
        elif "collected" in line and in_summary:
            print(line)
            before_collected = line.split(' collected ')[0]
            name = before_collected.split(' ')[-1]
            current_takers.add(name)
            print(name)
        elif "Rake" in line:
            print(line)
            current_rake = D(line.split('Rake ')[1])
            print(current_rake)

            if current_rake and current_takers:
                split_winnings = current_rake / len(current_takers)

                for taker in current_takers:
                    winnings[taker] += split_winnings

            # For Audit
            total_rake += current_rake

            current_takers.clear()
            current_rake = 0

print("Finished processing, showing rake takers")
for name, amount in winnings.items():
    print('Name: ' + name + " Rake winnings: " + str(amount))

print("Total Rake: " + str(total_rake))
print("Number of hands:" + str(len(hands)))
print("Finished!")

