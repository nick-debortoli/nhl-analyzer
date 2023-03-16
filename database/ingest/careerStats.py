# -*- coding: utf-8 -*-
import csv
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import unicodedata
import datetime

# set up selenium
caps = DesiredCapabilities.CHROME
caps["pageLoadStrategy"] = "eager"
driver = webdriver.Chrome(desired_capabilities=caps);


# --------------------- Variable declaration
# # letters = list(string.ascii_lowercase);
letters = ['a']

skater_fields = ['id', 'gamesPlayed','goals','assists','points','plusMinus', 'penaltyMinutes',
          'evenStrengthGoals','powerPlayGoals','shortHandedGoals', 'gameWinningGoals','evenStrengthAssists',
          'powerPlayAssists','shortHandedAssists','shots','shootingPct','totalShotAttempts','timeOnIce','averageTimeOnIce',
          'faceoffWins', 'faceOffLosses', 'faceoffPct', 'blockedShots', 'hits', 'takeaways', 'giveaways', 'infoID', 'isCurrent', 'teamID']

skater_career_fields = ['id', 'gamesPlayed','goals','assists','points','plusMinus', 'penaltyMinutes',
          'evenStrengthGoals','powerPlayGoals','shortHandedGoals', 'gameWinningGoals','evenStrengthAssists',
          'powerPlayAssists','shortHandedAssists','shots','shootingPct','totalShotAttempts','timeOnIce','averageTimeOnIce',
          'faceoffWins', 'faceOffLosses', 'faceoffPct', 'blockedShots', 'hits', 'takeaways', 'giveaways', 'infoID']

goalie_fields = ['id', 'gamesPlayed', 'gamesStarted', 'wins', 'losses', 'tiesPlusOTLosses', 'goalsAllowed', 'shotsAgainst', 'saves', 'savePct', 'goalsAllowedAverage',
                'shutouts', 'minutes', 'qualityStarts', 'qualityStartPct', 'reallyBadStarts', 'relativeGoalsAllowedPct', 'goalsSavedAboveAverage', 'adjustedGoalsAllowedAverage',
                'goaliePointShares', 'goals', 'assists', 'points', 'penaltyMinutes', 'infoID', 'isCurrent' , 'teamID']

goalie_career_fields = ['id', 'gamesPlayed', 'gamesStarted', 'wins', 'losses', 'tiesPlusOTLosses', 'goalsAllowed', 'shotsAgainst', 'saves', 'savePct', 'goalsAllowedAverage',
                'shutouts', 'minutes', 'qualityStarts', 'qualityStartPct', 'reallyBadStarts', 'relativeGoalsAllowedPct', 'goalsSavedAboveAverage', 'adjustedGoalsAllowedAverage',
                'goaliePointShares', 'goals', 'assists', 'points', 'penaltyMinutes', 'infoID']

info_fields = ['id', 'firstName', 'lastName', 'position', 'height', 'weight', 'draftPosition', 'shoots', 'age', 'isActive', 'isHallOfFame', 'jerseyNumber']

today = datetime.date.today()

# --------------------------- Functions
def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').strip()

def get_default_skater(type=None):

    skater_season = {
        'id': '', 'games_played': '', 'goals': '', 'assists': '', 'points': '', 'plus_minus': '', 
        'pen_min': '', 'goals_ev': '', 'goals_pp': '', 'goals_sh': '',
        'goals_gw': '', 'assists_ev': '', 'assists_pp': '', 'assists_sh': '',
        'shots': '', 'shot_pct': '', 'shots_attempted': '', 'time_on_ice': '', 'time_on_ice_avg': '',
        'faceoff_wins': '', 'faceoff_losses': '',  'faceoff_percentage': '', 'blocks': '',  'hits': '',
        'takeaways': '', 'giveaways': '', 'info_id': ''
    }

    if (type != 'career'):
        skater_season['is_current'] = ''
        skater_season['team_id'] = ''

    return skater_season

