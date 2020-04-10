import sys
from collections import defaultdict
from decimal import Decimal as D

print('Welcome to the Raker')
file_name = sys.argv[1]
print('Opening file ' + file_name)

winnings = defaultdict(int)
total_rake = 0

with open(file_name, 'r') as f:

    current_takers = set()
    current_rake = 0

    for line in f:
        if "collected" in line:
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
print("Finished!")

