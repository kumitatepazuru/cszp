def log(data):
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


def kekka(logs, lang):
    csvf = open("./csvdata/data.csv")
    csv = csvf.read()
    csv = csv.split("\n")
    k = log(logs)
    i = len(csv) - 1
    if k[2] == k[3]:
        if lang == 0:
            return "同点！今後が楽しみです！"
        else:
            return "Draw!We look forward to the future!"
    if max(int(k[2]), int(k[3])) == int(k[2]):
        ka = 0
    else:
        ka = 1

    re = 0
    rp = 0
    hit = 0
    while i >= 0:
        # print(i)
        temp = csv[i].split(",")
        # print(temp)
        if len(temp) == 1:
            pass
        elif temp[0] == k[ka]:
            hit += 1
            if int(temp[2]) == int(temp[3]):
                break
            elif max(int(temp[2]), int(temp[3])) == int(temp[2]):
                re += 1
            else:
                re = 0
                rp += 1
                break

        elif temp[1] == k[ka]:
            hit += 1
            if int(temp[2]) == int(temp[3]):
                break
            elif max(int(temp[2]), int(temp[3])) == int(temp[3]):
                re += 1
            else:
                re = 0
                rp += 1
                break
        i -= 1
    if lang == 0:
        if re == 0:
            if hit != 0:
                return k[ka] + "さんの勝ち！そして、連敗復帰！今後が楽しみです！"
            else:
                return k[ka] + "さんの勝ち！今後が楽しみです！"
        else:
            return k[ka] + "さんの勝ち！そして" + str(re + 1) + "連勝中！"
    else:
        if re == 0:
            if hit != 0:
                return k[ka] + " Won! And return to consecutive losses! We look forward to the future!"
            else:
                return k[ka] + " Won! We look forward to the future!"
        else:
            return k[ka] + " won! And " + str(re + 1) + " consecutive wins!"
