# redditbots
A collection of reddit bots

## WordFreqCountBot
Listens for messages containing it's username, space, a word.  The bot then searches the reddit comment and selfpost history of the author of the parent comment to the one that invoked it for instances of the word and replies to the comment that invoked with a list of examples of the parent author using that word.  If the word is in the "word list" (prefixed with a hash) then the bot will search for any of the words in the word list.

Example:

Comment A - "Blah, blah blah"

    ----> Comment B - "u/WordFreqCountBot hello".  
    
We say Comment B has invoked the bot to search the history of the author of Comment A for instances of the word 'hello'.  Plurals, with an 's', are also found, though the word as a substring of other words should not be.



 To add to the word lists edit the file WordLists.json.

 To run the bot, just run the WordFreqCountBot.py script.  The bot is "in production" so to speak as a cron job that runs the script every fifteen minutes.  If you run the bot with the word "dryrun" as the first argument (e.g. python WordFreqCountBot.py dryrun) then the script will not actually mark any messages as read or actually reply to anyone, but will instead just print out what it would have replied with.  This is useful for testing.
