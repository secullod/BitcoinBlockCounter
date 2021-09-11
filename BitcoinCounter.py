import requests
from string import Template
import json

blocks = {}
blocks['block_times'] = []
blocks['mining_times'] = {}
blocks['count'] = 0
unix_hour = 3600
unix_minute = 60
start_height = 0
end_height = 10001

temp_str = 'https://blockchain.info/block-height/$blockheight?format=json'
temp_obj = Template(temp_str)

for index, height in enumerate(range(start_height, end_height)):
    url = temp_obj.substitute(blockheight=height)
    result = requests.get(url).json()
    blocks['block_times'].append(result['blocks'][0]['time'])
    print(index + 1)

for height, (block_time, block_time2) in enumerate(zip(blocks['block_times'], blocks['block_times'][1:])):
    mining_time = block_time2 - block_time
    blocks['mining_times'][height + 1] = mining_time
    if mining_time > 2 * unix_hour:
        blocks['count'] += 1
        print(blocks['count'], "mined in", round(
            mining_time / unix_minute, 2), "minutes")

with open('block.json', 'w') as outfile:
    json.dump(blocks, outfile)
