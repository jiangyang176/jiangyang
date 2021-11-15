'''
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install python-dateutil -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# @itchat.msg_register([TEXT])是封装好的自动回复装饰器，当接收到的消息是Text，即文字消息【群组消息需要+isGroupChat=True】
消息分类：
图片或表情（PICTURE）、录制（RECORDING）、附件（ATTACHMENT）、小视频（VIDEO）、文本（TEXT），
地图（MAP），名片（CARD），通知（NOTE），分享（SHARING），好友邀请（FRIENDS）、语音（RECORDING）、系统消息（SYSTEM）
itchat.send，可以一次性发送多条
参数：（内容，用户）
返回值：发送结果，是否发送成功，json数据
注意：文件地址不可为中文
内容：可为单独的字符串内容，其他有【@类型@地址】，类型有图片（img）、文件（fil）、视频（vid）
用户：省略则发个自己，不稳定，msg['FromUserName']表示指定用户为触发用户
创建后台任务【＆-免疫Ctrl + C，nohup-免疫关闭会话】
pip install itchat -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install xlwt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install requests -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

cd /var/mobile/Library/SMS
启动
nohup python3 itchatt.py> itchatt_log.txt &
检查
ps -ef | grep itchatt | grep -v grep
结束
kill -n 9 $(ps -ef | grep itchatt | grep -v grep| tr -s ' ' | cut -d ' ' -f 3)
'''
#coding=utf8
import itchat,time,xlwt,os,re
import requests
from xlwt import Workbook
from xlwt import Pattern
from dateutil.parser import parse
from itchat.content import PICTURE, RECORDING, ATTACHMENT, VIDEO,TEXT

def 解析短信(messagexls_cell):
    return_=[]
    if 'empty' in messagexls_cell:
        pass
    elif '华为Netcare快速预警' in messagexls_cell:

        pattern_text_3 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
        PM_TIME = (pattern_text_3.findall(messagexls_cell)[0])
        # print(PM_TIME)

        场景 = re.split(r'\n',messagexls_cell)
        # print(场景)
        for line in 场景:
            # print(line)
            if '场景' in line:
                子场景 = line.split('）')[1].replace('场景','').replace('成功率场景','')
            elif '华为Netcare快速预警' in line:
                pass
            elif '网元指标异常' in line:
                pattern_text_2 = re.compile(r'Top.*?）')
                top_2 = (pattern_text_2.findall(line))
                # print(top_2)
                for t2 in top_2:
                    PM_NE = str(t2).split('：')[1].split('，')[0]
                    # print(PM_NE)
                    if 'ISBG' in PM_NE:
                        NE_TYPE = 'CSCF'
                    elif 'SCCAS' in PM_NE:
                        NE_TYPE = 'SCCAS'
                    elif 'VOLTEAS' in PM_NE:
                        NE_TYPE = 'MTELAS'
                    elif 'PSBC' in PM_NE:
                        NE_TYPE = 'PSBC'
                    elif 'MGCF' in PM_NE:
                        NE_TYPE = 'MGCF'
                    else:
                        NE_TYPE = '未定义类型网元'
                    PM_NAME = str(t2).split('，')[1].split('：')[0]
                    阈值 = str(t2).split('阈值：')[1].replace('）', '')
                    现网值 = str(t2).split('：')[-2].replace('，阈值', '')
                    try:
                        # print([子场景, PM_NAME, NE_TYPE, PM_NE, PM_TIME, 现网值, 阈值])
                        return_.append([子场景, PM_NAME, NE_TYPE, PM_NE, PM_TIME, 现网值, 阈值,'Netcare快速预警'])
                    except:
                        pass
            else:
                pass
        return return_
    else:
        # print(messagexls_cell)
        messagexls_cell_fmt = re.sub(r'.*异常指标：|；\\n发生时间.*', '', messagexls_cell, flags=re.S)
        pattern_text_MOMT = re.compile(r'MO|MT|注册成功率场景')
        messagexls_cell_MOMT = re.findall(pattern_text_MOMT,messagexls_cell)
        # print(messagexls_cell_MOMT[0])
        pattern_text = re.compile(r'（TOP.*?）')
        pattern_阈值 = re.compile(r'^：[0-9]*，$')
        pattern_time = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
        for top in pattern_text.findall(messagexls_cell_fmt):
            # print(top)
            PM_NE = str(top).split('：')[1].split(' ')[0]
            # print(PM_NE)
            if 'ISBG' in PM_NE:
                NE_TYPE = 'CSCF'
            elif 'SCCAS' in PM_NE:
                NE_TYPE = 'SCCAS'
            elif 'VOLTEAS' in PM_NE:
                NE_TYPE = 'MTELAS'
            elif 'PSBC' in PM_NE:
                NE_TYPE = 'PSBC'
            elif 'MGCF' in PM_NE:
                NE_TYPE = 'MGCF'
            else:
                NE_TYPE = '未定义类型网元'
            PM_NAME = str(top).split('：')[1].replace(str(top).split('：')[1].split(' ')[0] + ' ', '')
            # print(PM_NAME)
            try:
                PM_TIME = str(pattern_time.findall(messagexls_cell)[-2])
            except:
                PM_TIME = '2020-99-99 99:99'
            阈值 = str(top).split('阈值：')[1].replace('）','')
            现网值 = str(top).split('：')[-2].replace('，阈值','')
            # print(PM_TIME)
            try:
                # data_arry = 条件读取数据库(tablename=id_dict2[PM_NAME][NE_TYPE], NENAME=PM_NE,
                #         ID=id_dict[PM_NAME][NE_TYPE],
                #         TIME_END=PM_TIME)
                return_.append([str(messagexls_cell_MOMT[0]).replace('成功率场景',''),PM_NAME, NE_TYPE, PM_NE, PM_TIME, 现网值,阈值,'普通预警'])
            except:
                print('**忽略分析**')
                pass
        return return_

