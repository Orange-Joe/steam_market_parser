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
appid = 322330 # game to web crawl
last_round = False # Logic checks to see if the crawler is on the final page
page_num = 1 # iterator for JSON file names
json_files_list = [] # keeps track of the JSON files saved and prints at end
temp_list = [] # per web request this list gets appended to the CSV/JSON file
games_and_ids = [] # Will be appended with the games/ids created in other script 


def get_targets():
    dir_contents = os.listdir()
    if 'games.csv' in dir_contents:
        with open('games.csv') as file:
            source = file.read()
            source = source.split('\n')
            print(source)
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


while last_round is False:
    url = f'https://steamcommunity.com/market/search/render/?query=&start={start}&count={count}&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid={appid}&norender=1'
    r = requests.get(url)
    with open(f'page_{str(page_num)}.json', 'w') as file:
            file.write(r.text)
    with open(f'page_{str(page_num)}.json') as file:
        source = file.read()
    json_files_list.append(f'page_{page_num}.json')
    page_num += 1
    check = json.loads(source)
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
        amount = check['results'][i]['sell_listings']
        price = check['results'][i]['sell_price_text']
        market_name = check['results'][i]['asset_description']['market_name']
        market_hash_name = check['results'][i]['asset_description']['market_hash_name']
        app_name = check['results'][i]['app_name']
        master_list.append([name,hash_name,market_name,market_hash_name,amount,price])
        temp_list.append([name,hash_name,market_name,market_hash_name,amount,price])
        x+=1

        print(f"""    # Print out what's being added every .15 seconds            
[{x}] of {quantity} 
         app: {app_name}
        name: {name}
    market_name: {market_name}
    hash_name: {hash_name} 
market_hash_name: {market_hash_name} 
    Quantity: {amount} 
        Price: {price}
""")      
        time.sleep(.15)
    start += 99 # add 99 to the start and count so the next requests moves forward
    count += 99

    with open(f'{appid}.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for i in range(len(temp_list)):
            spamwriter.writerow([temp_list[i][0], temp_list[i][1], temp_list[i][2], temp_list[i][3]])

    temp_list = [] # clear the temp_list since the round is done.

    if last_round is True: # on the last wround printe a little wrap-up
        print(f'Total items found: {x}')
        print(f'Saved {appid}.csv')  # Print out the MASTER items csv
        for i in json_files_list:
            print('Saved ' + i) # Print out the all saved JSON file gathered by requests 
'''
JSON['results'] example:

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


