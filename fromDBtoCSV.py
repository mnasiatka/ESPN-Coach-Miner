import requests, json, csv

r = requests.post('http://ythogh.com/lrt/get_all_coaches.php')
data = json.loads(r.text)
with open('coaches.csv', 'wb') as writeFile:
    Writer = csv.writer(writeFile)
    Writer.writerow(['Coach', 'Win Percent', 'Season', 'Record', 'Team', 'Sport'])
    for item in data:
        obj = data[item]
        coach = obj['coach']
        winpercent = obj['winpercent']
        season = obj['season']
        record = obj['record']
        team = obj['team']
        sport = obj['sport']
        Writer.writerow([coach,winpercent,season,record,team,sport])
