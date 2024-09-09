import pandas as pd
import requests

skilllist = []
for skill in range(1,746) :
    url = f'https://pokeapi.co/api/v2/move/{skill}/'
    responses = requests.get(url)
    if responses.status_code == 200 :
        data = responses.json()

        skillname = "null"
        for entries in data.get('names') :
            if entries['language']['name'] == 'ko' :
                skillname = entries['name'].replace("\n" , " ")
                break

        typeskill = data['type']['name']
        url2 = f"https://pokeapi.co/api/v2/type/{typeskill}/"
        responses2 = requests.get(url2)
        if responses2.status_code == 200 :
            data2 = responses2.json()

            for kotype in data2.get('names') :
                if kotype['language']['name'] == 'ko' :
                    skilltype = kotype['name']
                    break


        skillinfo = "null"
        for entry in data['flavor_text_entries'] :
            if entry['language']['name'] == 'ko' :
                skillinfo = entry['flavor_text'].replace("\n", " ")
                break

        skilldamage = data['power']


        skilldata = [skillname,skillinfo,skilldamage,skilltype]
        skilllist.append(skilldata)

data = pd.DataFrame(skilllist, columns=('스킬이름','스킬정보','데미지','타입'))
data.index = data.index+1
print(data)
data.to_csv("skilldata.csv", index=True)