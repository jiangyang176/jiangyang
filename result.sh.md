# jiangyang

# *********************************************************************************************************************
# 分析系统日志：interview_data_set.gz
# 分析系统日志得到关键信息，用 Json 的格式 POST 上传至服务器 ( https://foo.com/bar )，key 的名称在括号里

# 设备名称: (deviceName)
# 错误的进程号码: (processId)
# 进程/服务名称: (processName)
# 错误的原因（描述）(description)
# 发生的时间（小时级），例如 0100-0200，0300-0400, (timeWindow)
# 在小时级别内发生的次数 (numberOfOccurrence)
# *********************************************************************************************************************
gzcat interview_data_set.gz | head -n 500 | sed -e '1h;2,$H;$!d;g;s/\n\t/ /g' | awk -f log_yc.awk> data.json
# 上面的 head -n 500 主要是为了演示，只取头 500 行数据，真正的环境是取的整个数据文件的所有数据
curl -X POST -H "Content-Type: application/json" -d @data.json https://foo.com/bar
