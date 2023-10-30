import os
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

COG_PATH = uppath(__file__, 3) + "/cogs/"
MAIN_PATH = uppath(__file__, 3)

with open(MAIN_PATH + "/core/data/servers.txt", "r") as f:
    SERVER_IDS = [int(id) for id in f.readlines()]