import MySQLdb

#This backup the data into the database, the data type is something like
#{VAL1,VAL2,...,VALn} where 'VALi' is a dictionary
def backup_data(bot_name,user,password,host,data):
	try:
		db = MySQLdb.connect(user=user,passwd=password,host=host)
		cursor = db.cursor()
		cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(bot_name))
		cursor.execute('use {}'.format(bot_name))
	except:
		print("Error with database")
		return
	for value in data:
		cursor.execute('CREATE TABLE IF NOT EXISTS {}(server_id TEXT CHARACTER SET \'utf8\', name VARCHAR(1024) CHARACTER SET \'utf8\', value TEXT CHARACTER SET \'utf8\',UNIQUE(name))'.format(value))
		for key in data[value]:
			if isinstance(data[value][key],dict):
				server_id = key
				for info in data[value][key]:
					content = data[value][key][info].replace("'",r"\'")
					nm = info.replace("'",r"\'")
					cursor.execute('INSERT INTO {}(server_id,name,value) VALUES (\'{}\',\'{}\',\'{}\') ON DUPLICATE KEY UPDATE value= \'{}\''.format(
									value,server_id,nm,content,content))
			else:
				content = str(data[value][key]).replace("'",r"\'")
				cursor.execute('INSERT INTO {}(server_id,name,value) VALUES (\'0\',\'{}\',\'{}\') ON DUPLICATE KEY UPDATE value=\'{}\''.format(
					value,str(key),content,content))
	db.commit()
	#Close connection
	cursor.close()
	db.close()

def load_from(bot_name,user,password,host):
	data = {}
	db = MySQLdb.connect(user=user,passwd=password,host=host)
	cursor = db.cursor()
	try:
		cursor.execute('use {}'.format(bot_name))
	except:
		print("No backup created")
		return
	cursor.execute('show tables')
	names = [i[0] for i in cursor.fetchall()]
	for name in names:
		data[name] = {}
		cursor.execute('SELECT DISTINCT server_id FROM {}'.format(name))
		ids = [i[0] for i in cursor.fetchall()]
		#This is weathers
		cursor.execute('SELECT * from {}'.format(name))
		if len(ids) == 1 and ids[0] == '0':
			for info in cursor.fetchall():
				data[name][info[1]] = info[2]
		else:
			for info in cursor.fetchall():
				if info[0] not in data[name]:
					data[name][info[0]] = {}
				data[name][info[0]][info[1]] = info[2]
	return data