from django.shortcuts import render, get_object_or_404
from matplotlib import colors
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from . import models
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from . import analyse
from . import sendmail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
idf_code = ''


@csrf_exempt
def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('cuckoo:index'))

@csrf_exempt
def log_out_dark(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('cuckoo:index-dark'))


@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        in_href = '#'
        log_name = request.user.username
        out_href = '../logout'
        in_value = 'none'
        out_value = ''
    else:
        in_href = '../login/0'
        log_name = 'Log In'
        out_href = '#'
        in_value = ''
        out_value = 'none'
    context = {'in': in_href, 'out': out_href, 'name': log_name, 'in_dis': in_value, 'out_dis': out_value}
    response = render(request, 'index.html', context)

    if request.method == 'POST':
        response = deal_search(request)
    return response


def index_dark(request):
    if request.user.is_authenticated:
        in_href = '#'
        log_name = request.user.username
        out_href = '../logout_dark'
        in_value = 'none'
        out_value = ''
    else:
        in_href = '../login/1'
        log_name = 'Log In'
        out_href = '#'
        in_value = ''
        out_value = 'none'
    context = {'in': in_href, 'out': out_href, 'name': log_name, 'in_dis': in_value, 'out_dis': out_value}
    response = render(request, 'index-dark.html', context)

    if request.method == 'POST':
        response = deal_search_dark(request)
    return response

@csrf_exempt
def login(request, bg_color):
    if bg_color == 1:
        bg_class = 'body2'
        box_color_id = 'rgba(164,172,167,0.6)'
        container_color_id = 'rgba(47,47,53,0.4)'
        hello_color_id = '#ccccd6'
        register_color_id = '#b2bbbe'
        index_url = 'index-dark'
        time_id = '1'
    else:
        bg_class = 'body1'
        box_color_id = colors.to_rgba('#cccccc', 0.7)
        container_color_id = colors.to_rgba('#e9e9e9', 0.95)
        hello_color_id = '#497568'
        register_color_id = '#648e93'
        index_url = 'index'
        time_id = '0'
    context = {"box_color": box_color_id, "container_color": container_color_id,
               "hello_color": hello_color_id, "register_color": register_color_id,
               "bg_class": bg_class, "index_url": index_url, 'time_id': time_id}

    # if request.is_ajax():
    #     response = deal_login(request)
    #     return response
    # else:
    return render(request, 'login.html', context)

@csrf_exempt
def register(request, bg_color):
    if bg_color == 1:
        bg_class = 'body2'
        box_color_id = 'rgba(164,172,167,0.6)'
        container_color_id = 'rgba(47,47,53,0.4)'
        hello_color_id = '#ccccd6'
        register_color_id = '#b2bbbe'
        index_url = 'index-dark'
        time_id = '1'
    else:
        bg_class = 'body1'
        box_color_id = colors.to_rgba('#cccccc', 0.7)
        container_color_id = colors.to_rgba('#e9e9e9', 0.95)
        hello_color_id = '#497568'
        register_color_id = '#648e93'
        index_url = 'index'
        time_id = '0'
    context = {'box_color': box_color_id, 'container_color': container_color_id,
               'hello_color': hello_color_id, 'register_color': register_color_id,
               'bg_class': bg_class, 'index_url': index_url, 'time_id': time_id}

    # if request.is_ajax():
    #     response = deal_register(request)
    #     return response

    return render(request, 'register.html', context)


def forget(request, bg_color):
    if bg_color == 1:
        bg_class = 'body2'
        box_color_id = 'rgba(164,172,167,0.6)'
        container_color_id = 'rgba(47,47,53,0.4)'
        hello_color_id = '#ccccd6'
        register_color_id = '#b2bbbe'
        index_url = 'index-dark'
        time_id = '1'
    else:
        bg_class = 'body1'
        box_color_id = colors.to_rgba('#cccccc', 0.7)
        container_color_id = colors.to_rgba('#e9e9e9', 0.95)
        hello_color_id = '#497568'
        register_color_id = '#648e93'
        index_url = 'index'
        time_id = '0'
    context = {'box_color': box_color_id, 'container_color': container_color_id,
               'hello_color': hello_color_id, 'register_color': register_color_id,
               'bg_class': bg_class, 'index_url': index_url, 'time_id': time_id}

    return render(request, 'forget.html', context)


# 从数据库里调数据返回给前端
@csrf_exempt
def search(request, bg_color, search_input):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    the_user = request.user
    user_object = User.objects.get(username=the_user.username)
    the_input = user_object.searchinput_set.get(search_input=search_input)
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href,
               'the_input': the_input, 'in': in_href, 'out': out_href, 'name': log_name,
               'in_dis': in_value, 'out_dis': out_value}
    if the_user.is_authenticated:
        user = the_user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'search-detail.html', context)
    else:
        response = render(request, 'search-detail.html', context)
    if request.is_ajax():
        response = deal_favorite(request)
        return response
    return response


