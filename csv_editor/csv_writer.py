import csv


def write_csv_files(teams):
    with open('../players_totals.csv', 'w', newline='') as playersfile, open('../teams.csv', 'w',
                                                                             newline='') as teamfile, open(
        "../players_avgs.csv", "w", newline='') as avgsfile:
        fieldnames = ['Player Name', 'class', 'Team', 'RGL', 'Steam', 'Total Kills', 'Total Assists', 'Total Damage',
                      'Total Deaths',
                      'Total Damage Taken', 'Total Healing', 'Total Charges', 'Total Drops', 'Total Headshot Hits']
        players_writer = csv.DictWriter(playersfile, fieldnames=fieldnames)

        fieldnames = ['Team Name', 'Team Round Wins', 'Team Kills', 'Team Total Damage']
        team_writer = csv.DictWriter(teamfile, fieldnames=fieldnames)

        fieldnames = ['Player Name', 'class', 'Team', 'RGL', 'Steam', 'Avg Kills', 'Avg Assists', 'Avg Damage',
                      'Avg Deaths',
                      'Avg Damage Taken', 'Avg Healing', 'Avg Charges', 'Avg Drops', 'Avg Headshot Hits']
        avgs_writer = csv.DictWriter(avgsfile, fieldnames=fieldnames)

        team_writer.writeheader()
        players_writer.writeheader()
        avgs_writer.writeheader()

        for team in teams:
            team_writer.writerow(
                {"Team Name": team.name, "Team Round Wins": team.team_wins, "Team Kills": team.team_total_kills,
                 "Team Total Damage": team.team_total_damage})

            for player in team.players:
                players_writer.writerow(
                    {"Player Name": player.name, "class": player.type, "Team": player.team,
                     "RGL": "https://rgl.gg/Public/" + player.rgl_link,
                     "Steam": player.steam_link,
                     "Total Kills": player.total_kills, "Total Assists": player.total_assists,
                     "Total Damage": player.total_damage, "Total Deaths": player.total_deaths,
                     "Total Damage Taken": player.total_damage_taken, "Total Healing": player.total_healing,
                     "Total Charges": player.total_charges, "Total Drops": player.total_drops,
                     "Total Headshot Hits": player.headshots_hit})

                if player.time_played_minutes == 0:
                    player.time_played_minutes = 1
                avgs_writer.writerow(
                    {"Player Name": player.name, "class": player.type, "Team": player.team,
                     "RGL": "https://rgl.gg/Public/" + player.rgl_link,
                     "Steam": player.steam_link,
                     "Avg Kills": player.total_kills / player.time_played_minutes,
                     "Avg Assists": player.total_assists / player.time_played_minutes,
                     "Avg Damage": player.total_damage / player.time_played_minutes,
                     "Avg Deaths": player.total_deaths / player.time_played_minutes,
                     "Avg Damage Taken": player.total_damage_taken / player.time_played_minutes,
                     "Avg Healing": player.total_healing / player.time_played_minutes,
                     "Avg Charges": player.total_charges / player.time_played_minutes,
                     "Avg Drops": player.total_drops / player.time_played_minutes,
                     "Avg Headshot Hits": player.headshots_hit / player.time_played_minutes})
