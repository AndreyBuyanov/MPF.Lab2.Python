from components.db import Db


class Urls:
    @staticmethod
    def getUrlsList():
        conn = Db.getConnection()
        cur = conn.cursor()
        cur.execute("SELECT `id`, `url`, `clicks` FROM `urls` ORDER BY ID DESC")
        return cur.fetchall()

    @staticmethod
    def incrementUrl(url):
        conn = Db.getConnection()
        cur = conn.cursor()
        cur.execute("UPDATE `urls` SET `clicks` = `clicks` + 1 WHERE `url`='{}'".format(url))
        conn.commit()

    @staticmethod
    def addUrl(url):
        conn = Db.getConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO `urls`(`url`) VALUES ('{}')".format(url))
        conn.commit()

    @staticmethod
    def removeUrlById(id):
        conn = Db.getConnection()
        cur = conn.cursor()
        cur.execute("DELETE FROM `urls` WHERE `id`='{}'".format(id))
        conn.commit()

