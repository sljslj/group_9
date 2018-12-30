# _*_ coding:utf-8 _*_
import csv
import re
import time
import os

movieData = []

moviePath = 'cuckoo\\data\\movie_data'
actorPath = 'cuckoo\\data\\actor_data'
historyPath = 'cuckoo\\data\\history'

# moviePath = 'data\\movie_data'
# actorPath = 'data\\actor_data'
# historyPath = 'data\\history'


def open_movie_file():  # 打开文件
    global movieData
    with open(moviePath, 'r', encoding='UTF-8') as initMovieFile:
        movie_file = csv.reader(initMovieFile, delimiter=',')
        flag = False
        for row in movie_file:
            if not flag:
                flag = True
            else:
                if not row == [] and not row[0] == "make_in":
                    movieData.append(row)

    return


def data_processing():  # 预处理文件
    global movieData

    for row in movieData:  # 删去数字项的其他符号
        if not row[1]:
            row[1] = "0"
        if row[2] == "万":
            row[1] = str(float(row[1]) / 10000)
        del (row[2])

        row[8] = re.sub("\\D", "", row[8])
        row[10] = re.sub("\\D", "", row[10])

        row[0] = row[0].split(',')
        row[2] = row[2].split('/')
        row[5] = row[5].split('-')
        row[7] = row[7].split('/')
        row[9] = row[9].split(',')

    movieData.sort(key=lambda x: x[10], reverse=True)  # 去重
    i = 0
    while i < len(movieData):
        if i and movieData[i][3] == movieData[i - 1][3]:
            movieData.pop(i)
        else:
            i += 1

    for row in movieData:
        if len(row[6]) > 3:
            row[6] = "-1"

    count = len(movieData) - 1
    while count >= 0:
        if not len(movieData[count][5]) == 3 or int(movieData[count][5][0]) < 2015 \
                or int(movieData[count][5][0]) > 2018:
            del (movieData[count])
        count -= 1

    for row in movieData:
        if len(row[5][2]) == 6:
            row[5][2] = re.sub("\\D", "", row[5][2])
        else:
            row[5][2] = row[5][2].split(' ')
            row[5][2] = row[5][2][0]

    return


def month_in_quarter(movie_month, movie_quarter):  # 判断月份是否在当前季度里
    for item in movie_quarter:
        if not item:
            continue
        if int(item) * 3 - 2 <= int(movie_month) <= int(item) * 3:
            return True
    return False


def has_month(current_month, movie_month):  # 判断是否包含当前月份
    for item in movie_month:
        if not item:
            continue
        if int(current_month) == int(item):
            return True
    return False


def all_empty(input_str):  # 判断是否全空
    for item in input_str:
        if item:
            return False
    return True


def select(movie_area, movie_type, movie_year, movie_quarter, movie_month):  # 筛选电影
    movie_area = movie_area.split('-')
    movie_type = movie_type.split('-')
    movie_year = movie_year.split('-')
    movie_quarter = movie_quarter.split('-')
    movie_month = movie_month.split('-')

    current_movie = []

    for row in movieData:
        flag = False
        for item in row[0]:  # 上映地点
            if all_empty(movie_area) or item in movie_area:
                flag += True
                break

        for item in row[9]:  # 电影类型
            if all_empty(movie_type) or item in movie_type:
                flag += True
                break

        if all_empty(movie_year) or row[5][0] in movie_year:  # 上映时间
            flag += True

        if all_empty(movie_quarter) or month_in_quarter(row[5][1], movie_quarter):  # 上映时间
            flag += True

        # print(row[5][2])
        if all_empty(movie_month) or has_month(row[5][1], movie_month):  # 上映时间
            flag += True

        if flag == 5:
            current_movie.append(row)

    return current_movie


