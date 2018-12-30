from django.urls import path
from . import views as cuckoo_views
app_name = 'cuckoo'
urlpatterns = [
    path('index/', cuckoo_views.index, name='index'),
    path('index-dark/', cuckoo_views.index_dark, name='index-dark'),
    path('login/<int:bg_color>', cuckoo_views.login, name='login'),
    path('register/<int:bg_color>', cuckoo_views.register, name='register'),
    path('forget/<int:bg_color>', cuckoo_views.forget, name='forget'),
    path('search/<int:bg_color>/<str:search_input>', cuckoo_views.search, name='search'),
    path('table/<int:bg_color>', cuckoo_views.movie_table, name='table'),
    path('actors/<int:bg_color>', cuckoo_views.model_actors, name='actors'),
    path('share/<int:bg_color>', cuckoo_views.box_office_share, name='share'),
    path('trend/<int:bg_color>', cuckoo_views.movie_trend, name='trend'),
    path('movie-top/<int:bg_color>', cuckoo_views.movie_top, name='movie-top'),
    path('actor-top/<int:bg_color>', cuckoo_views.actor_top, name='actor-top'),
    path('logout/', cuckoo_views.log_out, name='logout'),
    path('logout_dark/', cuckoo_views.log_out_dark, name='logout_dark'),

    path('login/deal-login/', cuckoo_views.deal_login),
    path('register/deal-login/', cuckoo_views.deal_register),
    path('register/deal-email/', cuckoo_views.deal_email),
    path('forget/deal-email/', cuckoo_views.deal_email),
    path('forget/deal-password/', cuckoo_views.deal_password),

    path('trend/deal-trend/', cuckoo_views.deal_trend),
    path('share/deal-box-share/', cuckoo_views.deal_box_share),
    path('deal-favorite/', cuckoo_views.deal_favorite),

    path('actors/deal-actor-top/', cuckoo_views.deal_actor_top),
    path('table/deal-movie-top/', cuckoo_views.deal_movie_top),

    path('index/deal-collect/', cuckoo_views.deal_favorite),
    path('index-dark/deal-collect/', cuckoo_views.deal_favorite),

    path('movie-top/deal-img', cuckoo_views.deal_img),
    path('actor-top/deal-img', cuckoo_views.deal_img),
    path('trend/deal-img', cuckoo_views.deal_img),
    path('share/deal-img', cuckoo_views.deal_img),
    path('share/delimg', cuckoo_views.deal_delimg),

    path('index-dark/deal-login/', cuckoo_views.deal_login),
    path('index/deal-login/', cuckoo_views.deal_login),

    path('share/delimg',cuckoo_views.deal_delimg),
    path('actors/delimg',cuckoo_views.deal_delimg),
    path('actor-top/delimg',cuckoo_views.deal_delimg),
    path('table/delimg',cuckoo_views.deal_delimg),
    path('trend/delimg',cuckoo_views.deal_delimg),
    path('movie-top/delimg',cuckoo_views.deal_delimg),

]
