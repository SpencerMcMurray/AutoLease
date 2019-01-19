import pymysql


class Database:
    def __init__(self):
        host = "den1.mysql6.gear.host"
        port = 3306
        user = "autolease"
        password = "Em56bP59!21_"
        db = "autolease"

        self.con = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        self.cur = self.con.cursor()
