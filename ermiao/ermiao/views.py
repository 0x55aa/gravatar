# coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    """
    用户注册
    """
    userprofile = ''
    if request.user.is_authenticated():
        userprofile = request.user.get_profile()
    return render_to_response('home.html', {'userprofile': userprofile, },
                    context_instance=RequestContext(request))
