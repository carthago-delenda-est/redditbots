#!/usr/bin/env python
# coding: utf-8

import praw, re, json, sys, os
from functools import reduce

sys.path.insert(1, '../')
import BotUtils



def should_respond(msg):
    parts = msg.split(" ")
    return len(parts) == 2 and parts[0].lower() == "u/wordfreqcountbot"
    

def process_message(msg, dryrun=False):
    if not dryrun:
        msg.mark_read()
    
    if not should_respond(msg.body):
        return
    
    parts = msg.body.split(" ")
    target = msg.parent().author.name
    
    word_target = parts[1].strip("\\")

    print(f"Processing message {msg.id} for {target} using word {word_target}.  dryrun?: {dryrun}")
    
    reply_comment = produce_reddit_comment(target, word_target)

    if not dryrun:
        msg.reply(reply_comment)
        
    return(reply_comment)

def get_all_instances_of_word(text_collection, word):
    pattern = re.compile(r"\b(%s[s]*)\b" % word, re.IGNORECASE)
    results = []
    for item in text_collection:
        if type(item) is praw.models.reddit.submission.Submission:
            text = item.selftext
            url = item.url
        else: #i.e it is a comment
            text = item.body
            url = item.permalink
            
        match = pattern.search(text)
        if match:
            results.append({
                'id': item.id,
                'context': text[max(0, match.start(1)-50):match.end(1)+50].replace('\n', ' '),
                'url': url if "https://" in url else f"https://reddit.com{url}",
                'target': word
            })
            
    return results


def bold_word_in_str(s, word):
    pattern = re.compile(r"\b(%s[s]*)\b" % word, re.IGNORECASE)
    word_to_bold = pattern.search(s).group()
    return pattern.sub(f"**{word_to_bold.upper()}**", s)

def produce_reddit_comment(username, search_target):
    targets = TARGETS.get(search_target, [search_target])
    comments = BotUtils.get_all_comments(reddit, username)
    submissions = BotUtils.get_all_submissions(reddit, username)
    comment_matches = reduce(lambda accumulator, value: accumulator + value, [get_all_instances_of_word(list(comments.values()), target) for target in targets], []) 
    submission_matches = reduce(lambda accumulator, value: accumulator + value, [get_all_instances_of_word(submissions.values(), target) for target in targets], []) 
    
    line_0 = f"Examing history for user {username} and use of {search_target}. \n\nComments: {len(comment_matches)} out of {len(comments)}.  **{BotUtils.pretty_decimal(len(comment_matches) / len(comments))}%**"
    line_1 = f"Submissions: {len(submission_matches)} out of {len(submissions)}.  **{BotUtils.pretty_decimal(len(submission_matches) / len(submissions))}%**"
    
    table_headings = "|Word|Context|Link|"
    table_row = "|-|-|-|"
    
    all_matches = comment_matches + submission_matches
    table_row_lines = [f"|{m['target']}|{bold_word_in_str(m['context'], m['target'])}|[Link]({m['url']})|" for m in all_matches]
    
    rows_omitted_line = "Table limited to 20 rows." if len(table_row_lines) > 20 else ""
    
    table_row_lines = "\n".join(table_row_lines[0:20])
    
    explain_line = f"Summon the bot with a list of words.  Supported lists: {', '.join(list(TARGETS.keys()))}.  Please give feedback or suggest additional word lists in the bot's subreddit."
    
    return f"{line_0}\n\n{line_1}\n\n{table_headings}\n{table_row}\n{table_row_lines}\n\n{rows_omitted_line}\n\n{explain_line}"


if __name__ == "__main__":
    reddit = praw.Reddit(client_id=os.environ.get('WORDFREQCOUNTBOT_ID'),
                     client_secret=os.environ.get('WORDFREQCOUNTBOT_SECRET'),
                     user_agent='Script',
                     username="WordFreqCountBot",
                     password=os.environ.get('WORDFREQCOUNTBOT_PASSWORD')
                    )

    TARGETS = json.load(open('WordLists.json', 'r'))['lists']

    my_messages = [message for message in reddit.inbox.unread()]

    for message in my_messages:
        print(process_message(message, dryrun=len(sys.argv) > 1 and sys.argv[1] == "dryrun"))


