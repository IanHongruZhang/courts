#-*-encoding:utf-8-*-
import ConParam
import Request
if __name__ == '__main__':
    """
        7个值按照顺序给下面附上参数
        key：关键词,str
        stindex:[0:'全文检索', 1:'首部', 2:'事实', 3:'理由', 4:'判决结果',5:'尾部'] int
        clindex:[0:'全部', 1:'刑事案由', 2:'民事案由', 3:'行政案由', 4:'赔偿案由'] int
        count_tlindex:[0:'全部',1:'最高法院',2:'高级法院',3:'中级法院',4:'基层法院'] int
        case_tlindex:[0:'全部',1:'刑事案件',2:'民事案件',3:'行政案件',4:'赔偿案件',5:'执行案件'] int
        cpindex:[0:'全部',1:'一审',2:'二审',3:'再审',4:'复核',5:'刑罚变重',6:'再审审查与审判监督',7:'其他'] int
        wtindex:[0:'全部',1:'裁判书',2:'调解书',3:'决定书',4:'通知书',5:'批复',6:'答复',7:'函',8:'令',9:'其他'] int
    """
    Param = ConParam.Param_Structure("保险",0, 0, 0, 0, 0, 0)
    print(Param)
    Page = 20 # 每页几条
    Order = "法院层级"  # 排序标准
    Direction = "asc"  # asc正序 desc倒序
    result = Request.get_data(Param,Page,Order,Direction)
    print("data_save",result)