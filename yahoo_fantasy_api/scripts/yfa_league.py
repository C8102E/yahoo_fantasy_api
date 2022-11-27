#!/bin/python

"""
Show the leagues you are a part of

"""
# from docopt import docopt
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from yahoo_fantasy_api import oauth2_logger

#MongoDB imports
import os
import pymongo
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

# map environment variables 
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")

# Mongo DB client connection
client = pymongo.MongoClient(f"mongodb+srv://admin:{MONGODB_PASSWORD}@cluster0.u3xxak7.mongodb.net/?retryWrites=true&w=majority")

# Mongo database name
fanyasy_db = client.nfl_fantasy

"""
☐ To Do ☑
--------------------------------------------------------
☑ Store results in MongoDB
☑ MongoDB dashboard a league table

☐ Make year of game dynamic

☐ Bring OAuth in
☐ Bring yfa.game function in
☐ Bring yfa.leauge function in

☐ Pause, consider extracting the useful modules of code 

--------------------------------------------------------
"""


if __name__ == '__main__':
    # args = docopt(__doc__, version='1.0')

    oauth2_logger.cleanup()

    creds = OAuth2(None, None, from_file='json')
    game = yfa.Game(creds, 'nfl')
    league_ids = game.league_ids(year='2022')
    for league_id in league_ids:
        if league_id.find("auto") > 0:
            continue
        league = yfa.League(creds, league_id)
        standings = league.standings()
        print("")
        print(league_id)
        for standing in standings:
            # print("{}".format(standing))
            # Write MongoDB code here
            collection = fanyasy_db.league
            collection.insert_one(standing)
        print("Write to database successful")
        # print(lg.settings())
