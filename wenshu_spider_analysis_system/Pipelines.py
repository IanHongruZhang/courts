from Mysql import Sql
import pymongo

class Save(object):
    def __init__(self,result):
        self.result = result

    def GeneralPipelines(self):
        pass

    def MysqlPipelines(self):
        for item in self.result:
            print(item)
            id_wenshu = item['id']
            ret = Sql.select_name(id_wenshu)
            if ret[0] == 1:
                print("已经存在了")
                pass
            else:
                name = item['name']
                type = item['type']
                date = item['date']
                number = item['number']
                court = item['court']
                Sql.insert_caipanwenshu(id_wenshu,name,type,date,number,court)
                print("Mysql已存储")

    def MongoPipelines(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['caipanwenshu']
        mycol = mydb["wenshu_infos"]
        try:
            mycol.insert_one(self.result)
            print("Mongodb已存储")
        except Exception as e:
            print("Mongodb Error")