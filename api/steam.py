def convert_steamid64_to_steamid(steamid):
    y = int(steamid) - 76561197960265728
    x = y % 2

    return "STEAM_0:{}:{}".format(x, (y - x) // 2)


def steamid_to_usteamid(steam64):
    steamid = convert_steamid64_to_steamid(steam64)
    steamid_split = steamid.split(':')
    usteamid = []
    usteamid.append('[U:1:')

    y = int(steamid_split[1])
    z = int(steamid_split[2])

    steamacct = z * 2 + y

    usteamid.append(str(steamacct) + ']')

    return ''.join(usteamid)