def message_from_netcare():
    def time_MOD(timelist):
        timelist2 = int(timelist[:-9]) + 978307200
        timeArray = time.localtime(timelist2)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(otherStyleTime)
        return otherStyleTime

    ################【规则内容】############################

    def 已聚类注册类固话关联错误HSS():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '否', style)
        ws.write(n, 4, '否', style)
        ws.write(n, 5, '聚类的为固网号段，为未开户号码频繁注册导致；根因网元判断错误', style)
        ws.write(n, 6, '终端行为', style)
        ws.write(n, 7, '接入侧', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '建议根据AI辅助判断是否需要上报固网注册类高风险', style)
    def 当前周期暂未检测到相关错误码异常():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '是', style)
        ws.write(n, 4, '否', style)
        ws.write(n, 5, '无分析结果，结论准确为否', style)
        ws.write(n, 6, '未知', style)
        ws.write(n, 7, '未知', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '建议聚类SIP错误码', style)

    def IPTracert():
        ws.write(n, 2, '/', style)
        ws.write(n, 3, '/', style)
        ws.write(n, 4, '/', style)
        ws.write(n, 5, 'IPTracert告警不涉及', style)
        ws.write(n, 6, '承载网', style)
        ws.write(n, 7, '数通', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '建议关联对端IP所属网元名称', style)

    def 聚类电信联通号码():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '是', style)
        ws.write(n, 4, '是', style)
        ws.write(n, 5, '', style)
        ws.write(n, 6, '它网', style)
        ws.write(n, 7, '电路域', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '', style)

    def 生成487请求终止聚类号段():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '是', style)
        ws.write(n, 4, '是', style)
        ws.write(n, 5, '', style)
        ws.write(n, 6, '终端行为', style)
        ws.write(n, 7, '接入侧', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '', style)

    def 收到487请求终止聚类号段():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '是', style)
        ws.write(n, 4, '是', style)
        ws.write(n, 5, '', style)
        ws.write(n, 6, '终端行为', style)
        ws.write(n, 7, '接入侧', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '', style)

    def 收到503请求终止聚类号段():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '是', style)
        ws.write(n, 4, '是', style)
        ws.write(n, 5, '', style)
        ws.write(n, 6, '对端网元故障', style)
        ws.write(n, 7, 'IMS域', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '', style)

    def 收到403请求终止聚类号段():
        ws.write(n, 2, '是', style)
        ws.write(n, 3, '否', style)
        ws.write(n, 4, '否', style)
        ws.write(n, 5, '', style)
        ws.write(n, 6, '部分号码频繁注册失败引起', style)
        ws.write(n, 7, '终端', style)
        ws.write(n, 8, '接入侧', style)
        ws.write(n, 9, '', style)

    def 待分析():
        ws.write(n, 2, '-', style)
        ws.write(n, 3, '-', style)
        ws.write(n, 4, '-', style)
        ws.write(n, 5, '-', style)
        ws.write(n, 6, '未知', style)
        ws.write(n, 7, '未知', style)
        ws.write(n, 8, '未知', style)
        ws.write(n, 9, '-', style)

    while True:

        w = Workbook()  # 创建一个工作簿
        ws = w.add_sheet('华为Netcare风险短信', cell_overwrite_ok=True)  # 创建一个工作表#第二参数用于确认同一个cell单元是否可以重设值。
        ws_2 = w.add_sheet('风险反向验证表', cell_overwrite_ok=True)  # 创建一个工作表#第二参数用于确认同一个cell单元是否可以重设值。
        ws_3 = w.add_sheet('汇总统计', cell_overwrite_ok=True)  # 创建一个工作表#第二参数用于确认同一个cell单元是否可以重设值。
        first_col = ws.col(0)  # xlwt中是行和列都是从0开始计算的
        sec_col = ws.col(1);
        col0 = ws_2.col(0);
        col1 = ws_2.col(1);
        col2 = ws_2.col(2);
        col3 = ws_2.col(3);
        col4 = ws_2.col(4)
        col5 = ws_2.col(5);
        col6 = ws_2.col(6);
        col9 = ws_2.col(9)
        first_col.width = 256 * 22
        sec_col.width = 256 * 130
        col0.width = 256 * 18
        col1.width = 256 * 38
        col2.width = 256 * 18
        col3.width = 256 * 24
        col4.width = 256 * 18
        col5.width = 256 * 18
        col6.width = 256 * 18
        col9.width = 256 * 24
        tall_style = xlwt.easyxf('font:height 720;')  # 36pt,类型小初的字号

        # 普通基本样式----------------------------
        style = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式
        a1 = xlwt.Alignment()  # 设置居中
        a1.horz = 0x01  # 设置左端对齐
        a1.vert = 0x01  # 设置垂直居中
        style.alignment = a1
        style.alignment.wrap = 1  # 自动换行
        # 重点关注样式----------------------------
        style_ = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
        a1 = xlwt.Alignment()  # 设置居中
        a1.horz = 0x01  # 设置左端对齐
        a1.vert = 0x01  # 设置垂直居中
        style_.alignment = a1
        style_.pattern = pattern
        style_.alignment.wrap = 1  # 自动换行
        # -----------------------------------------
        ws.write(0, 0, '实际收到短信时间', style)
        ws.write(0, 1, '短信内容', style)
        ws.write(0, 2, '风险上报准确性', style)
        ws.write(0, 3, '网元定界准确性', style)
        ws.write(0, 4, '结论准确性', style)
        ws.write(0, 5, '准确性为否的原因', style)
        ws.write(0, 6, '隐患类型', style)
        ws.write(0, 7, '产品域', style)
        ws.write(0, 8, '隐患厂家', style)
        ws.write(0, 9, '风险原因', style)
        ws.write(0, 10, '短信时延优化建议', style)
        ws_2.write(0, 0, '异常场景', style)
        ws_2.write(0, 1, '指标名称', style)
        ws_2.write(0, 2, '网元类型', style)
        ws_2.write(0, 3, '网元名称', style)
        ws_2.write(0, 4, '开始时间', style)
        ws_2.write(0, 5, '现网值', style)
        ws_2.write(0, 6, '阈值', style)
        ws_2.write(0, 7, '短信序号', style)
        ws_2.write(0, 8, '抖动差值', style)
        ws_2.write(0, 9, '预警类型', style)
        
        ws_3.write(0, 0, '1：只有接通率异常，没有Oxx错误码，规则不再钻CHR，建议标注为定界准', style)
        ws_3.write(1, 0, '2：只有请求数异常，没有OXX异常，规则不再钻CHR，建议标注为定界准', style)
        ws_3.write(2, 0, '3：针对MGCF不明确错误码，如4XX合在一起的错误码统计，规则不再钻CHR，建议标注为定界准', style)
        ws_3.write(3, 0, '4：针对第三方注册场景，规则不再钻取CHR，建议标注为定界准', style)
        ws_3.write(4, 0, '5：本身没有接CHR，未汇聚，建议标注为定界准', style)
        ws_3.write(5, 0, '6：承载网问题受影响的本端网元多，对端网元已汇聚，本端可不做汇聚（客户会议确认），建议标注为定界准确', style)
        ws_3.write(6, 0, '7：对端地址不可达告警信息不全，无法确定告警是否与指标异常相关，建议聚类对端地址不可达告警信息：涉及短信内容呈现优化，建议先标注为定界准（分析优化方案）', style)
        ws_3.write(7, 0, '8：注册类场景，结论冗余信息过多，且未聚类到注册失败号码号段，涉及短信内容具体呈现优化，建议根据具体风险内容判定定界准确性（分析优化方案,分析钻取结论是否准确，打分规则是否合理，结合最近很多403风险告警来分析。）', style)
        ws_3.write(8, 0, '9：硬件告警与此指标异常无关（单板端口存在容灾备份）聚类网元错误，标注为不准确（具体分析）。', style)
        ws_3.write(9, 0, '10：骚扰号码扫描注册、呼叫导致，非网元问题，标注未不准确（分析优化方案）', style)
        ws_3.write(11, 0, '风险上报准确性', style)
        ws_3.write(11, 1, '网元定界准确性', style)
        ws_3.write(11, 2, '结论准确性', style)

        fo = open('Netcare_message.html', encoding='UTF-8')
        fl = fo.read()
        n = 1
        n_ = 1
        for i in fl.split('</TR>'):
            if '【华为Net' in i:
                m = 0
                for j in i.split('</TD>'):
                    if m == 0:
                        ID = str(j).replace('<TR><TD>', '')
                        m += 1
                        # ws.write(n, 0, str(ID), style)

                    elif m == 1:
                        m += 1
                        TIME = time_MOD(str(j).replace('<TD>', ''))
                        a_time = parse(str(TIME))
                        ws.write(n, 0, str(TIME), style)

                    elif m == 2:
                        if j != '\n' and '指标恢复情况' not in j and 'IP承载告警恢复' not in j:
                            TEXT = str(j).replace('<TD>', '').replace('\n', '', 1)
                            # print(' +' * 60)
                            # print(TEXT)
                            短信解析结果 = 解析短信(messagexls_cell=TEXT)
                            try:
                                # print('预写入表格信息',短信解析结果)
                                b_time = parse(str(TEXT).split('发生时间：')[1].split('；')[0].split('~')[1].lstrip())
                                a_b_time = '%.0f' % ((a_time - b_time).seconds / 60)
                                # print('%.0f' % ((a_time - b_time).seconds / 60))
                            except:
                                a_b_time = '-1'
                            ws.write(n, 1, TEXT, style)

                            for ll in range(len(短信解析结果)):
                                print(短信解析结果[ll])
                                ws_2.write(n_, 0, 短信解析结果[ll][0], style)
                                ws_2.write(n_, 1, 短信解析结果[ll][1], style)
                                ws_2.write(n_, 2, 短信解析结果[ll][2], style)
                                ws_2.write(n_, 3, 短信解析结果[ll][3], style)
                                ws_2.write(n_, 4, 短信解析结果[ll][4], style)
                                ws_2.write(n_, 5, 短信解析结果[ll][5], style)
                                ws_2.write(n_, 6, 短信解析结果[ll][6], style)
                                ws_2.write(n_, 7, n + 1, style)
                                ws_2.write(n_, 9, 短信解析结果[ll][7], style)
                                try:
                                    ws_2.write(n_, 8, str(int(短信解析结果[ll][5]) - int(短信解析结果[ll][6])), style)
                                except:
                                    pass
                                n_ += 1

                            if int(a_b_time) > 20:
                                ws.write(n, 10, a_b_time + '分钟短信延迟', style_)
                            else:
                                ws.write(n, 10, a_b_time + '分钟短信延迟', style)
                            ################【规则应用】############################

                            if '号码；' in str(TEXT):
                                聚类电信联通号码()
                            elif '生成487' in str(TEXT):
                                生成487请求终止聚类号段()
                                if '号段：' not in str(TEXT)  or 'TOP用户' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '疑似高频号码呼叫产生，需要聚类号段', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)

                            elif '收到487' in str(TEXT):
                                收到487请求终止聚类号段()
                                if '号段：' not in str(TEXT)  or 'TOP用户' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '疑似高频号码呼叫产生，需要聚类号段', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)

                            elif '收到503' in str(TEXT) or '生成503' in str(TEXT):
                                收到503请求终止聚类号段()
                                if '号段：' not in str(TEXT) or 'TOP用户' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '未聚类号段', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)
                                if '拆线网元：' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '未聚类拆线网元', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)

                            elif '收到403' in str(TEXT) or '生成403' in str(TEXT) or '403 请求禁止增加' in str(TEXT)\
                                    or 'S-CSCF初始注册成功率下降' in str(TEXT) or 'UAA失败响应次数增加' in str(TEXT) or 'I-CSCF注册成功率下降' in str(TEXT):
                                收到403请求终止聚类号段()
                                if '号码归属' in str(TEXT) and '注册成功率场景' in str(TEXT) and '+861' not in str(
                                        TEXT) and 'FE' in str(TEXT):
                                    已聚类注册类固话关联错误HSS()
                                    if '根因网元：+' in str(TEXT):
                                        ws.write(n, 3, '是', style)
                                        ws.write(n, 5, '聚类的为固网号段，为未开户号码频繁注册导致', style)
                                if '注册号段' in str(TEXT) and '注册成功率场景' in str(TEXT) and '+861' not in str(
                                        TEXT) and 'FE' in str(TEXT):
                                    已聚类注册类固话关联错误HSS()
                                    if '根因网元：+' in str(TEXT):
                                        ws.write(n, 3, '是', style)
                                        ws.write(n, 5, '聚类的为固网号段，为未开户号码频繁注册导致', style)
                                if '号段：' not in str(TEXT) or 'TOP用户' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '未聚类号段', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)
                                if '拆线网元：' not in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '未聚类拆线网元', style)
                                    ws.write(n, 9, '需要netcare分析未聚类原因', style)
                                if '呼叫失败' in str(TEXT):
                                    ws.write(n, 4, '否', style)
                                    ws.write(n, 5, '注册403和呼叫无关，结论场景描述错误', style)
                                    ws.write(n, 9, '需要netcare改进结论描述', style)

                            elif '当前周期暂未检测到相关错误码异常' in str(TEXT):
                                当前周期暂未检测到相关错误码异常()
                                if 'DS' in str(TEXT) or  'MGCF' in str(TEXT):
                                    ws.write(n, 9, '建议获取DS或MGCF的SIP信令消息测量，聚类SIP错误码', style)

                            elif '高危告警，IPTracert' in str(TEXT):
                                IPTracert()

                            else:
                                待分析()

                            ### 规则匹配原则：只能由上到下，匹配最先获取的规则！！！

                            n += 1
        print('本期短信数量：', n, ' 条.')
        ws.write(n, 0, 'END')
        w.save('Netcare_message_2020.xls')
        fo.close()
        # os.remove('Netcare_message_2020_[UTF-8].xml')
        # os.remove('Netcare_message_2020_[UTF-8].zip')
        return n

