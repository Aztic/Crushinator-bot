# Nyoko-bot
A ~~beautiful~~ discord bot

## Requirements
- [Discord.py](https://github.com/Rapptz/discord.py)
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Html5libs](https://github.com/html5lib/html5lib-python) (optional, you can use another parsing lib)

### Optional clients
- [Anilist Client](https://github.com/noisypixy/python-anilist)
- [Riot api client](https://github.com/Aztic/riot-api-client)
- Openweather client

For almost every client, you'll need respective API's token. Put them in "tokens" section of "config" file.


### Config
  You have a config file with JSON format where you can put some "simple" options, like database integration.
  
### Database integration
  #### Requirements
  - [MySQL](https://www.mysql.com/)
  - [MySQLdb](https://sourceforge.net/projects/mysql-python/)
  
  If you wish, you can make Nyoko backup the data in your database. It'll create the database and respective tables if they doesn't exists.
For words and weather information, it have this style

| server_id | name | value |
|-----------| ------| -------|
|   id_1    |name1 |value1 |
|   id_2    | name2 | value2 |
|   ....    | ..... | ...... |
|   id_n    | name_n | value_n |


