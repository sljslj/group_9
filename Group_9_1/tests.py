import unittest
import manage
 
manage.analyse.open_movie_file()
manage.analyse.data_processing()


class TestDivision(unittest.TestCase):
    # 遍历输出部分测试

    def test_home_page_1(self):
        temp = manage.analyse.home_page("", "", "", "", "")  # 输出全部电影，共1085部
        number = len(temp)
        self.assertEqual(number, 1085)

    def test_home_page_2(self):
        temp = manage.analyse.home_page("-中国大陆", "", "", "", "")  # 中国大陆有728部电影
        number = len(temp)
        self.assertEqual(number, 727)

    def test_home_page_3(self):
        temp = manage.analyse.home_page("-多米尼加", "", "", "", "")  # 多米尼加只有1部电影...
        number = len(temp)
        self.assertEqual(number, 1)

    def test_home_page_4(self):
        temp = manage.analyse.home_page("-多米尼加", "-喜剧", "", "", "")  # ...而且不是喜剧...
        number = len(temp)
        self.assertEqual(number, 0)

    def test_home_page_5(self):
        temp = manage.analyse.home_page("-多米尼加", "-冒险", "-2017", "-4", "-12")  # ...是2017年的冒险电影
        number = len(temp)
        self.assertEqual(number, 1)

    def test_home_page_6(self):
        temp = manage.analyse.home_page("-中国大陆-多米尼加", "", "", "", "")  # 中国大陆和多米尼加一共有729部电影
        number = len(temp)
        self.assertEqual(number, 728)

    def test_home_page_7(self):
        temp = manage.analyse.home_page("", "", "", "-1", "-4")  # 4月不在第一季度
        number = len(temp)
        self.assertEqual(number, 0)

    def test_home_page_8(self):
        temp = manage.analyse.home_page("", "", "-2014", "", "")  # 2014年不在考虑范围...
        number = len(temp)
        self.assertEqual(number, 0)

    def test_home_page_9(self):
        temp = manage.analyse.home_page("", "", "-2015-2016-2017-2018-2019", "", "")  # ...2015/2016/2017/2018年都在
        number = len(temp)
        self.assertEqual(number, 1085)

    # 搜索部分测试

    def test_movie_search_1(self):
        temp = manage.analyse.search("terminator")  # 电影名英文搜索
        name = temp[0][3]
        self.assertEqual(name, "终结者：创世纪")

    def test_movie_search_2(self):
        temp = manage.analyse.search("终结者：创世纪")  # 电影名中文搜索
        name = temp[0][3]
        self.assertEqual(name, "终结者：创世纪")

    def test_movie_search_3(self):
        temp = manage.analyse.search("温子仁")  # 导演搜索
        name = temp[0][3]
        self.assertEqual(name, "速度与激情7")

    def test_movie_search_4(self):
        temp = manage.analyse.search("欧阳娜娜")  # 演员搜索
        number = len(temp)
        self.assertEqual(number, 5)

    def test_movie_search_5(self):
        temp = manage.analyse.search("")  # 空输入
        number = len(temp)
        self.assertEqual(number, 0)

    def test_movie_search_6(self):
        temp = manage.analyse.search("sui bian shu ru")  # 随便输入
        number = len(temp)
        self.assertEqual(number, 0)

    # 劳模部分测试
    def test_model_actor_1(self):
        temp = manage.analyse.model_actor("", "", "10", "Actor")  # 范围全部，输出前十劳模男演员，第一名任达华，参与16部电影
        name = temp[0][0]
        number = temp[0][1]
        self.assertEqual(name, "任达华")
        self.assertEqual(number, 16)

    def test_model_actor_2(self):
        temp = manage.analyse.model_actor("", "", "10", "Actress")  # 范围全部，输出前十劳模女演员，第一名郭采洁，参与12部电影
        name = temp[0][0]
        number = temp[0][1]
        self.assertEqual(name, "郭采洁")
        self.assertEqual(number, 12)

    def test_model_actor_3(self):
        temp = manage.analyse.model_actor("", "", "10", "Director")  # 范围全部，输出前十劳模导演，第一名王晶，导演了7部电影
        name = temp[0][0]
        number = temp[0][1]
        self.assertEqual(name, "王晶")
        self.assertEqual(number, 7)

    def test_model_actor_4(self):
        temp = manage.analyse.model_actor("-美国", "2018", "10", "Actor")  # 美国2018前十劳模男演员，第一名诺亚·尤佩，出演了4部电影
        name = temp[0][0]
        number = temp[0][1]
        self.assertEqual(name, "诺亚·尤佩")
        self.assertEqual(number, 4)

    def test_model_actor_5(self):
        temp = manage.analyse.model_actor("-美国-中国大陆", "2018", "10", "Actor")  # 美国2018前十劳模男演员，第一名郭政建，出演了6部电影
        name = temp[0][0]
        number = temp[0][1]
        self.assertEqual(name, "郭政建")
        self.assertEqual(number, 6)

    def test_model_actor_6(self):
        temp = manage.analyse.model_actor("-多米尼加", "-2018", "10", "Actor")  # 多米尼加2018没有男演员
        number = len(temp)
        self.assertEqual(number, 0)

    def test_model_actor_7(self):
        temp = manage.analyse.model_actor("-中国大陆", "-2018", "10", "Actor")  # 中国大陆2018有足够数量男演员，第一名是郭政建，出演了6部电影
        total_number = len(temp)
        name = temp[0][0]
        actor_number = temp[0][1]
        self.assertEqual(total_number, 10)
        self.assertEqual(name, "郭政建")
        self.assertEqual(actor_number, 6)

    def test_model_actor_8(self):
        temp = manage.analyse.model_actor("-中国大陆", "-2018", "3", "Actor")  # 中国大陆2018前3劳模男演员，第一名还是郭政建（猜猜为什么呢？），出演了6部电影
        total_number = len(temp)
        name = temp[0][0]
        actor_number = temp[0][1]
        self.assertEqual(total_number, 3)
        self.assertEqual(name, "郭政建")
        self.assertEqual(actor_number, 6)

    def test_model_actor_9(self):
        temp = manage.analyse.model_actor("-中国大陆", "-2015-2016-2017--2018", "3", "Actor")
        # 中国大陆2015/2016/2017/2018前3劳模男演员，第一名是任达华，出演了17部电影
        total_number = len(temp)
        name = temp[0][0]
        actor_number = temp[0][1]
        self.assertEqual(total_number, 3)
        self.assertEqual(name, "任达华")
        self.assertEqual(actor_number, 16)

    # 最高票房电影部分测试

    def test_top_movie_1(self):
        temp = manage.analyse.top_movie("", "", "", "", "", "10")  # 全球前10票房电影，第一名是战狼，票房56.83亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "战狼2")
        self.assertEqual(box, "56.83")

    def test_top_movie_2(self):
        temp = manage.analyse.top_movie("", "", "", "", "", "3")  # 全球前3票房电影，第一名还是战狼，票房56.83亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "战狼2")
        self.assertEqual(box, "56.83")

    def test_top_movie_3(self):
        temp = manage.analyse.top_movie("-美国", "", "", "", "", "3")  # 美国前3票房电影，第一名还是速度与激情8，票房26.70亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "速度与激情8")
        self.assertEqual(box, "26.70")

    def test_top_movie_4(self):
        temp = manage.analyse.top_movie("-美国", "", "-2016", "", "", "3")  # 美国2016前3票房电影，第一名是疯狂动物城，票房15.27亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "疯狂动物城")
        self.assertEqual(box, "15.27")

    def test_top_movie_5(self):
        temp = manage.analyse.top_movie("-美国", "-喜剧", "-2016", "2", "4", "3")  # 美国2016年4月前3票房喜剧电影，第一名是废柴特工，票房0.19865亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "废柴特工")
        self.assertEqual(box, "0.19865")

    def test_top_movie_6(self):
        temp = manage.analyse.top_movie("-奥地利", "-喜剧", "-2016", "2", "4", "3")  # 奥地利2016年4月没有喜剧电影
        number = len(temp)
        self.assertEqual(number, 0)

    def test_top_movie_7(self):
        temp = manage.analyse.top_movie("-美国", "-喜剧-剧情-战争-科幻", "-2016", "-2", "-4", "3")
        # 美国2016年4月前3票房喜剧、剧情、战争、科幻电影，第一名是奇幻森林，票房9.76亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "奇幻森林")
        self.assertEqual(box, "9.76")

    def test_top_movie_8(self):
        temp = manage.analyse.top_movie("-美国-英国", "-喜剧-剧情-战争-科幻", "-2016-2017", "-2", "-4-5-6", "3")
        # 美国、英国2016/2017年4/5/6月前3票房喜剧、剧情、战争、科幻电影，第一名是变形金刚5：最后的骑士，票房15.51亿
        name = temp[0][3]
        box = temp[0][1]
        self.assertEqual(name, "变形金刚5：最后的骑士")
        self.assertEqual(box, "15.51")

    # 折线趋势图部分测试

    def test_broken_line_graph_1(self):
        temp = manage.analyse.broken_line_graph("", "")  # 全部电影折线图，2015年1月总票房26.722959999999997亿
        box = temp[0][0]
        self.assertEqual(box, 26.722959999999997)

    def test_broken_line_graph_2(self):
        temp = manage.analyse.broken_line_graph("-多米尼加", "")  # 多米尼加只有2017年12月有票房，为0.38718亿...
        box = temp[2][11]
        self.assertEqual(box, 0.38718)
        box = temp[2][10]
        self.assertEqual(box, 0)  # ...11月为0

    def test_broken_line_graph_3(self):
        temp = manage.analyse.broken_line_graph("", "-喜剧")  # 全部喜剧电影折线图，2015年1月喜剧电影总票房15.302230000000002亿
        box = temp[0][0]
        self.assertEqual(box, 15.302230000000002)

    def test_broken_line_graph_4(self):
        temp = manage.analyse.broken_line_graph("", "-喜剧-剧情-科幻-恐怖")
        # 全部喜剧、剧情、科幻、恐怖电影折线图，2015年1月喜剧电影总票房16.48529亿
        box = temp[0][0]
        self.assertEqual(box, 16.48529)

    def test_broken_line_graph_5(self):
        temp = manage.analyse.broken_line_graph("-中国大陆-美国-英国", "-喜剧-剧情-科幻-恐怖")
        # 中国大陆、美国、英国全部喜剧、剧情、科幻、恐怖电影折线图，2015年1月总票房16.48514亿
        box = temp[0][0]
        self.assertEqual(box, 16.48514)

    def test_broken_line_graph_6(self):
        temp = manage.analyse.broken_line_graph("-中国大陆", "")
        # 中国大陆电影折线图，2017年7月总票房78.88594000000002亿（因为战狼2）
        box = temp[2][6]
        self.assertEqual(box, 78.88594000000002)

    # 饼状图部分测试

    def test_pie_graph_1(self):
        temp = manage.analyse.pie_graph("", "", "", "")  # 全部电影的种类票房
        box = temp[0]
        self.assertEqual(box, 207.34899000000001)  # 惊悚电影，总票房207.34899000000001亿
        box = temp[1]
        self.assertEqual(box, 680.9510499999998)  # 冒险电影，总票房680.9510499999998亿
        box = temp[2]
        self.assertEqual(box, 494.6814300000001)  # 剧情电影，总票房494.6814300000001亿

    def test_pie_graph_2(self):
        temp = manage.analyse.pie_graph("-中国大陆", "", "", "")  # 中国大陆电影的种类票房
        box = temp[0]
        self.assertEqual(box, 46.78766999999999)  # 惊悚电影，总票房46.78766999999999亿
        box = temp[1]
        self.assertEqual(box, 206.20998000000012)  # 冒险电影，总票房206.20998000000012亿
        box = temp[2]
        self.assertEqual(box, 390.53815999999995)  # 剧情电影，总票房390.53815999999995亿

    def test_pie_graph_3(self):
        temp = manage.analyse.pie_graph("-多米尼加", "", "", "")  # 多米尼加电影的种类票房
        box = temp[0]
        self.assertEqual(box, 0.38718)  # 惊悚电影，总票房0
        box = temp[1]
        self.assertEqual(box, 0.38718)  # 冒险电影，总票房0.38718
        box = temp[2]
        self.assertEqual(box, 0)  # 剧情电影，总票房0

    def test_pie_graph_4(self):
        temp = manage.analyse.pie_graph("-中国大陆", "-2015", "-1", "-2")  # 中国大陆2015年2月电影的种类票房
        box = temp[0]
        self.assertEqual(box, 0.02374)  # 惊悚电影，总票房0.02374亿
        box = temp[1]
        self.assertEqual(box, 6.9637400000000005)  # 冒险电影，总票房6.9637400000000005亿
        box = temp[2]
        self.assertEqual(box, 11.96667)  # 剧情电影，总票房11.96667亿

    def test_pie_graph_5(self):
        temp = manage.analyse.pie_graph("-中国大陆-美国", "-2015-2016", "-1-2", "-2-5")  # 中国大陆、美国2015、2016年2月、5月电影的种类票房
        box = temp[0]
        self.assertEqual(box, 1.5224400000000002)  # 惊悚电影，总票房1.5224400000000002亿
        box = temp[1]
        self.assertEqual(box, 43.26479)  # 冒险电影，总票房43.26479亿
        box = temp[2]
        self.assertEqual(box, 16.14552)  # 剧情电影，总票房16.14552亿


if __name__ == '__main__':
    unittest.main()
