import os

escapeValue = -1000
max_odds_index = 3
split_key = "race_id="
home_dir = os.getcwd()
test_years = [ "2023", "2024", "2025", "2026" ]
valid_years = [ test_years[0] ]
score_years = [ test_years[1] ]
recovery_test_years = [ test_years[0], test_years[1] ]
simu_years = [ test_years[2], test_years[3] ]
predict_pace_key_list = [ "pace", "pace_regression", "before_pace_regression", "after_pace_regression", "pace_conv", "first_up3", "last_up3" ]
prod_check = False

