# This will create graph of Twitter friends for the Twitter user central_user
# in this case, 'ncameronbritt'

# It gather info on 200 of central_user's friends, and does likewise for 
# each of those 200 users for a potential network of 40,000 friends and friends of friends.

#User info is put in a NetworkX directed graph, and then exported as graphml

# 15 min pauses are triggered by 'rate limit exceeded' errors recieved from Twitter API
# Replace APP_KEY, APP_SECRET, etc with your own credentials

import tweepy
import networkx as nx
import time

APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# create directional graph
G = nx.DiGraph()

# user whose friends and friends of friends we'll collect
central_user = 'ncameronbritt'

# function to get friends of friends -- looks just like main part...
def getFriends(top_user_id):
    
    try: 
        # get list of followers
        user_list = api.friends_ids(user_id=top_user_id)
        # get 200 followers -- chunk into to lists of 100
        group1 = api.lookup_users(user_list[:100])
        group2 = api.lookup_users(user_list[100:200])
        groups = [group1, group2]
        # iterate through chunks, friends
        for group in groups: 
            for friend in group:
                friend_id = friend.id
                friend_name = friend.screen_name
                followers_count = friend.followers_count
                G.add_node(friend_id, screen_name = friend_name, followers_count = followers_count)
                G.add_edge(top_user_id, friend_id)
                print "Getting names for %s" % friend_name


    except tweepy.TweepError as e:
        print e
        # pause for rate limit error
        if e.args[0][0]['code'] is 88: 
            print "Time out -- waiting for 15 minutes"
            print "Collected %r nodes so far." % len(G)
            time.sleep(15 * 60)
        # ignore other errors. maybe not a great idea...
        else: 
            pass



if __name__ == "__main__":        
    # get info on user we're interested in
    top_user = api.get_user(screen_name = central_user)
    top_user_id = top_user.id
    top_user_name = top_user.screen_name

    # print top_user_id
    print top_user_name
    G.add_node(top_user_id, screen_name = top_user_name)

    # get friends list
    # probably could/should do this with recursion if going deeper
    try: 
        user_list = api.friends_ids(user_id=top_user_id)
        # get 200 followers -- chunk into to lists of 100
        group1 = api.lookup_users(user_list[:100])
        group2 = api.lookup_users(user_list[100:200])
        groups = [group1, group2]
        # get friends first
        for group in groups: 
            for friend in group:
                friend_id = friend.id
                friend_name = friend.screen_name
                followers_count = friend.followers_count
                G.add_node(friend_id, screen_name = friend_name, followers_count = followers_count)
                G.add_edge(top_user_id, friend_id)
                print "Getting names for %s" % friend_name
        # now get friends of friends.         
        for group in groups:
            for friend in group:
                getFriends(friend.id)

    except tweepy.TweepError as e:
        print e
        # pause for rate limit error
        if e.args[0][0]['code'] is 88: 
            print "Time out -- waiting for 15 minutes"
            print "Collected %r nodes so far." % len(G)
            time.sleep(15 * 60)
        # ignore other errors. maybe not a great idea...
        else: 
            pass
            

        
    # how many nodes total?
    print "All done! The graph has %r nodes." % len(G)

    # write to graphml to use in Gephi or to import into Neo4j
    nx.write_graphml(G, "twitter_friends.graphml")
