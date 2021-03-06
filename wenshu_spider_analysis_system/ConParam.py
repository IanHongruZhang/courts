###-*-encoding:utf-8-*-###
### 构造检索条件 ####
# 检索关键词
def Param_Structure(key,stindex,clindex,count_tlindex,case_tlindex,cpindex,wtindex):
    keyword = key
    # 检索类型
    search_type_list = ['全文检索', '首部', '事实', '理由', '判决结果', '尾部']
    search_type = search_type_list[stindex]
    # 案由
    case_list = ['全部', '刑事案由', '民事案由', '行政案由', '赔偿案由']
    case = case_list[clindex]
    # 法院层级
    court_type_list = ['全部', '最高法院', '高级法院', '中级法院', '基层法院']
    court_type = court_type_list[count_tlindex]
    # 案件类型
    case_type_list = ['全部', '刑事案件', '民事案件', '行政案件', '赔偿案件',
                      '执行案件']
    case_type = case_type_list[case_tlindex]
    # 审判程序
    case_process_list = ['全部', '一审', '二审', '再审', '复核', '刑罚变重', '再审审查与审判监督',
                         '其他']
    case_process = case_process_list[cpindex]
    # 文书类型
    wenshu_type_list = ['全部', '裁判书', '调解书', '决定书', '通知书', '批复', '答复',
                        '函', '令', '其他']
    wenshu_type = wenshu_type_list[wtindex]
    # 裁判日期
    start_date = '2018-05-15'
    end_date = '2018-05-16'
    # 法院地域，需要二次获取，判断那些省份的法院有数据
    court_loc_list = ['全部']
    court_loc = court_loc_list[0]
    # 法院名称
    court_name_list = ["全部"]
    court_name = court_name_list[0]

    param_list = []
    param_list.append("{0}:{1}".format(search_type, keyword))
    if case != '全部':
        param_list.append("案由:{}".format(case))
    if court_type != '全部':
        param_list.append("法院层级:{}".format(court_type))
    if case_type != '全部':
        param_list.append("案件类型:{}".format(case_type))
    if case_process != '全部':
        param_list.append("审判程序:{}".format(case_process))
    if wenshu_type != '全部':
        param_list.append("文书类型:{}".format(wenshu_type))
    # param_list.append("裁判日期:{0} TO {1}".format(start_date, end_date))
    if court_loc != '全部':
        param_list.append("法院地域:{}".format(court_loc))
    if court_name != '全部':
        param_list.append("法院名称:{}".format(court_loc))

    Param = ','.join(param_list)
    return Param