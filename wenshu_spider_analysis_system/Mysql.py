import mysql.connector

'''
MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_USER
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

`id` int(11) NOT NULL AUTO_INCREMENT,
`id_wenshu` varchar(255) DEFAULT NULL,
`name` varchar(255) DEFAULT NULL,
`type` varchar(255) DEFAULT NULL,
`date` varchar(255) DEFAULT NULL,
`number` varchar(255) DEFAULT NULL,
`count` varchar(255) DEFAULT NULL,
'''

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '945180zyj'
MYSQL_PORT = '3306'
MYSQL_DB = 'spiders'

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT, host=MYSQL_HOSTS,
                              database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_caipanwenshu(cls, id_wenshu, name, type, date, number, court):
        sql = 'INSERT INTO caipanwenshu (`id_wenshu`,`name`,`type`,`date`,`number`,`court`) VALUES (%(id_wenshu)s,%(name)s,%(type)s,%(date)s,%(number)s,%(court)s)'
        value = {
            'id_wenshu': id_wenshu,
            'name': name,
            'type': type,
            'date': date,
            'number': number,
            'court': court,
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls, id_wenshu):
        sql = 'SELECT EXISTS(SELECT 1 FROM caipanwenshu WHERE id_wenshu=%(id_wenshu)s)'
        value = {
            'id_wenshu': id_wenshu
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]