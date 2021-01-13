import mariadb


db_config = {
    'host': 'mariadb',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'lab2_python'
}


class Db:
    @staticmethod
    def getConnection():
        return mariadb.connect(**db_config)
