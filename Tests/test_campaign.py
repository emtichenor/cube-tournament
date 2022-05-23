from unittest.mock import patch
from src.Campaign import Campaign
import os

@patch('Files.src.Campaign.input')
@patch('Files.Campaign.Campaign.generateSeason')
def test_startup(patch_season, patch_input):
    campaign = Campaign()
    cmp_name = "test_startup"
    patch_input.return_value = cmp_name
    campaign.startup()
    path = f'../Data/Campaigns/{cmp_name}/'
    dirs = os.listdir(path)
    for dir in ["Unused_Old_Rosters", "Schedules", "Tournaments"]:
        assert dir in dirs
        os.rmdir(path+dir)
    os.rmdir(path)
    assert patch_season.call_count == 1

@patch("Files.src.Campaign.Roster")
def test_generateSeason(patch_roster):
    campaign = Campaign()
    campaign.campaign_name = "test_gen_season"
    path = f'../Data/Campaigns/{campaign.campaign_name}/'
    os.mkdir(path)
    os.mkdir(path+"Schedules")
    campaign.generateSeason()
    assert os.path.isfile(f"{path}Schedules/Season_1.csv")
    os.remove(f"{path}Schedules/Season_1.csv")
    os.rmdir(f"{path}Schedules")
    os.rmdir(path)
