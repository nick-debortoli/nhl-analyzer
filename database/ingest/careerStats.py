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

# --------------------- Variable declaration
# # letters = list(string.ascii_lowercase);
letters = ['i']

skater_fields = ['id', 'gamesPlayed','goals','assists','points','plusMinus', 'penaltyMinutes',
          'evenStrengthGoals','powerPlayGoals','shortHandedGoals', 'gameWinningGoals','evenStrengthAssists',
          'powerPlayAssists','shortHandedAssists','shots','shootingPct','totalShotAttempts','timeOnIce','averageTimeOnIce',
          'faceoffWins', 'faceOffLosses', 'faceoffPct', 'blockedShots', 'hits', 'takeaways', 'giveaways', 'infoID']

goalie_fields = ['id', 'gamesPlayed', 'gamesStarted', 'wins', 'losses', 'tiesPlusOTLosses', 'goalsAllowed', 'shotsAgainst', 'saves', 'savePct', 'goalsAllowedAverage',
                'shutouts', 'minutes', 'qualityStarts', 'qualityStartPct', 'reallyBadStarts', 'relativeGoalsAllowedPct', 'goalsSavedAboveAverage', 'adjustedGoalsAllowedAverage',
                'goaliePointShares', 'goals', 'assists', 'points', 'penaltyMinutes']

info_fields = ['id', 'firstName', 'lastName', 'position', 'height', 'weight', 'draftPosition', 'shoots', 'age', 'isActive', 'isHallOfFame', 'jerseyNumber']

# --------------------------- Functions

def check_exists_by_selector(selector, soup):
    selection = soup.select(selector);
    if (len(selection) == 0): 
            return False
    else:
        return True

def get_player_info(soup):
    print('Getting player info...')
    info_object = {}

    time.sleep(5)
    has_thumbnail = check_exists_by_selector('#meta > div.media-item > img', soup);
    initial_selection = '#meta > div'

    if (has_thumbnail):
        initial_selection += ':nth-child(2)'

    full_name =  soup.select_one(initial_selection +  ' > h1 > span').text
    first_name = ' '.join(full_name.split()[:-1])
    last_name = full_name.split()[-1]

    position_and_shoots =  soup.select_one(initial_selection +  ' > p:nth-child(2)').text.split('Shoots: ')[0].split('Catches: ')
    position = position_and_shoots[0].replace('Position: ', '').replace('\xa0•\xa0    ', '');
    shoots = position_and_shoots[1].replace('\n', '')
    
    height =  soup.select_one(initial_selection +  ' > p:nth-child(3) > span:nth-child(1)').text
    weight =  soup.select_one(initial_selection+  ' > p:nth-child(3) > span:nth-child(2)').text

    meta_div = soup.select_one(initial_selection)
    meta_attributes = meta_div.findAll('p')

    age = ''
    is_active = False
    is_HOF = False
    draft_position = 'Undrafted'

    for attribute in meta_attributes:
        text = attribute.text

        if ('Born:' in text):
            year_split = text.split(',')[1]
            yearBorn = year_split.split(' ')[0].strip()

        if ('Age:' in text):
            age_split = text.split('Age:')[1]
            age = age_split.split('-')[0].replace('\xa0','')
        
        if ('Hall of Fame' in text): 
            is_HOF = True
        
        if ('Current' in text):
            is_active = True
        
        if ('overall' in text):
            overall_split = text.split('overall')[0]
            draft_position = overall_split.split('(')[1].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '').replace('\xa0','')
            
    info_object['id'] = (last_name + first_name + yearBorn).replace('-','').replace("'",'')
    info_object['first_name'] = first_name
    info_object['last_name'] = last_name
    info_object['position'] = position
    info_object['height'] = height
    info_object['weight'] = weight
    info_object['draft_position'] = draft_position
    info_object['shoots'] = shoots
    info_object['age'] = age
    info_object['is_active'] = is_active
    info_object['is_HOF'] = is_HOF
    
    

    return info_object

# ---------------- Main logic

for letter in letters:
    # Get all players with last name starting with letter 
    url = "https://www.hockey-reference.com/players/" + letter
    print('\n\n\n')
    print('URL:', url)
    driver.get(url)
    print('-------STARTING SEARCH FOR', letter, 'PLAYERS')
   

    # get all nhl players...
    playerCount = len(driver.find_elements(By.CLASS_NAME, 'nhl'))
    # playerz = [players]

    # ...and iterate through them
    for player in (range(0, playerCount - 1)): 
        time.sleep(3)

        player = driver.find_elements(By.CLASS_NAME, 'nhl')[player]
        playerPage = player.find_element(By.TAG_NAME, 'a').get_attribute('href');
        print(playerPage)
        driver.get(playerPage)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # get player info
        player_info = get_player_info(soup)
        print(player_info)
        print('\n')
        driver.execute_script("window.history.go(-1)")

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