def get_default_goalie(type=None):

    goalie_season = {
        'id', 'games_goalie', 'starts_goalie', 'win_goalie', 'losses_goalie', 'ties_goalie', 'goals_against', 
        'shots_against', 'saves', 'save_pct', 'goals_against_average', 'shutouts', 'min_goalie', 'quality_starts_goalie',
        'quality_starts_goalie_pct', 'really_bad_starts_goalie', 'ga_pct_mius', 'gs_above_average', 'goals_against_avg_adjusted',
        'gps', 'goals', 'assists', 'points', 'pen_min', 'info_id', 'is_current', 'team_id'
    }

    if (type != 'career'):
        goalie_season['is_current'] = ''
        goalie_season['team_id'] = ''

    return goalie_season

def check_exists_by_selector(selector, soup):
    selection = soup.select(selector);
    if (len(selection) == 0): 
            return False
    else:
        return True

def career_average(stat, num_seasons):
        return int(round(float(stat) / num_seasons))
    
def get_player_info(soup):
    
    print('Getting player info...')
    info_object = {}

    has_thumbnail = check_exists_by_selector('#meta > div.media-item > img', soup);
    initial_selection = '#meta > div'

    if (has_thumbnail):
        initial_selection += ':nth-child(2)'

    full_name =  soup.select_one(initial_selection +  ' > h1 > span').text
    first_name = ' '.join(full_name.split()[:-1])
    last_name = full_name.split()[-1]

    position_shoots_text = soup.select_one(initial_selection +  ' > p:nth-child(2)').text

    if ('Shoots: ' in position_shoots_text):
        position_and_shoots =  position_shoots_text.split('Shoots: ')
    else:
        position_and_shoots =  position_shoots_text.split('Catches: ')
    
    position_text = position_and_shoots[0].replace('Position: ', '')
    position = normalize(position_text)
    shoots = position_and_shoots[1].replace('\n', '')
    
    height =  soup.select_one(initial_selection +  ' > p:nth-child(3) > span:nth-child(1)').text.replace('-', "feet") + 'inches'
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
            age_text = age_split.split('-')[0]
            age = normalize(age_text)
        
        if ('Hall of Fame' in text): 
            is_HOF = True
        
        if ('Current' in text):
            is_active = True
        
        if ('overall' in text):
            overall_split = text.split('overall')[0]
            draft_text = overall_split.split('(')[1].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
            draft_position = normalize(draft_text)
            
    info_object['id'] = normalize((last_name + first_name + yearBorn).replace('-','').replace("'",''))
    info_object['first_name'] = normalize(first_name)
    info_object['last_name'] = normalize(last_name)
    info_object['position'] = position
    info_object['height'] = normalize(height)
    info_object['weight'] = normalize(weight)
    info_object['draft_position'] = draft_position
    info_object['shoots'] = normalize(shoots)
    info_object['age'] = age
    info_object['is_active'] = is_active
    info_object['is_HOF'] = is_HOF
    
    

    return info_object

