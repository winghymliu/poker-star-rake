import re
from collections import defaultdict


class RakeResults:
    def __init__(self, winnings, total_rake, total_hands, duplicates):
        self.winnings = winnings
        self.total_rake = total_rake
        self.total_hands = total_hands
        self.duplicates = duplicates


class RakeCalculator:

    def __init__(self, poker_files):
        print('Welcome to the Raker')
        print(poker_files)
        num_files = len(poker_files)
        self.poker_files = poker_files

        self.winnings = defaultdict(int)
        self.total_rake = 0
        self.hand_numbers = set()
        self.duplicates = 0

        print('Number of files ' + str(num_files))

    def process_files(self):
        for arg_index in range(len(self.poker_files)):
            file_name = self.poker_files[arg_index]
            print('Opening file ' + str(file_name))
            with open(file_name, 'r', encoding='utf-8-sig') as f:

                self.current_rake = 0

                self.in_summary = False
                self.in_hand = False

                hand = defaultdict(int)

                for line in f:
                    if line[0:10] == "PokerStars":
                        self.reset_hand(line, hand)
                    elif line[0:15] == "*** SUMMARY ***" and self.in_hand:
                        self.process_summary(line)
                    elif self.in_summary:
                        pot_rake_line = re.search('Total pot.*\| Rake ([0-9]*?)\s', line)
                        seat_line = re.search('Seat [0-9]: (\S*\s).*(won|collected) \(([0-9]*?)\)', line)
                        if seat_line:
                            self.update_player_winnings(hand, line, seat_line)
                        elif pot_rake_line:
                            self.update_rake(line, pot_rake_line)
                        elif len(line.strip()) == 0:
                            self.process_rake(hand)

        print("Finished processing, showing rake takers")
        for name, amount in sorted(self.winnings.items()):
            print('Name: ' + name + " Rake winnings: " + str(amount))

        print("Total Rake: " + str(self.total_rake))
        print("Number of hands:" + str(len(self.hand_numbers)))
        print("Duplicates: " + str(self.duplicates))
        print("Finished!")
        return RakeResults(self.winnings, self.total_rake, len(self.hand_numbers), self.duplicates)

    def reset_hand(self, line, hand):

        # Reset hand
        print(line)
        current_rake = 0
        hand.clear()
        hand_number_line = re.search('PokerStars.*(#[0-9]*?):\s.*', line)
        if hand_number_line:
            found = hand_number_line.group(1);
            if found in self.hand_numbers:
                self.in_hand = False
                self.in_summary = False
                self.duplicates += 1
            else:
                self.hand_numbers.add(found)
                self.in_hand = False
                self.in_summary = True

    def process_rake(self, hand):
        # End of SUMMARY, now process the rakes for the hand
        self.in_summary = False
        total_won = sum(hand.values())
        self.total_rake += self.current_rake
        for name, won_amount in hand.items():
            print("Rake Amount " + str(self.current_rake))
            attributed_rake = won_amount / total_won * self.current_rake
            print("Attribute rake " + str(attributed_rake) + " to " + name)
            self.winnings[name] += attributed_rake

    def update_rake(self, line, pot_rake_line):
        # Capture rake amount for the hand
        print(line)
        pot_rake_amount = pot_rake_line.group(1)
        print("Rake Amount: " + pot_rake_amount)
        self.current_rake = int(pot_rake_amount)

    def update_player_winnings(self, hand, line, seat_line):
        # Capture player and won/collected amount
        print(line)
        player = seat_line.group(1).strip()
        seat_won_amount = seat_line.group(3)
        print("Won amount: " + seat_won_amount + " by " + player)
        hand[player] += int(seat_won_amount)

    def process_summary(self, line):
        # Start processing SUMMARY
        print(line)
        self.in_hand = False
        self.in_summary = True