def search(input_str):  # 搜电影/搜演员/搜导演
    history_update(input_str, "search")
    search_result = []

    if not input_str:
        return search_result

    search_result = simple_cmp(movieData, input_str)

    if input_str.isalpha() and not input_str == input_str.title():
        input_str = input_str.title()
        temp = simple_cmp(movieData, input_str)
        for row in temp:
            search_result.append(row)

    return search_result


def simple_cmp(cmp_movie_area, input_str):  # 判断是否查找到
    if not input_str or (input_str.isdigit() and len(input_str) < 8):
        return

    search_result = []

    for row in cmp_movie_area:
        for item in row:
            flag = False
            if input_str in item:
                search_result.append(row)
                break
            for sub_item in item:
                if input_str in sub_item:
                    search_result.append(row)
                    flag = True
                    break
            if flag:
                break

    return search_result


def home_page(movie_area, movie_type, movie_year, movie_quarter, movie_month):  # 遍历输出
    """
    movie_country = input("movie_country:")
    movie_type = input("movie_type:")
    movie_year = input("movie_year:")
    movie_quarter = input("movie_quarter:")
    movie_month = input("movie_month:")
    """
    current_movie = select(movie_area, movie_type, movie_year, movie_quarter, movie_month)

    home_page_result = []

    sqc = 6
    current_movie.sort(key=lambda x: float(x[sqc]), reverse=True)

    for row in current_movie:
        home_page_result.append(row)

    return home_page_result


def top_movie(movie_area, movie_type, movie_year, movie_quarter, movie_month, top_num):  # 票房排名靠前的电影
    """
    movie_country = input("movie_country:")
    movie_type = input("movie_type:")
    movie_year = input("movie_year:")
    movie_quarter = input("movie_quarter:")
    movie_month = input("movie_month:")
    """
    current_movie = select(movie_area, movie_type, movie_year, movie_quarter, movie_month)
    current_movie.sort(key=lambda x: float(x[1]), reverse=True)

    top_num = int(top_num)

    top_movie_result = []

    for i in range(0, top_num):
        if i >= len(current_movie):
            break
        top_movie_result.append(current_movie[i])

    return top_movie_result


def model_actor(movie_area, movie_year, top_num, model_object):  # 劳模男女演员与导演
    """
    movie_country = input("movie_country:")
    movie_year = input("movie_year:")
    """
    current_movie = select(movie_area, "", movie_year, "", "")
    actor_movie_count = []
    actor_sex = []  # as is known to us all, actor means male and actress vice versa, who cares though
    director_movie_count = []

    top_actor = []
    top_actress = []
    movie_actor_result = []

    if not top_num:
        top_num = 0
    else:
        top_num = int(top_num)

    with open(actorPath, 'r', encoding='UTF-8') as init_actor_file:
        actor_file = csv.reader(init_actor_file, delimiter=',')
        for row in actor_file:
            if not row == []:
                actor_sex.append(row)

    for row in current_movie:
        for actor in row[7]:
            flag = False
            if not actor:
                continue
            for item in actor_movie_count:
                if actor == item[0]:
                    flag = True
                    item[1] += 1
                    item[2].append(row[3])
                    continue

            if not flag:
                actor_movie_count.append([actor, 1, [row[3]]])

        for director in row[2]:
            flag = False
            if not director:
                continue
            for item in director_movie_count:
                if director == item[0]:
                    flag = True
                    item[1] += 1
                    item[2].append(row[3])
                    continue

            if not flag:
                director_movie_count.append([director, 1, [row[3]]])

    actor_movie_count.sort(key=lambda x: float(x[1]), reverse=True)
    director_movie_count.sort(key=lambda x: float(x[1]), reverse=True)

    # for row in actor_movie_count:
    #     print(row[0])

    actor_count = 0
    actress_count = 0

    for row in actor_movie_count:
        for item in actor_sex:
            if row[0] == item[1]:
                if item[2] == "男" and actor_count < top_num:
                    # print(row[0])
                    top_actor.append(row)
                    actor_count += 1
                if item[2] == "女" and actress_count < top_num:
                    top_actress.append(row)
                    actress_count += 1
                break

        if actor_count >= top_num and actress_count >= top_num:
            break

    if model_object == "Actor":
        movie_actor_result = top_actor
    if model_object == "Actress":
        movie_actor_result = top_actress
    if model_object == "Director":
        for i in range(0, top_num):
            if i >= len(director_movie_count):
                break
            movie_actor_result.append(director_movie_count[i])
            # print(movie_actor_result)

    return movie_actor_result


