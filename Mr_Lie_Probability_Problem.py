# SSR 1.5%
# SR 3%
# R 95.5%
# 每10连必定出SSR或者SR
# 抽中SSR或者SR之后重置10连计数
# 计算100次以内
# (1)第一次出现ssr的次数
# (2)出现ssr的次数

import random

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
    for num in range(0, 100):

        # DD,你终于要出货了
        if counter == 9:

            # 计数器清零
            counter = 0

            res = random.uniform(0, card['SSR'] + card['SR'])

            # 你终于出货了，DD
            if res <= card['SSR']:

                if first_SSR == 0:
                    first_SSR = num

                # 你又多了一个SSR
                card_count['SSR'] += 1

            else:
                card_count['SR'] += 1

        else:
            res = random.uniform(0, 1)

            if res <= card['SSR']:

                if first_SSR == 0:
                    first_SSR = num

                card_count['SSR'] += 1
                counter = 0

            elif res <= card['SSR'] + card['SR'] and res > card['SSR']:
                card_count['SR'] += 1
                counter = 0

            else:
                card_count['R'] +=1
                counter += 1

    print('第一次抽中SSR是第' + str(first_SSR) + '次；SSR概率为' + str(card_count['SSR']) + '%')


# 画图
def main():
    pass


draw_card();
