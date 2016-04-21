import requests
import json
from bs4 import BeautifulSoup as bs

hltv = "http://www.hltv.org"

def getLinks():
	other = {}
	links = []
	matches = bs(requests.get(hltv+"/matches/").text)
	for mac in matches.find_all('div', class_="matchListBox"):
		status = mac.find('div', class_="matchTimeCell").text
		if status == 'Finished':
			team1 = mac.find('div', class_='matchTeam1Cell')
			team2 = mac.find('div', class_='matchTeam2Cell')
			score = str(mac.find('div', class_='matchScoreCell').text.strip())
			if len(score) > 10:
				score = score[2].strip()

			other[str(team1.text.strip()+' vs '+team2.text.strip())] = {
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
			if len(score) > 10:
				score = score[2].strip()

			other[str(team1.text.strip()+' vs '+team2.text.strip())] = {
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
	for link in links:
		match = bs(requests.get(hltv+link).text)
		date = match.find('div', {'style':'text-align:center;font-size: 18px;display:flex;flex-direction: row;justify-content: center;align-items: center'}).text.strip()
		teams = match.find_all('a', {'class': 'nolinkstyle'}, text=True)
		logos= match.find_all('img', {'style': 'vertical-align:-20%;border: 1px solid black;border-radius: 5px;'})
		maclar[str(teams[0].text+" vs "+teams[1].text)] = {
			'date': str(date.strip().replace("\n","").strip()), 
			'team1': teams[0].text,
			'team1Logo': logos[0]['src'],
			'team2': teams[1].text,
			'team2Logo': logos[1]['src'],

		}
	return maclar