def find_all(s):
    res_list = []
    f_w = open('搜索结果.txt', 'w', encoding="UTF-8")
    for root, dirs, files in os.walk('01-20200727'):
        for name in (files):
            if '.txt' in name :
                print(name)
                try:
                    f = open(root + '/' + name, 'r', encoding="UTF-8")
                    text = f.readlines()
                    f.close
                except:
                    pass
                try:
                    f = open(root + '/' + name, 'r', encoding="GBK")
                    text = f.readlines()
                    f.close
                except:
                    pass

                for l_ in text:
                    if s in l_:
                        print(l_)
                        res_list.append(name+':'+l_+'\r')
                        f_w.write(name+':'+l_+'\r')
    f_w.close
    print(res_list)
    return res_list

@itchat.msg_register([TEXT])
def text_reply(msg):
    # 当消息是由非群组发出
    # print(msg)
    # print(msg['Text']);
    # if msg['User']['NickName'] == 'ZhangsR' and not msg['FromUserName'] == myUserName: # 智能回复
    if '可获取验证码' in msg['User']['RemarkName'] or 'NetCare' in msg['User']['RemarkName'] : # 智能回复: # 智能回复
        if '验证码' in msg['Text']:
            os.system('sqlite3 -html sms.db "select ROWID,date,text from message where [text] like \'%dwfanxiaolong3%\' order by date desc limit 0,1;" >/var/mobile/Library/SMS/4A_message.html')
            time.sleep(0.5)
            val = open('4A_message.html')
            message = val.readlines()
            print(message)
            return str(message)
            #select ROWID,date,text from message where [text] like '%短信口令%' order by ROWID desc limit 0,1;
        elif '短信统计'in msg['Text']:
            mess_num = int(msg['Text'].replace('短信统计',''))
            os.system(
                'sqlite3 -html sms.db "select ROWID,date,text from message where [text] like \'%【华为Net%\' order by date desc limit 0,{};" >/var/mobile/Library/SMS/Netcare_message.html'.format(mess_num))
            time.sleep(0.5)
            风险条数 = message_from_netcare()
            itchat.send_file('Netcare_message_2020.xls',toUserName=msg['User']['UserName'])
            return '最近{}条短信中，包含{}条风险短信，整理结果请查收：'.format(mess_num,风险条数)
        elif '配置查询'in msg['Text']:
            mess_ip = str(msg['Text'].replace('配置查询',''))
            
            itchat.send(u'正在查询，请稍等。。。', toUserName=msg['User']['UserName'])

            # time.sleep(0.5)

            res_ = find_all(mess_ip)

            # res_[1]发送为微信发送文件路径
            itchat.send_file('搜索结果.txt',toUserName=msg['User']['UserName'])

            return '配置查询{}结果{}个，请参考：'.format(mess_ip,len(res_))
            
        elif '集中注册'in msg['Text']:
            itchat.send(u'运行SE2600_集中注册分析一键式.py，分析结果正在输出，请稍后。。。', toUserName=msg['User']['UserName'])
            itchat.send_file('集中注册分析结果-同IP端口&带终端类型及用户号码.rar',toUserName=msg['User']['UserName'])
        elif '告警+'in msg['Text']:
            itchat.send(u'告警+功能建设中。。。\r\n*可自动输出网元当前告警及近一周历史告警报表', toUserName=msg['User']['UserName'])
        elif '指标+'in msg['Text']:
            itchat.send(u'指标+功能建设中。。。\r\n*可自动输出网元当前关键指标情况及近一周指标波动报表', toUserName=msg['User']['UserName'])
        elif 'MGW编解码+'in msg['Text']:
            itchat.send(u'MGW编解码+功能建设中。。。\r\n*可自动进行MGW编解码过载预测，输出建议执行脚本', toUserName=msg['User']['UserName'])
        elif '开户日志+'in msg['Text']:
            itchat.send(u'开户日志+功能建设中。。。\r\n*可自动输出指定日期开户增删改日志', toUserName=msg['User']['UserName'])
        elif '操作日志+'in msg['Text']:
            itchat.send(u'操作日志+功能建设中。。。\r\n*可自动输出指定日期网元操作日志', toUserName=msg['User']['UserName'])


        else :
            pass
            # return get_response(str(msg['Text']))['text']

