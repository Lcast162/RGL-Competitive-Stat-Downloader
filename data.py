import csv
import sys

import logs
import rgl
import steam
import classes.player, classes.team


def fill_in_team_stats(team, log_data, team_color, last_combined_date):
    if last_combined_date <= int(log_data['info']['date']):
        print(team_color)
        team.team_wins = team.team_wins + log_data['teams'][str(team_color)]['score']
        team.team_total_kills = team.team_total_kills + log_data['teams'][str(team_color)]['kills']
        team.team_total_damage = team.team_total_damage + log_data['teams'][str(team_color)]['dmg']
        return team


def get_team_color(player, log_data):
    if player.steam32 in log_data['players']:
        player_json = log_data['players'][player.steam32]
        return player_json['team']


def get_last_combined_date(log_data, last_combined_date):
    if last_combined_date < int(log_data['info']['date']) and  log_data['info']['uploader']['info'] is not None and "Combiner" in log_data['info']['uploader']['info']:
        last_combined_date = int(log_data['info']['date'])
    return last_combined_date


def fill_in_player_stats(player, log_data, last_combined_date):

    if player.steam32 in log_data['players'] and last_combined_date <= int(log_data['info']['date']):
        player_json = log_data['players'][player.steam32]
        player.total_kills = player.total_kills + player_json['kills']
        player.total_damage = player.total_damage + player_json['dmg']
        player.total_deaths = player.total_deaths + player_json['deaths']
        player.total_assists = player.total_assists + player_json['assists']
        player.total_charges = player.total_charges + player_json['ubers']
        player.total_damage_taken = player.total_damage_taken + player_json['dt']
        player.total_healing = player.total_healing + player_json['heal']
        player.total_drops = player.total_drops + player_json['drops']
        player.headshots_hit = player.headshots_hit + player_json['headshots_hit']
        player.round_played = player.round_played + 1
        player.time_played_minutes = player.time_played_minutes + (int(log_data['length'])/60)
        player.type = player_json['class_stats'][0]['type']
    return player


IM_Season_16_Teams = rgl.get_teams_table()

teams = []
counter = 1
for team in IM_Season_16_Teams:
    print("Starting to grab info for team: " + team + "\n")
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
            classes.player.Player(player_link, rgl_link, steam_link, steam_32, 0, 0, 0, 0, 0, 0, 0, 0, 0, team, 0, ""))

    match_logs = []
    for match in team_season_matches:
        match_logs = match_logs + rgl.get_match_logs(team_season_matches[match])
    last_combined_date = 0
    for log_url in match_logs:
        log_data = logs.get_logs_data(log_url)
        team_color = ""
        last_combined_date = get_last_combined_date(log_data, last_combined_date)
        for player in team_players:

            fill_in_player_stats(player, log_data, last_combined_date)
            color = get_team_color(player, log_data)

            if color is not None:
                team_color = color

        fill_in_team_stats(current_team, log_data, team_color,last_combined_date)
    current_team.players = team_players
    teams.append(current_team)
    print("Finished to grabbing info for team: " + team + "\n")
    print("Current Progress is " + str(counter) + "/" + str(len(IM_Season_16_Teams)))
    counter= counter + 1

  #  if team == "We the P":
     #   break


with open('players_totals.csv', 'w', newline='') as playersfile, open('teams.csv', 'w', newline='') as teamfile, open("players_avgs.csv", "w", newline='') as avgsfile:
    fieldnames = ['Player Name','class', 'Team', 'RGL', 'Steam', 'Total Kills', 'Total Assists', 'Total Damage', 'Total Deaths',
                  'Total Damage Taken', 'Total Healing', 'Total Charges', 'Total Drops', 'Total Headshot Hits']
    players_writer = csv.DictWriter(playersfile, fieldnames=fieldnames)

    fieldnames = ['Team Name', 'Team Round Wins', 'Team Kills', 'Team Total Damage']
    team_writer = csv.DictWriter(teamfile, fieldnames=fieldnames)

    fieldnames = ['Player Name', 'class', 'Team', 'RGL', 'Steam', 'Avg Kills', 'Avg Assists', 'Avg Damage', 'Avg Deaths',
                  'Avg Damage Taken', 'Avg Healing', 'Avg Charges', 'Avg Drops', 'Avg Headshot Hits']
    avgs_writer = csv.DictWriter(avgsfile, fieldnames=fieldnames)

    team_writer.writeheader()
    players_writer.writeheader()
    avgs_writer.writeheader()

    for team in teams:
        team_writer.writerow({"Team Name": team.name, "Team Round Wins": team.team_wins, "Team Kills": team.team_total_kills,
                              "Team Total Damage": team.team_total_damage})

        for player in team.players:
            players_writer.writerow(
                {"Player Name": player.name, "class": player.type, "Team": player.team, "RGL": "https://rgl.gg/Public/" + player.rgl_link,
                 "Steam": player.steam_link,
                 "Total Kills": player.total_kills, "Total Assists": player.total_assists,
                 "Total Damage": player.total_damage, "Total Deaths": player.total_deaths,
                 "Total Damage Taken": player.total_damage_taken, "Total Healing": player.total_healing,
                 "Total Charges": player.total_charges, "Total Drops": player.total_drops,
                 "Total Headshot Hits": player.headshots_hit})

            if player.time_played_minutes == 0:
                player.time_played_minutes = 1
            avgs_writer.writerow(
                {"Player Name": player.name, "class": player.type, "Team": player.team, "RGL": "https://rgl.gg/Public/" + player.rgl_link,
                 "Steam": player.steam_link,
                 "Avg Kills": player.total_kills/player.time_played_minutes , "Avg Assists": player.total_assists/player.time_played_minutes,
                 "Avg Damage": player.total_damage/player.time_played_minutes, "Avg Deaths": player.total_deaths/player.time_played_minutes,
                 "Avg Damage Taken": player.total_damage_taken/player.time_played_minutes, "Avg Healing": player.total_healing/player.time_played_minutes,
                 "Avg Charges": player.total_charges/player.time_played_minutes, "Avg Drops": player.total_drops/player.time_played_minutes,
                 "Avg Headshot Hits": player.headshots_hit/player.time_played_minutes})
