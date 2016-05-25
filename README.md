# Twitter-friend-network

This will create graph of Twitter friends for the Twitter user central_user
in this case, 'ncameronbritt'

It gather info on 200 of central_user's friends, and does likewise for 
each of those 200 users for a potential network of 40,000 friends and friends of friends.

User info is put in a NetworkX directed graph, and then exported as graphml

15 min pauses are triggered by 'rate limit exceeded' errors recieved from Twitter API
Replace APP_KEY, APP_SECRET, etc with your own credentials
