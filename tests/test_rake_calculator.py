import pytest
from rake_calculator import RakeCalculator


def test_calculator():

    test_file = "resources/HH20200403 3 April 10p BB - 50-100 - Play Money No Limit Hold'em.txt"
    test_files = [test_file]
    rake_calculator = RakeCalculator(test_files)
    rake_results = rake_calculator.process_files()

    assert int(rake_results.total_rake) == 66065
    assert int(rake_results.duplicates) == 0
    assert int(rake_results.total_hands) == 280

    assert int(rake_results.winnings['420justblazeit']) == 3454
    assert int(rake_results.winnings['hellokwanny']) == 6775
    assert int(rake_results.winnings['no1beyondfan888']) == 17683
    assert int(rake_results.winnings['pokeher878787']) == 11268
    assert int(rake_results.winnings['scra88le56']) == 13666
    assert int(rake_results.winnings['winghymliu']) == 13216