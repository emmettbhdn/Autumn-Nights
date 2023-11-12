import os
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

COG_PATH = uppath(__file__, 3) + "/cogs/"
MAIN_PATH = uppath(__file__, 3)

with open(MAIN_PATH + "/core/data/servers.txt", "r") as f:
    SERVER_IDS = [int(id) for id in f.readlines()]
    
with open(MAIN_PATH + "/core/data/weekly_message_channel.txt", "r") as f:
    WEEKLY_MESSAGE_CHANNEL_ID = int(f.readline())
    
with open(MAIN_PATH + "/core/data/member_of_the_week_role.txt", "r") as f:
    MEMBER_OF_THE_WEEK_ROLE_ID = int(f.readline())
    
with open(MAIN_PATH + "/core/data/random_chance_role.txt", "r") as f:
    RANDOM_CHANCE_ROLE_ID = int(f.readline())
    
def getNthKeyInSortedDict(input_dict, n):
    sorted_key_list = list(dict(reversed(sorted(input_dict.items(), key=lambda item: item[1]))))
    return sorted_key_list[n]