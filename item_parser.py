import os 
import time
import requests
import csv
import json

start = 0 # 0 is the first item to be displayed
start_check = 0 
count = 99 # Number of items that is listed per page
x = 0 # iterator to keep track of how many items are found
master_list = [] # master list for csv/json output file
quantity = 0 # keeps track of the number of items 
appid = 440 # game to web crawl
last_round = False # Logic checks to see if the crawler is on the final page
page_num = 1 # iterator for JSON file names
json_files_list = [] # keeps track of the JSON files saved and prints at end
temp_list = [] # per web request this list gets appended to the CSV/JSON file
games_and_ids = [] # Will be appended with the games/ids created in other script 
commodity_count = 0 
which_game = 0 # which game to parse, based on the games_and_ids list
json_dict = []

def get_targets():
    dir_contents = os.listdir()
    if 'games.csv' in dir_contents:
        with open('games.csv') as file:
            source = file.read()
            source = source.split('\n')
            for i in source:
                games_and_ids.append(i.split(','))
    elif 'games.csv' not in dir_contents:
        print('games.csv not found in current directory')

def shell_tool(): # little shell UI that doesn't have much use right now
    while True:
        print("""
[1] View Games and Ids
[x] Exit
""")
        choice = str(input('[INPUT]: '))
        if choice == '1':
            print('placeholder')
            # for i in games_and_ids:
            #     print(i)
        if choice == 'x':
            break

def arborist(): # it's called arborist because it's making a directory 'tree'
    global num_append, dir_check, appid, json_dict, which_game
    os.chdir(f'/home/guest/steamy/')
    dir_check = os.listdir()
    while games_and_ids[which_game][0] in dir_check:
        which_game += 1
    os.mkdir(f'/home/guest/steamy/{games_and_ids[which_game][0]}') 
    os.chdir(f'/home/guest/steamy/{games_and_ids[which_game][0]}')
    appid = games_and_ids[which_game][1]
    with open(f'{appid}.json', 'w') as f:
        json.dump(json_dict, f)

with open(f'{appid}.json', 'w') as f:
    json.dump(json_dict, f)

