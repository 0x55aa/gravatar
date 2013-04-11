# coding:utf-8
#头像获取
import urllib
import hashlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
#导入用户数据模型
from django.contrib.auth.models import User

from accounts.models import UserProfile
from accounts.forms import RegistrationForm, LoginForm
from django.conf import settings


def register(request):
    """
    用户注册
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password2'],
                email=form.cleaned_data['email'],)
            user.save()
            #gravatar头像获取
            #不存在时默认返回的头像，定义为404，如果返回404，使用ermiao默认头像路径
            default = 404
            #头像大小
            size = 80
            #gravatar头像地址
            gravatar_url = "http://www.gravatar.com/avatar/" + \
                           hashlib.md5(user.email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
            resp = urllib.urlopen(gravatar_url)
            if resp.getcode() == 404:
                #默认头像路径
                avatar = '/img/avatar.png'
            else:
                #头像保存路径
                avatar = '/uploads/avatar/' + \
                    hashlib.md5(user.email.lower()).hexdigest() + '.png'
                full_avatar = settings.STATIC_ROOT + avatar
                f = open(full_avatar, "wb")
                f.write(resp.read())
                f.close
            userprofile = UserProfile(
                user=user,
                avatar=avatar,)
            userprofile.save()

            #注册成功
            return render_to_response('warn.html',
                                      {'warning': u'注册成功！', },
                                      context_instance=RequestContext(request)
                                      )
    else:
        form = RegistrationForm()

    return render_to_response('accounts/register.html',
                              {'form': form, },
                              context_instance=RequestContext(request)
                              )


def login(request):
    """
    登录
    """
    #登录成功，返回页面
    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = '/'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #数据合法
        if form.is_valid():
            u = User.objects.get(email=request.POST['email'])
            user = auth.authenticate(username=u.username, password=request.POST['password'])
            auth.login(request, user)

            #检查是否记住登录
            if 'remember' not in request.POST.keys():
                request.session.set_expiry(0)

            if request.POST['next']:
                next = request.POST['next']

            return HttpResponseRedirect(next,)
    else:
        form = LoginForm()
        #用于跳转，返回登录前页面
        if 'HTTP_REFERER' in request.META:
            next = request.META['HTTP_REFERER']

    return render_to_response('accounts/login.html',
                              {'form': form, 'next': next, },
                              context_instance=RequestContext(request))


@login_required
def logout(request):
    """
    退出
    """
    #这里可以记录用户退出

    auth.logout(request)
    return HttpResponseRedirect('/',)
