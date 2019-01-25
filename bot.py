import praw
import config
import os

reddit = praw.Reddit(username=config.username,
                  password=config.password,
                  client_id=config.client_id,
                  client_secret=config.client_secret,
                  user_agent=config.user_agent)


def this_blew_up_reply(reddit):
    search_results = reddit \
        .subreddit(config.subreddit) \
        .search(config.search_query, sort=config.search_sort, time_filter=config.search_time_sort)

    # Create a list
    if not os.path.isfile(config.filepath):
        posts_replied_to = []

    # Or load the list of posts we have replied to
    else:
        with open(config.filepath, "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    counter = 0

    for submission in search_results:
        if submission.id not in posts_replied_to:
            submission.reply(config.response)
            counter += 1
            posts_replied_to.append(submission.id)
        else:
            print('already replied to post id = {}'.format(submission.id))

    print("number of submissions replied to = {}".format(counter))

    # Write updated list to file
    with open(config.filepath, "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")


def delete_self_comment(reddit):
    deleted_comments = []
    comments = reddit.redditor(config.username).comments.new(limit=None)
    for comment in comments:
        if comment.score <= config.comment_delete_threshold:
            deleted_comments.append(comment.id)
            comment.delete()

    print('number of deleted comments = {}'.format(len(deleted_comments)))


this_blew_up_reply(reddit)
delete_self_comment(reddit)