def get_player_stats(soup, info_id, position):
    print('Getting player stats...')
    player_stats = []

    if (position == 'G'):
        player_career = get_default_goalie('career')
    else:
        player_career = get_default_skater('career')

    if (check_exists_by_selector('#stats_basic_nhl', soup)):
        inital_selector = '#stats_basic_nhl'
    else:
        inital_selector = '#stats_basic_plus_nhl'

    table = soup.select_one(inital_selector + ' > tbody')
    table_rows = table.find_all('tr')

    for row in table_rows:
        cells = row.find_all('td')
        season = normalize(row.find('th').text.split('-')[0])
        season_stats = get_default_skater()
        team_id = ''

        if (season == str(today.year - 1)):
            season_stats['is_current'] = True;
        else:
            season_stats['is_current'] = False;

        for cell in cells:
            cell_text = normalize(cell.text)
            stat_type = normalize(cell['data-stat'])

            if (cell_text == '' or stat_type == 'lg_id' or stat_type == 'age'):
                continue

            if (stat_type == 'team_id'):

                if (cell_text == 'TOT'):
                    season_stats  = get_default_skater()
                    break;

                team_id = cell_text

            else:
                season_stats[stat_type] = cell_text

        if (team_id != ''):
            season_stats['id'] = info_id + '_' + season + team_id
            season_stats['info_id'] = info_id
            season_stats['team_id'] = team_id + season
       
        player_stats.append(season_stats)

    table_foot = soup.select_one(inital_selector + ' > tfoot')
    career_row = table_foot.find_all('tr')[-1]
    career_cells = career_row.find_all('td')
    number_of_seasons = 1

    for cell in career_cells:
        cell_text = normalize(cell.text)
        stat_type = normalize(cell['data-stat'])

        if (cell_text == '' or stat_type == 'lg_id' or stat_type == 'age' or stat_type == 'award_summary'):
                continue
        
        if (stat_type == 'team_id'):
            number_of_seasons = int(cell_text.replace(' yr', '').replace('s', ''))
        elif (stat_type == 'shot_pct' or stat_type == 'time_on_ice_avg' or stat_type == 'faceoff_percentage' 
              or stat_type == 'save_pct' or stat_type == 'goals_against_avg' or stat_type == 'quality_start_goalie_pct' 
              or stat_type == 'ga_pct_minus' or stat_type == 'gs_above_avg' or stat_type == 'goals_against_avg_adjusted'):
            player_career[stat_type] = cell_text
        else:
            player_career[stat_type] = career_average(cell_text, number_of_seasons)

    player_career['info_id'] = info_id
    player_career['id'] = info_id + 'Avg' 

    return player_stats, player_career


# ---------------- Main logic

