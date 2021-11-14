题目：
319. 灯泡开关
初始时有 n 个灯泡处于关闭状态。第一轮，你将会打开所有灯泡。接下来的第二轮，你将会每两个灯泡关闭一个。
第三轮，你每三个灯泡就切换一个灯泡的开关（即，打开变关闭，关闭变打开）。第 i 轮，你每 i 个灯泡就切换一个灯泡的开关。直到第 n 轮，你只需要切换最后一个灯泡的开关。
找出并返回 n 轮后有多少个亮着的灯泡。


class Solution:
    def bulbSwitch(self, n: int) -> int:
        if n==0:
            return 0
        elif n ==1:
            return 1
        tp = [0*i for i in range(n+1)]
        # print(tp)
        for x in range(1,n+1):
            for m in range(x, n+1,x):
                tp[m] +=1
                tp[m] = tp[m]%2
            # print(tp)
        return sum(tp)
yc_put =int(input("请输入有多少盏灯"))
yc_out = Solution().bulbSwitch(yc_put)
print("还有{}盏灯亮着".format(yc_out))


解题方案二： 对于n 而言，约数为奇数个时为开，偶数个为关； 所以x**2 != n n的约数为奇数个出现的
class Solution:
    def bulbSwitch(self, n: int) -> int:
        return int(sqrt(n+0.5))
yc_put =int(input("请输入有多少盏灯"))
yc_out = Solution().bulbSwitch(yc_put)
print("还有{}盏灯亮着".format(yc_out))
