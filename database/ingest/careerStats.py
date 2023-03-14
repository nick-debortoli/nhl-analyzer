import requests
import csv
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# set up selenium
driver = webdriver.Chrome();

# # letters = list(string.ascii_lowercase);
letters = ['b']

skater_fields = ['id', 'gamesPlayed','goals','assists','points','plusMinus', 'penaltyMinutes',
          'evenStrengthGoals','powerPlayGoals','shortHandedGoals', 'gameWinningGoals','evenStrengthAssists',
          'powerPlayAssists','shortHandedAssists','shots','shootingPct','totalShotAttempts','timeOnIce','averageTimeOnIce',
          'faceoffWins', 'faceOffLosses', 'faceoffPct', 'blockedShots', 'hits', 'takeaways', 'giveaways', 'infoID']

goalie_fields = ['id', 'gamesPlayed', 'gamesStarted', 'wins', 'losses', 'tiesPlusOTLosses', 'goalsAllowed', 'shotsAgainst', 'saves', 'savePct', 'goalsAllowedAverage',
                'shutouts', 'minutes', 'qualityStarts', 'qualityStartPct', 'reallyBadStarts', 'relativeGoalsAllowedPct', 'goalsSavedAboveAverage', 'adjustedGoalsAllowedAverage',
                'goaliePointShares', 'goals', 'assists', 'points', 'penaltyMinutes']

info_fields = ['id', 'firstName', 'lastName', 'position', 'height', 'weight', 'draftPosition', 'shoots', 'age', 'isActive', 'isHallOfFame', 'jerseyNumber']

def check_exists_by_selector(selector, soup):
    try:
        soup.select(selector)
    except:
        return False
    return True

def get_player_info(soup):
    print('Getting player info...')
    info_object = {}

    hasThumbnail = check_exists_by_selector('#meta > div.media-item > img', soup);
    iniitialSelection = '#meta > div'

    if (hasThumbnail):
        iniitialSelection == ':nth-child(2)'
    print(iniitialSelection)
    full_name =  soup.select_one(iniitialSelection +  ' > h1 > span').text
    first_name = ' '.join(full_name.split()[:-1])
    last_name = full_name.split()[-1]
    positionAndShoots =  soup.select_one(iniitialSelection+  ' > p:nth-child(2)').text
    height =  soup.select_one(iniitialSelection +  ' > p:nth-child(3) > span:nth-child(1)').text
    weight =  soup.select_one(iniitialSelection+  ' > p:nth-child(3) > span:nth-child(2)').text

    info_object['first_name'] = first_name
    info_object['last_name'] = last_name
    info_object['positionAndShoots'] = positionAndShoots
    info_object['height'] = height
    info_object['weight'] = weight

    return info_object

for letter in letters:
    # Get all players with last name starting with letter 
    url = "https://www.hockey-reference.com/players/" + letter
    print('URL:', url)
    driver.get(url)
    print('---STARTING SEARCH FOR', letter, 'PLAYERS')
   

    # get all nhl players...
    players = driver.find_element(By.CLASS_NAME, 'nhl')
    playerz = [players]

    # ...and iterate through them
    for player in playerz: 
        player.find_element(By.TAG_NAME, 'a').click();
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # get player info
        player_info = get_player_info(soup)
        print(player_info)

    # for rowIndex in range(0,len(rows) -1):
    #     row = rows[rowIndex]
    #     stats = []
        
    #     for element in range(0,len(row)-1):
    #         stats.append(row.findAll('td')[element].text)
    #         print(stats)

            
#             # values.append()


#     # with open('skater_stats_'+year+'.csv', 'w') as csvfile: 
#     #     # creating a csv writer object 
#     #     csvwriter = csv.writer(csvfile) 
            
#     #     # writing the fields 
#     #     csvwriter.writerow(fields) 
            
#     #     # writing the data rows 
#     #     csvwriter.writerows(values)


