# Helper funcitons for the member of the week functionalities
from core.helperFunctions.dataHelpers import uppath
import pickle # Library to serialize python objects such as dicts
import discord
# from replit import db

MEMBER_MESSAGES_DICT_PATH = uppath(__file__, 2) + "\\data\\weekly_messages.dat"

def saveMemberMessageDict(dict):
    with open(MEMBER_MESSAGES_DICT_PATH, "wb") as f:
        pickle.dump(dict, f)
        print("Updated the member messages dict")

def loadMemberMessageDict():
    with open(MEMBER_MESSAGES_DICT_PATH, "rb") as f:
        dict = pickle.load(f)
        return dict

def addMemberMessages(member_id, num_messages = 1):
    members_dict = loadMemberMessageDict()
    old_message_num = members_dict[member_id]
    members_dict[member_id] = old_message_num + num_messages
    saveMemberMessageDict(members_dict)

def getMemberMessages(member_id):
    dict = loadMemberMessageDict()
    return dict[member_id]

async def resetMemberMessageDict(guild):
    with open(MEMBER_MESSAGES_DICT_PATH, "wb") as f:
        f.truncate(0)
        members = await getMembersList(guild)
        member_ids = [member.id for member in members]
        members_dict = dict.fromkeys(member_ids, 0)
        pickle.dump(dict(members_dict), f)
        print("Reset the member messages dict")

async def getMembersList(guild, limit=None):
    members = await guild.fetch_members(limit=limit).flatten()
    return members

def getMember(client, arg): # Safe way of getting a member object
    if isinstance(arg, int):
        return client.get_user(arg) # If the argument is an int and thus an id, get the member object from that id
    elif isinstance(arg, discord.Member):
        return arg # If its a member object already, just return it normally
    else:
        raise discord.InvalidArgument # If its neither an id or a discord.Member object, raise an error
    
# def writeToDb(key, value): # Write to the replit db using a key and value pair
#     db[str(key)] = str(value)

# def deleteDbEntry(key): # Delete a db entry
#     try:
#         del db[str(key)] # Delete the entry from the replit db by using the key
#     except KeyError: 
#         return # If the db entry isnt found, do nothing
