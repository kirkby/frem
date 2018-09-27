#!/usr/local/bin/python3
from requests_html import HTMLSession
session = HTMLSession()
import sys 
import re
#import pprint
from os import listdir
from os.path import isfile, join
from player import Player

# TODO Real 
# - load main file and extract player urls as list
# - from each url, extract player info into object
# - from each url, save file for offline use
# - 
#  TODO TEST
# - load 


def get_player_urls():
    r = session.get(BK_FREM_MAIN_URL)
    links = r.html.absolute_links
    players = [x for x in links if 'spillerid' in x]
    print(str(len(players)) + ' spillere fundet.' )
    return players

def dev_get_player_urls():
    links = [
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=491', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=686', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=640', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=903', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=913', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=661', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=905', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=422', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=916', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=914', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=882', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=900', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=906',
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=909', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=912', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=886', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=890', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=917', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=918', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=888', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=655', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=901', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=861', 
    'http://www.bkfrem.dk/default.asp?id=19&spillerid=910']
    return links

def dev_load_players_from_disk():
    """Assumes that dir only holds data files.
    Assummes that python web server is running
    Command: python3 -m http.server"""
    url = 'http://0.0.0.0:8000/'
    #files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files = listdir('/users/mkm/Dev/python/data')
    playerUrls = [url + f for f in files]
    return playerUrls

def save_player_page_to_file(url):
    # extract id from url parameter spillerid=xxx
    regex = re.compile('spillerid')
    match = regex.search(url)
    start = match.start()
    path = url[start:].strip()
    path = 'bkfrem-' + path.replace('spillerid=', '') + '.html'
    print(path)

    ## get page
    response = session.get(url)
    enc = response.encoding
    # save page as file
    file = open('/users/mkm/Dev/python/data/' + path, "w+", encoding=enc)
    file.write(response.text)
    file.close()
    return

# given a bkfrem.dk player page html, extract player name and number
def extract_name_number_from_html(html):
    # find name and number in H1
    #print('html: ' + str(html))
    name = html.find('h1', first=True).text
    regex = re.compile('\d+\.')
    match = regex.match(name)
    if match:
        end = match.end()
        nbr = name[0:end-1].strip()
        name = name[end:].strip()
    else:
        nbr = 'N/A'
    return Player(name, nbr)
    #print('!Spiller nr. ' + player.nbr + ' er ' + player.name)    

# given a bkfrem.dk player page html, extract player data
def extract_player_data_from_html(player, html):
    
    props = {}

    for i in range(1,len(player.tableDef)):
        selector = 'table > tr:nth-child(' + str(i) + ') > td:nth-child(2)'
        data = p.html.find(selector, first=True)
        props[player.tableDef[i]] = data.text
        #print(str(i) + '. ' + player.tableDef[i] + ': ' + data.text)
    
    player.props = props
    # special case: games and games this season in one string, ex "70 (10)"
    regex = re.compile('(\d+).+\((\d+)\)')
    match = regex.search(props['Games'])
    if match:
        props['Games'] = match.group(1)
        props['Games-this-season'] = match.group(2)

    # special case: goals and goals this season in one string, ex "25 (10)"
    match = regex.search(props['Goals'])
    if match:
        props['Goals'] = match.group(1)
        props['Goals-this-season'] = match.group(2)

    return

def print_player(player):
    print()
    print('*** ' + player.name + '(' + str(player.id) + ') ***')
    print('Url: ' + player.url)
    print('Nummer: ' + player.nbr)
    print('Mål: ' + player.goals)
    print('Født: ' + player.birthday)
    print('Højde: ' + player.height)
    print('Vægt: ' + player.weight)
    print('')
    #for key, value in player.props.items():
    #        if key not in ['Description', 'Career', 'Debute']:
    #            print (key + ':' + value)



# ---------------------------------------------------
# main()
# ---------------------------------------------------

# load player urls from main page id=19
#playerUrls = get_player_urls()

# development
#for url in playerUrls:
#    save_player_page_to_file(url)
#exit()
playerUrls = dev_load_players_from_disk()

# for each player, extract info from html
for url in playerUrls:
    player = Player(url)
    res = session.get(url)
    player.set_name_nbr(res.html)
    player.set_properties(res.html)
    print_player(player)
    if int(player.nbr) > 10:
        exit()
    
    

