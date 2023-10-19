import classes.player
import classes.team
from csv_editor import csv_writer, data
from api import rgl, steam, logs


def run_tool(div):
    Season_16_Teams = rgl.get_teams_table("MAIN")
    teams = []
    counter = 1
    for team in Season_16_Teams:
        print("Starting to grab info for team: " + team + "\n")
        current_team = classes.team.Team(team, 0, 0, 0, [])
        team_players = []
        team_players_links = rgl.get_team_players_links(Season_16_Teams[team])
        team_season_matches = rgl.get_team_season_matches(Season_16_Teams[team])

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
            print(log_url)
            log_data = logs.get_logs_data(log_url)
            team_color = ""
            last_combined_date = data.get_last_combined_date(log_data, last_combined_date)
            for player in team_players:

                data.fill_in_player_stats(player, log_data, last_combined_date)
                color = data.get_team_color(player, log_data)

                if color is not None:
                    team_color = color

            data.fill_in_team_stats(current_team, log_data, team_color, last_combined_date)
        current_team.players = team_players
        teams.append(current_team)
        print("Finished to grabbing info for team: " + team + "\n")
        print("Current Progress is " + str(counter) + "/" + str(len(Season_16_Teams)))
        counter= counter + 1
        if team =="Ceviche de tiburon":
            break


    csv_writer.write_csv_files(teams)