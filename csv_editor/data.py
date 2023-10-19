
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
