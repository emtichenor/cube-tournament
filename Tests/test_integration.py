from unittest.mock import patch
from src import main
from Tests import Config
from src.Roster import Roster
import os

@patch('time.sleep')
def test_integration(patch_time):
    print(os.getcwd())
    os.chdir('../Files/')
    main.practiceTournament(Config.get_options(True))

    roster = Roster()
    roster.load()
    for p in roster.roster:
        assert p.best_placing <= p.avg_placing