def broken_line_graph(movie_area, movie_type):  # 折线图
    """
    movie_country = input("movie_country:")
    movie_type = input("movie_type:")
    """
    month_box = [[], [], [], []]

    for i in range(0, 4):
        for j in range(0, 12):
            month_box[i].append(0)
            current_movie = select(movie_area, movie_type, str(2015 + i), "", str(1 + j))

            for row in current_movie:
                month_box[i][j] += float(row[1])

    return month_box


def pie_graph(movie_area, movie_year, movie_quarter, movie_month):  # 饼状图
    """
    movie_country = input("movie_country:")
    movie_year = input("movie_year:")
    movie_quarter = input("movie_quarter:")
    movie_month = input("movie_month:")
    """
    current_movie = select(movie_area, "", movie_year, movie_quarter, movie_month)

    movie_type = ['惊悚', '冒险', '剧情', '动作', '传记', '喜剧', '动画', '家庭', '爱情', '科幻', '灾难', '音乐',
                  '奇幻', '悬疑', '黑色电影', '武侠', '战争', '古装', '历史', '运动', '恐怖', '歌舞', '犯罪', '纪录片',
                  '戏曲', '短片', '西部']

    box_type = []
    for i in range(0, len(movie_type)):
        box_type.append(0)

    for row in current_movie:
        for item in row[9]:
            for i in range(0, len(movie_type)):
                if item == movie_type[i]:
                    if row[1]:
                        box_type[i] += float(row[1])
                    break

    return box_type


def printer():  # 打印，不在这里实现
    # ok i don't know how to print or somewhat save a picture thus this func is empty
    # there should be print history as well
    return


def history_update(hst_contend, hst_type):  # 更新历史，不在这里实现
    temp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    history = [temp, hst_contend, hst_type]
    write_back_file(history)
    return


def history_display():  # 显示历史，不在这里实现
    if not os.path.exists(historyPath):
        fp = open(historyPath, "a+")
        fp.close()

    history_display_result = []

    with open(historyPath, 'r') as init_history_file:
        history_file = csv.reader(init_history_file, delimiter=',')
        for row in history_file:
            # print(row)
            history_display_result.append(row)

    return history_display_result


def history_clear():  # 清除历史，不在这里实现
    if os.path.exists(moviePath):
        os.remove(historyPath)

    fp = open(historyPath, "a+")
    fp.close()

    return


def write_back_file(history):  # 写回文件
    fp = open(historyPath, "a", newline="")
    csv_write = csv.writer(fp, dialect="excel")
    csv_write.writerow(history)
    fp.close()


if __name__ == "__main__":  # 手动测试
    open_movie_file()
    data_processing()

    while 1:
        output = []
        switch = input("选择功能：")
        if switch == "1":
            output = home_page("多米尼加", "", "2017", "", "")  # 遍历输出电影
        if switch == "2":
            output = search("复仇者联盟")  # 搜索电影
        if switch == "3":
            history_clear()  # 清除历史
        if switch == "4":
            output = model_actor("多米尼加", "", "10", "Actor")  # 劳模演员/导演
        if switch == "5":
            output = top_movie("", "", "", "", "", "10")  # 最高排名电影
        if switch == "6":
            output = broken_line_graph("-多米尼加", "")  # 折线趋势图，票房单位为“亿”
        if switch == "7":
            output = pie_graph("-", "-", "-", "-")  # 饼状图
        if switch == "8":
            output = history_display()  # 输出历史

        if not output:
            print("none")
        for op in output:
            print(op)
