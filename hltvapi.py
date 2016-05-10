import requests
import json
from bs4 import BeautifulSoup as bs
from termcolor import colored

hltv = "http://www.hltv.org"

def getLinks():
	other = {}
	links = []
	matches = bs(requests.get(hltv+"/matches/").text)
	ab = 0
	for mac in matches.find_all('div', class_="matchListBox"):
		ab += 1
		status = mac.find('div', class_="matchTimeCell").text
		if status == 'Finished':
			team1 = mac.find('div', class_='matchTeam1Cell')
			team2 = mac.find('div', class_='matchTeam2Cell')
			score = str(mac.find('div', class_='matchScoreCell').text.strip())
			if len(score) > 10:
				score = score[2].strip()

			other["a"+str(ab)] = {
				'status': 'Finished',
				'team1': str(team1.text.strip()), 
				'team1Logo': str(team1.find('img')['src']),
				'team2': str(team2.text.strip()),
				'team2Logo': str(team2.find('img')['src']),
				'score': score
			}
		elif status == 'LIVE':
			team1 = mac.find('div', class_='matchTeam1Cell')
			team2 = mac.find('div', class_='matchTeam2Cell')
			score = str(mac.find('div', class_='matchScoreCell').text.strip())
			if len(score) > 10:
				score = score[2].strip()

			other["a"+str(ab)] = {
				'status': 'LIVE',
				'team1': str(team1.text.strip()), 
				'team1Logo': str(team1.find('img')['src']),
				'team2': str(team2.text.strip()),
				'team2Logo': str(team2.find('img')['src']),
				'score': score
			}
		else:
			links.append(mac.find_all('a',href=True, text='Details')[0]['href'])
	return links, other

def matches():
	returned = getLinks()
	links = returned[0]
	maclar = returned[1]
	a = 0
	for link in links:
		a += 1
		print colored('Parsing ', 'green')+colored(str(a),'red')+colored('. match.', 'green')
		match= bs(requests.get(hltv+link).text)
		date= match.find('div', {'style':'text-align:center;font-size: 18px;display:flex;flex-direction: row;justify-content: center;align-items: center'}).text.strip()
		logos= match.find_all('img', {'style': 'vertical-align: -3%; border: 1px solid black; border-radius: 5px; height: 20px;'})
	
		team1 = match.find('div', {'id': 'voteteam1'})
		team2 = match.find('div', {'id': 'voteteam1'})
		if team1 and team2 != None:
			team1 = str(team1.text)
			team2 = str(team2.text)

			maclar[str(a)] = {
				'date': str(date.strip().replace("\n","").strip()), 
				'team1': team1,
				'team1Logo': str(logos[0]['src']),
				'team2': team2,
				'team2Logo': str(logos[1]['src']),	
				}
		else:
			print colored('I cant find teams for this match. Skip.', 'blue')

	return maclar
