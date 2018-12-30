from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码", null=True)
    email = models.EmailField(max_length=50, verbose_name=u"邮箱", null=True)

    send_type = models.CharField(choices=(("register", "注册"), ("forgrt", u"找回密码")), max_length=15, null=True)
    send_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=200)
    movie_url = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.movie_name


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    data_url = models.CharField(max_length=500000, default='')
    image_name = models.CharField(max_length=50, default='图片')

    def __str__(self):
        return self.image_name


class MovieDetail(models.Model):
    make_in = models.CharField(max_length=200)
    movie_boxOffice = models.CharField(max_length=200)
    movie_directors = models.CharField(max_length=200)
    movie_name_chi = models.CharField(max_length=200)
    movie_name_eng = models.CharField(max_length=200)
    movie_releaseDate = models.CharField(max_length=200)
    movie_score = models.CharField(max_length=20)
    movie_stars_all = models.CharField(max_length=200)
    movie_timeLength = models.CharField(max_length=200)
    movie_type = models.CharField(max_length=200)
    movie_url_index = models.CharField(max_length=200)


# 用作搜索输入的转存
class SearchInput(models.Model):
    search_input = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.search_input


# 用作搜索结果的转存，关联到每一个搜索输入
class SearchResult(models.Model):
    search_input = models.ForeignKey(SearchInput, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=200)
    movie_score = models.CharField(max_length=20)
    movie_star_all = models.CharField(max_length=200, default='No one')
    movie_url = models.CharField(max_length=50, default='')
    favorite_msg = models.CharField(max_length=10, default="收藏")

    def __str__(self):
        return self.movie_name
