from rake_calculator import RakeCalculator
import sys

print(sys.argv[1:])
rake_calculator = RakeCalculator(sys.argv[1:])
rake_calculator.process_files()