def movie_table(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name,  'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'table.html', context)
    else:
        response = render(request, 'table.html', context)
    return response


def model_actors(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name,  'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'actors.html', context)
    else:
        response = render(request, 'actors.html', context)
    return response


def box_office_share(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name,  'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'share.html', context)
    else:
        response = render(request, 'share.html', context)
    return response


def movie_trend(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name, 'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'trend.html', context)
    else:
        response = render(request, 'trend.html', context)
    return response


def movie_top(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name,  'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'movie-top.html', context)
    else:
        response = render(request, 'movie-top.html', context)
    return response


def actor_top(request, bg_color):
    if bg_color == 1:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout_dark'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/1'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/dark.png'
        css_name = '/static/css/dark-color-table.css'
        home_href = '../index-dark'
    else:
        if request.user.is_authenticated:
            in_href = '#'
            log_name = request.user.username
            user_name = request.user.username
            out_href = '../logout'
            in_value = 'none'
            out_value = ''
        else:
            in_href = '../login/0'
            log_name = 'Log In'
            user_name = ''
            out_href = '#'
            in_value = ''
            out_value = 'none'
        logo_name = '/static/img/logo/white.png'
        css_name = ''
        home_href = '../index'
    context = {'bg': bg_color, 'logo': logo_name, 'css': css_name, 'home': home_href, 'in': in_href,
               'out': out_href, 'name': log_name,  'in_dis': in_value, 'out_dis': out_value, 'user': user_name}
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
        print(user_name)
        # info = user_name.searchinput_set.all
        the_user = get_object_or_404(User, username=user)
        context['the_user'] = the_user
        print(the_user.history_set.all())
        response = render(request, 'actor-top.html', context)
    else:
        response = render(request, 'actor-top.html', context)
    return response

# ————————————————————————————————————————————————————————————————————————————————————————————————————

@csrf_exempt
def deal_search(request):
    search_input = request.POST.get('search')  # 拿到了搜索信息输入
    # print(search_input)
    outcome = analyse.search(search_input)
    print(outcome)
    # print(outcome)
    msg = '收藏'
    # user = ''
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
    else:
        return login(request, 0)

    the_search = user_name.searchinput_set.filter(search_input=search_input)
    if the_search:
        the_search.delete()
    info = user_name.searchinput_set.create(search_input=search_input)
    # print('b')
    info.save()
    if outcome:
        for film in outcome:
            # print(3)
            if user_name.favorite_set.filter(user=user_name, movie_name=film[3]):
                msg = '已收藏'
            else:
                msg = '收藏'

            movie_url = 'https://piaofang.maoyan.com/movie/' + film[10]
            user_name.searchinput_set.filter(search_input=info)[0].\
                searchresult_set.create(movie_name=film[3], movie_score=film[6], movie_url=movie_url,
                                        movie_star_all=' / '.join(film[7]), favorite_msg=msg)
    a = search(request, 0, search_input)
    return a

@csrf_exempt
def deal_search_dark(request):
    search_input = request.POST.get('search')  # 拿到了搜索信息输入
    # print(search_input)
    outcome = analyse.search(search_input)
    # print(outcome)
    msg = '收藏'
    # user = ''
    if request.user.is_authenticated:
        user = request.user.username
        user_name = User.objects.get(username=user)
    else:
        return login(request, 1)

    the_search = user_name.searchinput_set.filter(search_input=search_input)
    if the_search:
        the_search.delete()
    info = user_name.searchinput_set.create(search_input=search_input)
    # print('b')
    info.save()
    if outcome:
        for film in outcome:
            # print(3)
            if user_name.favorite_set.filter(user=user_name, movie_name=film[3]):
                msg = '已收藏'
            else:
                msg = '收藏'
            user_name.searchinput_set.filter(search_input=info)[0].\
                searchresult_set.create(movie_name=film[3], movie_score=film[6],
                                        movie_star_all=' / '.join(film[7]), favorite_msg=msg)
    a = search(request, 1, search_input)
    return a

@csrf_exempt
def deal_register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    input_idf = request.POST.get('idf')
    global idf_code

    # print(input_idf)
    if input_idf != idf_code:
        return JsonResponse({"message": "Wrong verification code.", 's': False})

    result = User.objects.filter(username=username)
    if result:
        return JsonResponse({"message": "User name is already exist.", 's': False})

    try:
        User.objects.create_user(username=username, email=email, password=password)
        # user = auth.authenticate(username=username, password=password)
        # auth.login(request, user)
        return JsonResponse({'message': "Successful registration!", 's': True})
    except ValidationError:
        return JsonResponse({'status': 10024, 'message': "Create data wrong.", 's': False})


def deal_email(request):
    email = request.GET.get('email')
    print(email)
    global idf_code
    idf_code = sendmail.send_register_email(email, "register")
    print(idf_code)
    return JsonResponse({'message': 'An attempt has been made to send identifying code to your mailbox.'})


@csrf_exempt
def deal_password(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    input_idf = request.POST.get('idf')
    global idf_code

    if User.objects.filter(username=username):
        result = User.objects.get(username=username)
        if email == result.email:
            if input_idf == '12345':
                result.set_password(password)
                result.save()
                print(password)
                print(result.password)
                return JsonResponse({"message": "Successful modification.", "s": True})
            else:
                return JsonResponse({"message": "Wrong verification code.", "s": False})
        else:
            return JsonResponse({"message": "User name and email address do not match.", "s": False})
    else:
        return JsonResponse({"message": "User name does not exist.", "s": False})

@csrf_exempt
def deal_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        request.session['user'] = username
        return JsonResponse({"message": "Login successfully. Welcome to Cuckoo's world!", "s": True})
    else:
        return JsonResponse({"message": "User name does not exist or password error.", "s": False})


@csrf_exempt
def deal_favorite(request):
    print("ajax chenggong")
    username = request.user
    if username:
        login_message = 'yes'
        user = User.objects.get(username=username)

        movie_name = request.POST['moviename']
        movie_url = request.POST['url']
        print(movie_name)
        #print(user.favorite_set.all())
        # 从收藏夹中搜索
        the_movie = user.favorite_set.filter(movie_name=movie_name)
        if the_movie:  # 如果已经收藏了，就取消收藏
            print(the_movie)
            the_movie.delete()
            message = '取消收藏成功'
        else:
            the_new_movie = user.favorite_set.create(movie_name=movie_name,movie_url=movie_url)
            the_new_movie.save()
            message = '收藏成功'
    else:
        login_message = '您尚未登录'
        message = '收藏失败'
    return JsonResponse({'message': message, 'login_message': login_message})


def deal_trend(request):
    movieaddr = request.GET['movieaddr']
    movietype = request.GET['movietype']

    trend_result = analyse.broken_line_graph(movieaddr, movietype)
    print(trend_result)
    five = trend_result[0]
    six = trend_result[1]
    seven = trend_result[2]
    eight = trend_result[3]

    return JsonResponse({'five': five, 'six': six, 'seven': seven, 'eight': eight})


def deal_box_share(request):
    print('deal_box_share')
    year = request.GET['year']
    season = request.GET['season']
    month = request.GET['month']
    movieaddr = request.GET['movieaddr']

    box_share_result = analyse.pie_graph(movieaddr, year, season, month)
    print(box_share_result)
    return JsonResponse({'box': box_share_result})


def deal_actor_top(request):
    topnum = request.GET['topnum']
    toptype = request.GET['toptype']
    year = request.GET['year']
    area = request.GET['area']
    top_result = analyse.model_actor(area, year, topnum, toptype)
    for result_index in top_result:
        result_index[2] = '/'.join(result_index[2])

    print(top_result)
    label = []
    num = []
    for movie in top_result:
        label.append(movie[0])
        num.append(movie[1])
    num.append(0)
    return JsonResponse({"item_set": top_result, "label": label, "num": num})


def deal_movie_top(request):
    year = request.GET['year']
    month = request.GET['month']
    area = request.GET['area']
    movietop = request.GET['movietop']
    movietype = request.GET['movietype']
    season = request.GET['season']

    print(year+season+month+area+movietype+movietop)
    top_movie_result = analyse.top_movie(area, movietype, year, season, month, movietop)
    # use '/' as split
    # for index_result in top_movie_result:
    #     index_result[0] = '/'.join(index_result[0])
    #     index_result[2] = '/'.join(index_result[2])
    #     index_result[5] = '/'.join(index_result[5])
    #     index_result[7] = '/'.join(index_result[7])
    #     index_result[9] = '/'.join(index_result[9])
    print(top_movie_result)
    label = []
    box = []
    for movie in top_movie_result:
        label.append(movie[3])
        box.append(movie[1])
    box.append(0)
    return JsonResponse({"item_set": top_movie_result, 'label': label, 'box': box})



@csrf_exempt
def deal_img(request):
    if request.user.is_authenticated:
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        imgurl = request.POST['imgurl']
        imgname = request.POST['name']
        the_new_img = user.history_set.create(image_name=imgname, data_url=imgurl)
        the_new_img.save()
        return JsonResponse({'message': '保存成功', 'name': imgname, 'imgurl': imgurl})
    else:
        return login(request, 0)

@csrf_exempt
def deal_delimg(request):
    if request.user.is_authenticated:
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        imgname = request.POST['logname']
        the_img = user.history_set.filter(image_name=imgname)
        the_img[0].delete()
        return JsonResponse({'message': '删除成功', 'name':imgname})
    else:
        return login(request, 0)

