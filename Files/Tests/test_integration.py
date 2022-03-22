from unittest.mock import patch
import pytest
from Files import main
from Files.Tests.Config import Config
from Files.Roster import Roster
import os

@patch('time.sleep')
def test_integration(patch_time):
    print(os.getcwd())
    os.chdir('../')
    main.practiceTournament(Config.get_options(True))

    roster = Roster()
    roster.load()
    for p in roster.roster:
        assert p.best_placing <= p.avg_placing
