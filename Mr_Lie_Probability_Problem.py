# SSR 1.5%
# SR 3%
# R 95.5%
# 每10连必定出SSR或者SR
# 抽中SSR或者SR之后重置10连计数
# 计算100次以内
# (1)第一次出现ssr的次数
# (2)出现ssr的次数

import random
import time
import numpy as np
import matplotlib.pyplot as plt

# 概率公示
card = {'SSR': 0.015, 'SR': 0.030, 'R': 0.955}

# 抽卡了，DD
def draw_card():

    # 第一次抽到SSR所用次数
    first_SSR = 0

    # 内置计数器
    counter = 0

    # 抽到卡种类
    card_count = {'SSR': 0, 'SR': 0, 'R': 0}

    # 抽卡100次
    for num in range(0, 200):

        # DD,你终于要出货了
        if counter == 9:

            # 计数器清零
            counter = 0

            res = random.uniform(0, card['SSR'] + card['SR'])

            # 你终于出货了，DD
            if res <= card['SSR']:

                if first_SSR == 0:
                    first_SSR = num + 1

                # 你又多了一个SSR
                card_count['SSR'] += 1

            else:
                # 太菜了，DD
                card_count['SR'] += 1

        else:
            res = random.uniform(0, 1)

            # NB嗷
            if res <= card['SSR']:

                if first_SSR == 0:
                    first_SSR = num

                card_count['SSR'] += 1
                counter = 0

            # 出货了，可惜是SR
            elif res <= card['SSR'] + card['SR'] and res > card['SSR']:
                card_count['SR'] += 1
                counter = 0

            # 非酋的命
            else:
                card_count['R'] +=1
                counter += 1

    #print('第一次抽中SSR是第' + str(first_SSR) + '次；SSR概率为' + str(card_count['SSR']) + '%')

    return first_SSR, card_count['SSR']

# 多次试验
def test(times):
    first_num_lst = [0,] * times
    SSR_num_lst = [0,] * times

    for num in range(0, times):
        first_num_lst[num], SSR_num_lst[num] = draw_card()

    return np.mean(first_num_lst), np.mean(SSR_num_lst)

# 画图
def main():

    test_num = ['1', '10', '50', '100', '200', '500', '1000', '5000', '10000', '50000', '100000', '500000', '1000000']

    length = len(test_num)
    first_num_avg_lst = [0,] * length
    SSR_num_avg_lst = [0,] * length

    for num in range(0, length):

        time_start = time.time()

        first_num_avg_lst[num], SSR_num_avg_lst[num] = test(int(test_num[num]))

        time_end = time.time()

        print(str(time_end - time_start) + 's [for ' + str(test_num[num]) + ' times]')

    plt.figure(figsize=(8, 10))
    plt.subplot(211)
    plt.plot(test_num, first_num_avg_lst)
    plt.title('AVERAGE \'FIRST TIME\' OF \'SSR\' & AVERAGE \'PROBABILITY\' OF \'SSR\'')
    plt.xlabel('time of test')
    plt.ylabel('\'first time\' of \'SSR\'')

    plt.subplot(212)
    plt.plot(test_num, SSR_num_avg_lst)
    plt.xlabel('times of test')
    plt.ylabel('\'probability\' of \'SSR\'')

    plt.show()

# 开始测试
if __name__ == "__main__":
    main()