def log(data):
    try:
        logdata = data.find("vs")
        while data[logdata] != "\t":
            logdata -= 1
        team1s = logdata + 2

        logdata += 2
        while data[logdata] != "'":
            logdata += 1
        team1e = logdata

        logdata += 1
        while data[logdata] != "'":
            logdata += 1
        team2s = logdata + 1

        logdata += 1
        while data[logdata] != "'":
            logdata += 1
        team2e = logdata

        team1n = data[team1s:team1e]
        team2n = data[team2s:team2e]

        while data[logdata] != " ":
            logdata += 1

        logdata += 1
        team1s = logdata

        while data[logdata] != " ":
            logdata += 1

        team1e = logdata
        logdata += 1

        while data[logdata] != " ":
            logdata += 1

        logdata += 1
        team2s = logdata

        while data[logdata] != "\n":
            logdata += 1

        team2e = logdata

        team1p = data[team1s:team1e]
        team2p = data[team2s:team2e]
        return team1n, team2n, team1p, team2p
    except IndexError:
        return "", "", "0", "0"
