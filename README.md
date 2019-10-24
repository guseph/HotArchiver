# HotArchiver
This Reddit application fetches specified number of "Hot" submissions in a subreddit within a time interval and archives it in a MySQL database.

# Current Functionality
* HTTPS Get request for accessing pushshift.io Reddit API.
* MySQL interface using Python's mysql.connector to access a local MySQL database.
* Menu allowing for hourly archival or more advanced options.

# Planned Updates
* Allow users to view the database tables and search for specific titles, scores, or urls.
* Interface with tkinter instead of just the Python terminal.