for letter in letters:
    # Get all players with last name starting with letter 
    url = "https://www.hockey-reference.com/players/" + letter
    print('\n\n\n')
    driver.get(url)
    print('-------STARTING SEARCH FOR', letter, 'PLAYERS')
   
    info_values = []
    skater_values = []
    skater_career_values = []
    goalie_values = []
    goalie_career_values = []
    
    # get all nhl players...
    playerCount = len(driver.find_elements(By.CLASS_NAME, 'nhl'))
    # playerz = [driver.find_element(By.CLASS_NAME, 'nhl')]
 
    # ...and iterate through them
    for player in (range(0, playerCount)): 
    # for player in playerz: 
        time.sleep(1)

        player = driver.find_elements(By.CLASS_NAME, 'nhl')[player]
        playerPage = player.find_element(By.TAG_NAME, 'a').get_attribute('href');
        print(playerPage)
        driver.get(playerPage)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # get player info
        player_info = get_player_info(soup)
        print(player_info)
        
        info_values.append([player_info['id'], player_info['first_name'], player_info['last_name'], player_info['position'], player_info['height'],
                                  player_info['weight'], player_info['draft_position'], player_info['shoots'], player_info['age'], player_info['is_active'],
                                  player_info['is_HOF'], ''])
        
        position = player_info['position']
        player_stats, player_career_stats = get_player_stats(soup, player_info['id'], position)
        print('\n')
        if (position == 'G'):
            for season in player_stats:
            
                print(season)
                goalie_values.append(season['id'], season['games_goalie'], season['starts_goalie'], season['win_goalie'], season['losses_goalie'], season['ties_goalie'], season['goals_against'], 
                                    season['shots_against'], season['saves'], season['save_pct'], season['goals_against_average'],['shutouts'], season['min_goalie'], season['quality_starts_goalie'],
                                    season['quality_starts_goalie_pct'], season['really_bad_starts_goalie'], season['ga_pct_mius'], season['gs_above_average'], season['goals_against_avg_adjusted'],
                                    season['gps'], season['goals'], season['assists'], season['points'], season['pen_min'], season['info_id'], season['is_current'], season['team_id'])
                
            goalie_values.append(player_career_stats['id'], player_career_stats['games_goalie'], player_career_stats['starts_goalie'], player_career_stats['win_goalie'], player_career_stats['losses_goalie'], player_career_stats['ties_goalie'], player_career_stats['goals_against'], 
                                player_career_stats['shots_against'], player_career_stats['saves'], player_career_stats['save_pct'], player_career_stats['goals_against_average'],['shutouts'], player_career_stats['min_goalie'], player_career_stats['quality_starts_goalie'],
                                player_career_stats['quality_starts_goalie_pct'], player_career_stats['really_bad_starts_goalie'], player_career_stats['ga_pct_mius'], player_career_stats['gs_above_average'], player_career_stats['goals_against_avg_adjusted'],
                                player_career_stats['gps'], player_career_stats['goals'], player_career_stats['assists'], player_career_stats['points'], player_career_stats['pen_min'], player_career_stats['info_id'])
                
           
        else:
            for season in player_stats:
                skater_values.append([season['id'], season[ 'games_played'] , season['goals'] , season['assists'] , season['points'] , season['plus_minus'] , 
                                    season[ 'pen_min'] , season['goals_ev'] , season['goals_pp'] , season['goals_sh'],
                                    season['goals_gw'] , season['assists_ev'] , season['assists_pp'] , season['assists_sh'], 
                                    season['shots'] , season['shot_pct'] , season['shots_attempted'] , season['time_on_ice'] , season['time_on_ice_avg'], 
                                    season['faceoff_wins'], season[ 'faceoff_losses'] , season[ 'faceoff_percentage'] , season['blocks'] , season[ 'hits'], 
                                    season[ 'takeaways'] , season['giveaways'] , season['info_id'] , season['is_current'], season['team_id']])
                
            skater_career_values.append([player_career_stats['id'], player_career_stats[ 'games_played'] , player_career_stats['goals'] , player_career_stats['assists'] , player_career_stats['points'],
                                player_career_stats['plus_minus'] , player_career_stats[ 'pen_min'] , player_career_stats['goals_ev'] , player_career_stats['goals_pp'] , player_career_stats['goals_sh'],
                                player_career_stats['goals_gw'] , player_career_stats['assists_ev'] , player_career_stats['assists_pp'] , player_career_stats['assists_sh'], 
                                player_career_stats['shots'] , player_career_stats['shot_pct'] , player_career_stats['shots_attempted'] , player_career_stats['time_on_ice'] , player_career_stats['time_on_ice_avg'], 
                                player_career_stats['faceoff_wins'], player_career_stats[ 'faceoff_losses'] , player_career_stats[ 'faceoff_percentage'] , player_career_stats[ 'blocks'] , player_career_stats[ 'hits'], 
                                player_career_stats[ 'takeaways'], player_career_stats[ 'giveaways'], player_career_stats[ 'info_id']])

        
        driver.execute_script("window.history.go(-1)")

    # with open(letter +'_player_info.csv', 'w') as csvfile: 
    #     # creating a csv writer object 
    #     csvwriter = csv.writer(csvfile) 
            
    #     # writing the fields 
    #     csvwriter.writerow(info_fields) 
            
    #     # writing the data rows 
    #     csvwriter.writerows(info_values)

    with open(letter +'_skater_stats.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(skater_fields) 
            
        # writing the data rows 
        csvwriter.writerows(skater_values)

    with open(letter +'_skater_career_stats.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(skater_career_fields) 
            
        # writing the data rows 
        csvwriter.writerows(skater_career_values)

    with open(letter +'_goalie_stats.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(goalie_fields) 
            
        # writing the data rows 
        csvwriter.writerows(goalie_values)

    with open(letter +'_goalie_career_stats.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(goalie_career_fields) 
            
        # writing the data rows 
        csvwriter.writerows(goalie_career_values)



