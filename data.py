import sys

import logs
import rgl
import steam
import classes.player, classes.team


def fill_in_team_stats(team, log_data):
    team.team_wins = team.team_wins + log_data['teams']['Read']['score']
    team.team_total_kills = team.team_total_kills + log_data['teams']['Read']['kills']
    team.team_total_damage = team.team_total_damage + log_data['teams']['Read']['dmg']
    return team

def fill_in_player_stats(player, log_data):

    if player.steam32 in log_data['players']:
        player_json = log_data['players'][player.steam32]
        player.total_kills = player.total_kills + player_json['kills']
        player.total_damage = player.total_damage + player_json['dmg']
    return player


IM_Season_16_Teams = rgl.get_teams_table()

teams = []
for team in IM_Season_16_Teams:
    current_team = classes.team.Team(team, 0, 0, 0, [])
    team_players = []
    team_players_links = rgl.get_team_players_links(IM_Season_16_Teams[team])
    team_season_matches = rgl.get_team_season_matches(IM_Season_16_Teams[team])

    for player_link in team_players_links:
        rgl_link = team_players_links[player_link]['player_link']
        steam_link = team_players_links[player_link]['steam_profile']
        steam_64 = steam_link.split("profiles/", 1)[1]
        steam_32 = steam.steamid_to_usteamid(steam_64)

        team_players.append(
            classes.player.Player(player_link, rgl_link, steam_link,steam_32,  0, 0, 0, 0, 0, 0, 0, 0, 0, team))

    match_logs = []
    for match in team_season_matches:
        match_logs = match_logs + rgl.get_match_logs(team_season_matches[match])

    for log_url in match_logs:
        log_data = logs.get_logs_data(log_url)

        for player in team_players:
            fill_in_player_stats(player, log_data)

    current_team.players = team_players
    teams.append(current_team)


for team in teams:
    print("-----------------------------------------------------------")
    print("Team Name: " + team.name)
    print("Team Wins: " + str(team.team_wins))
    print("Team Kills: " + str(team.team_total_kills))
    print("Team Total Damage " + str(team.team_total_damage))
    print("---------------------PLAYERS-------------------------------")

    for player in team.players:
        print("-----------------------" + player.name + "-----------------------------\n")
        print("Player Name: " + player.name)
        print("RGL Link: https://rgl.gg/Public/"+player.rgl_link)
        print("Player Kills: " + str(player.total_kills))
        print("Player Damage: " + str(player.total_damage))
        print("Player Damage Taken: " + str(player.total_damage_taken))
        print("-----------------------" + player.name + "-----------------------------\n")
    print("\n")