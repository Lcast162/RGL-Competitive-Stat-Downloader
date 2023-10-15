import requests
from bs4 import BeautifulSoup
import re


def get_player_steam_profile(player_url):
    player_url = player_url.replace("https://", "")
    player_html = requests.get("https://rgl.gg/Public/" + player_url)
    steam_link = ""

    if player_html.status_code == 200:
        soup = BeautifulSoup(player_html.content, "html.parser")
        steam_link = soup.find("a", {"alt": "Steam"})
    return steam_link['href']


def get_teams_table():
    im_season_16_league_link = "https://rgl.gg/Public/LeagueTable?g=879&s=144&r=24"
    league_html = requests.get(im_season_16_league_link)
    team_dict = {}

    if league_html.status_code == 200:
        soup = BeautifulSoup(league_html.content, "html.parser")
        team_list = soup.find("table", {"class": "table table-striped"}).findAll("a",
                                                                                 {"class": "deco-none-excepthover"})

        for team in team_list:
            team_name = team.text.strip().replace('\n', '')

            if "BYE" in team_name or "Free Agent" in team_name:
                break
            team_url = team['href']
            team_dict[team_name] = team_url

    return team_dict


def get_match_logs(match_url):
    team_url = match_url.replace("https://", "")
    match_html = requests.get("https://rgl.gg/Public/" + team_url)
    logs_dict = {}

    if match_html.status_code == 200:
        soup = BeautifulSoup(match_html.content, "html.parser")
        match_logs = soup.find('div', {"style": "padding-left: 20px"}).findAll('a', href=True)

        for match in match_logs:
            match_url = match['href'].split("#", 1)[0]
            if "https://logs.tf" in match_url and match_url not in logs_dict.keys():
                logs_dict[match_url] = 0

        return list(logs_dict.keys())


def get_team_season_matches(team_url):
    team_url = team_url.replace("https://", "")
    team_html = requests.get("https://rgl.gg/Public/" + team_url)
    matches_dict = {}

    if team_html.status_code == 200:
        soup = BeautifulSoup(team_html.content, "html.parser")
        league_matches = soup.find("div", {"class": "col-lg-8 col-sm-12"}).find("table", {
            "class": "table table-striped"}).find_all('a', href=True)

        for match in league_matches:
            match_name = match.text.strip().replace('\n', '')
            match_link = match['href']
            if "Week" in match_name:
                matches_dict[match_name] = match_link
        return matches_dict


def get_team_players_links(team_url):
    team_url = team_url.replace("https://", "")
    team_html = requests.get("https://rgl.gg/Public/" + team_url)

    players_dict = {}
    if team_html.status_code == 200:
        steam_profile = ""
        soup = BeautifulSoup(team_html.content, "html.parser")
        player_list = soup.find("table", {"class": "table table-striped"}).find_all('a', href=True)

        for player in player_list:

            player_name = player.text.strip().replace('\n', '')
            player_link = player['href']
            if player_name == "" or "Join Team" in player_name:
                continue

            steam_profile = get_player_steam_profile(player_link)
            players_dict[player_name] = {"player_link": player_link, "steam_profile": steam_profile}

    return players_dict