def get_excel_wechatfrinends(friends):
    # 准备输出表
    w = xlwt.Workbook()
    ws = w.add_sheet('output')
    n = 1
    for i in friends:
        ws.write(n,0,i['NickName'])
        ws.write(n,1,i['RemarkName'])
        if i['Sex'] == 1:
            ws.write(n, 2, '男')
        elif i['Sex'] == 2:
            ws.write(n, 2, '女')
        else:
            ws.write(n, 2, '未知')
        ws.write(n,3,i['Province'])
        ws.write(n,4,i['City'])
        ws.write(n,5,i['UserName'])
        n+=1
    w.save('test_itchart.xls')

def send_email(email_body='备用机微信异常登出'):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.utils import formataddr
    from email.mime.multipart import MIMEMultipart

    my_sender = 'anshanfan@qq.com'  # 发件人邮箱账号
    my_pass = 'ajxqdjysbjizbfhc'  # 发件人邮箱密码
    my_user = 'fanxiaolongx@139.com'  # 收件人邮箱账号，我这边发送给自己

    def mail():
        ret = True
        try:
            msg = MIMEMultipart()
            # 构造附件1
            file1 = MIMEText(open('itchatt_log.txt', 'rb').read(), 'base64', 'utf-8')
            file1["Content-Type"] = 'application/octet-stream'
            file1["Content-Disposition"] = 'attachment; filename="itchatt_log.txt"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            msg.attach(file1)
            # msg = MIMEText('邮件内容QR.png', 'plain', 'utf-8')
            msg['From'] = formataddr(["NetCare_message_email", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = email_body  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

if __name__ == '__main__':
    def ldong():
        print('******微信登入******')
    def edong():
        print('++++++微信登出++++++')

    while True:
        try:
            # 登入
            itchat.auto_login(hotReload=True, loginCallback=ldong, exitCallback=edong, enableCmdQR=2)
            # itchat.auto_login(hotReload=True, loginCallback=ldong, exitCallback=edong)
            itchat.send(u'备用机微信启动', '')
            friends = itchat.get_friends(update=True)[0:]
            get_excel_wechatfrinends(friends)
            # 获取自己的UserName
            myUserName = itchat.get_friends(update=True)[0]["UserName"]
            print (myUserName)
            itchat.run()
        except:
            send_email('备用机微信异常登出')
            pass
