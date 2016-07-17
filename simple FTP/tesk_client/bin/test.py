#!/usr/bin/env python3
#Created by xuchao on 16/7/4.
import time,sys
def view_bar(num,total):
    rate = num / total
    rate_num= int(rate * 100)
    r = '\r[%-100s]%d%%' % ('=' * rate_num,rate_num, )
    sys.stdout.write(r)
    sys.stdout.flush()

if __name__ == '__main__':
    for i in range(101):
        time.sleep(0.1)
        view_bar(i,100)