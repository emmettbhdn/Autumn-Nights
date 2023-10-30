import os
from core.helperFunctions import dataHelpers

def loadAllCogs(client):
    for filename in os.listdir(dataHelpers.COG_PATH):
        if filename.endswith(".py") and filename != "__init__.py":
            # Loads the extension by the file name and cuts off the .py at the end
            client.load_extension(f"cogs.{filename[:-3]}")
            print("Cog Loaded: " + filename[:-3])
        else:
            print("Ignored non-python file: " + filename)    

def unloadAllCogs(client):
    for filename in os.listdir(dataHelpers.COG_PATH):
        if filename.endswith(".py") and filename != "__init__.py":
            # Unloads the extension by the file name and cuts off the .py at the end
            client.unload_extension(f"cogs.{filename[:-3]}")
            print("Cog Unloaded: " + filename[:-3])
        else:
            print("Ignroed non-python file: " + filename)
            
def getCogList():
    cogList = []
    for filename in os.listdir(dataHelpers.COG_PATH):
        if filename.endswith(".py") and filename != "__init__.py":
            cogList.append(filename[:-3])