def harvester():
    global last_round, json_files_list, page_num, check, count, total_count, start, start_check, quantity, commodity_count, master_list, temp_list, x, which_game, appid, json_dict
    while last_round is False:
        with open(f'{appid}.json', 'r') as f:
            json_item_data = json.load(f)
        url = f'https://steamcommunity.com/market/search/render/?query=&start={start}&count={count}&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid={appid}&norender=1'
        r = requests.get(url)
        with open(f'page_{str(page_num)}.json', 'w') as file:
            file.write(r.text)
        json_files_list.append(f'page_{page_num}.json') # this list is generated for a summarized printout
        page_num += 1 # this is to add an iterated number to each file name
        check = json.loads(r.text)
        total_count = check["total_count"]
        start_check = check["start"]    
        if quantity == 0:
            quantity = total_count
        elif int(total_count) > int(quantity):
            quantity = total_count
        print(f'{quantity} - {start_check} = {int(quantity)-int(start_check)}' )
        time.sleep(3)
        if int(quantity)-int(start_check) <= 99:
            print('on the last round')
            last_round = True
        for i in range(len(check['results'])):
            # Each of these is parsing the JSON file
            name = check['results'][i]['name'] 
            hash_name = check['results'][i]['hash_name']
            amount = check['results'][i]['sell_listings'] # number of listings for the particular item
            price = check['results'][i]['sell_price_text']
            market_name = check['results'][i]['asset_description']['market_name']
            market_hash_name = check['results'][i]['asset_description']['market_hash_name'] # this is the name which is a variable in the multisell URL
            app_name = check['results'][i]['app_name']
            commodity = check['results'][i]['asset_description']['commodity'] # items must have value of 1 to work with multisell link
            if commodity == 1: # Only commodity items can be multi-sold
                commodity_count += 1 # iterate up the commodity count
                # json_dict['itemlist']['items'].append({'name': name, 'hash_name': hash_name})
                json_item_data.append({'name': name, 'hash_name': hash_name})
            master_list.append([name,hash_name,market_name,market_hash_name,amount,price,app_name,commodity,commodity_count])
            temp_list.append([name,hash_name,market_name,market_hash_name,amount,price,app_name,commodity,commodity_count])
            x+=1 # iterate up the item count
            print(f"""          
    [{x}] of {quantity} 
            app: {app_name}
            name: {name}
        market_name: {market_name}
        hash_name: {hash_name} 
    market_hash_name: {market_hash_name} 
        Quantity: {amount} 
    Commodity: {commodity}
    Commodities: {commodity_count}/{x} 
            Price: {price}
    """)      
            time.sleep(.20)
        start += 99 # add 99 to the start and count so the next requests moves forward
        count += 99
        os.system(f"echo '{app_name}, item #: {x}, commodity count: {commodity_count}' >> status.txt")


        with open(f'{appid}.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            for i in range(len(temp_list)):
                spamwriter.writerow([temp_list[i][0], 
                temp_list[i][1], 
                temp_list[i][2], 
                temp_list[i][3],
                temp_list[i][4],
                temp_list[i][5],
                temp_list[i][6],
                temp_list[i][7]])

        with open(f'{appid}.json', 'w') as f:
            json.dump(json_item_data, f)
        temp_list = [] # clear the temp_list since the round is done.

        if last_round is True: # on the last wround printe a little wrap-up
            print(f'Total items found: {x}')
            print(f'Saved {appid}.csv')  # Print out the MASTER items csv
            for i in json_files_list:
                print('Saved ' + i) # Print out all the saved JSON files gathered by requests
            x = 0 
            count = 0 
            start = 0 
            quantity = 0
            page_num = 0 
            which_game += 1
            os.chdir('/home/guest/steamy')
            json_files_list = [] 
            master_list = []
            temp_list = [] 
            commodity_count = 0
            json.dict = []

get_targets()

for i in range(len(games_and_ids)):
    arborist() # run this function right away
    harvester()
    last_round = False

'''
JSON['results'] example of what I'm parsing from:

{"name":"Elegant Tesla Coil Lantern"', 
'"hash_name":"LANTERN_TESLA"', 
'"sell_listings":21', 
'"sell_price":6215', 
'"sell_price_text":"$62.15"', 
'"app_icon":"https:\\/\\/cdn.akamai.steamstatic.com\\/steamcommunity\\/public\\/images\\/apps\\/322330\\/a80aa6cff8eebc1cbc18c367d9ab063e1553b0ee.jpg"', 
'"app_name":"Don\'t Starve Together"',
 '"asset_description":{"appid":322330', 
 '"classid":"3062072085"', 
 '"instanceid":"0"', 
 '"currency":0', 
'"background_color":""', 
'"icon_url":"C5ICScRs-sa8qjOIVneH3_IDEQVCaW_20WWBAJVET_LaTPFmptfcUOC_bWRo_WNVUQGUl612BbG7ZJ38YPdP_I14GUE4ZZEKGbBJLA"', 
'"icon_url_large":"C5ICScRs-sa8qjOIVneH3_IDEQVCaW_20WWBAJVGRfDaTPFmptfcUOC_bWRo_WNVUQGUl612BbG7ZJ38YPdP_I14GUE4ZZFb803wpA"', 
'"descriptions":[{"type":"html"', 
'"value":"Rarity: <font color = \\"BD4646\\">Elegant<\\/font>"', 
'"color":"FFFFFF"', '"label":""}', 
'{"type":"text"', '"value":" "', '"color":"FFFFFF"', 
'"label":""}', '{"type":"text"', 
'"value":"An electrical resonant transformer circuit that provides light."',
 '"color":"FFFFFF"', '"label":""}]', '"tradable":1', 
'"name":"Elegant Tesla Coil Lantern"', '"name_color":"BD4646"', 
'"type":""', '"market_name":"Elegant Tesla Coil Lantern"', 
'"market_hash_name":"LANTERN_TESLA"', '"market_fee":"0.100000000000000006"', 
'"commodity":1', '"market_tradable_restriction":3', 
'"market_marketable_restriction":3', '"marketable":1}', 
'"sale_price_text":"$59.45"}', '
'''

'''
What I want it to look like:
{
    "itemlist": {
        "items": [
            {
                name: 'Rocket Launcher'
                hash_name: 'Rocket Launcher'
            },
            {
                name: 'Custom Grenade'
                hash_name: 'Grenade'
            }
        ]        
    }
}
'''
