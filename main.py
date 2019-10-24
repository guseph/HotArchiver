# main.py
import mySQLInterface
import pushshiftInterface
import time
import pprint

def list_help_commands():
    print('Available Commands:')
    print('HELP : Prints a list of available commands.')
    print('ARCHIVE : Archives a subreddit using the top 100 results within hour intervals.')
    print('ADVANCED : Like ARCHIVE, but provides finer control over archival process. Expect additional input statements.')
    print('CLEAR: Deletes an archived subreddit after confirmation.')
    print('QUIT : Exits the program.')

def archive_subreddit(dataB: mySQLInterface.DBInstance, subreddit: str, hours:int=1, size:int=100):
    JUNE_22_2005_REDDIT_START_EPOCH_TIME = 1119398400
    if 'r/' in subreddit:
        subreddit = subreddit[2:]   # strips the r/ if users provided the subreddit with this prefix

    dataB.change_table(subreddit)
    
    try:
        for hour in range(int(time.time()), JUNE_22_2005_REDDIT_START_EPOCH_TIME, -3600 * hours):  # 3600 seconds = 1 hour
            use_response_dict = pushshiftInterface.get_request('/reddit/submission/search', {'subreddit': subreddit, 'sort_type':'score', 'sort':'desc', 'filter':['id', 'created_utc', 'author', 'score', 'title', 'url'], 'size':size, 'before':f'{hour}', 'after':f'{hour - 3600 * hours}'})

            authors = []
            created_utcs = []
            sub_ids = []
            scores = []
            titles = []
            urls = []

            for post in use_response_dict['data']:
                authors.append(post['author'])
                created_utcs.append(post['created_utc'])
                sub_ids.append(post['id'])
                scores.append(post['score'])
                titles.append(post['title'])
                urls.append(post['url'])
            
            dataB.insert_many_records(subreddit, authors, created_utcs, sub_ids, scores, titles, urls)

            if hour < JUNE_22_2005_REDDIT_START_EPOCH_TIME:
                break
        print(f'Archival of subreddit {subreddit} complete.')
    except pushshiftInterface.HTTPError as he:
        print(f'HTTP Error Code: {he.error_code()}')


def clear_subreddit_archive(dataB: mySQLInterface.DBInstance, subreddit: str):
    user_confirm = input(f'Are you sure you wish to clear {subreddit}\'s archive? [y/n]: ')
    if user_confirm == 'y':
        dataB.clear_table(subreddit)
    elif user_confirm == 'n':
        print(f'Archive for {subreddit} will not be deleted.')
    else:
        print(f'Invalid input, returning to main menu.')

    

if __name__ == "__main__":
    print('Connecting to server.')

    print('Initializing MySQL Database Instance. Database preconfigured to \'redditarc\'')

    dataB_instance = mySQLInterface.DBInstance('redditarc')  # connects to an online MySQL server, using 'redditarc' as the database storing archives in tables

    while True:   # Execution loop
        user_input = input('Enter a command. Type HELP for available commands: ')
        if user_input == 'QUIT':
            break
        elif user_input == 'HELP':
            list_help_commands()
        elif user_input == 'ARCHIVE':
            archive_subreddit(dataB_instance, input('Choose a subreddit to archive: '))
        elif user_input == 'ADVANCED':
            archive_subreddit(dataB_instance, input('Choose a subreddit to archive: '), int(input('Enter hour interval: ')), int(input('Enter size of results to retrieve each hour interval: ')))
        elif user_input == 'CLEAR':
            clear_subreddit_archive(dataB_instance, input('Choose a subreddit to clear: '))



    
