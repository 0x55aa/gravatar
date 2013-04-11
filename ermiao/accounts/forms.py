#-*- coding:utf-8 -*-

from django import forms
#导入用户数据模型
from django.contrib.auth.models import User
from django.contrib import auth
#导入正则表达式模块
import re
#
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    """
    用户注册类，从Form类继承
    """

    #用户名文本框
    username = forms.CharField(label='用户名',min_length=3,max_length=7)
    #email
    email = forms.EmailField(label='电子邮件')
    #passwd
    password1 = forms.CharField(label='密码',min_length=6,max_length=20,widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',min_length=6,max_length=20,widget=forms.PasswordInput())


    #验证输入用户名的合法性，正则表达式 去除特殊字符，可以是数字字母文字
    def clean_username(self):
        #去除用户输入的用户名
        username = self.cleaned_data['username']
        #正则表达式验证
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字、下划线和汉字。')
        name_list = ['root', u'官方', 'admin']
        for name in name_list:
            if name in username:
                raise forms.ValidationError('该用户名已存在，请重新填写！')
        try:
            #判断用户名是否被注册
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('该用户名已存在，请重新填写！')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('该电子邮件已被注册，请重新填写！')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('两次输入密码不同，请重新输入')


class LoginForm(forms.Form):
    """
    用户login类，从Form类继承
    """
    #email
    email = forms.EmailField(label='电子邮件')
    #passwd
    password = forms.CharField(label='密码',min_length=6,max_length=20,widget=forms.PasswordInput())
    #是否记住登录
    remember = forms.BooleanField(label='下次自动登录',required=False)

    def clean_email(self):

        email = self.cleaned_data['email']

        try:
            #判断email是否被注册
            User.objects.get(email=self.cleaned_data['email'])
        except ObjectDoesNotExist:
            raise forms.ValidationError('该email不存在或密码错误，请重新填写！')

        return email
    
    def clean_password(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            u = User.objects.get(email=email)
            user = auth.authenticate(username=u.username, password=password)
            if user is not None and user.is_active:
                return password
        
            raise forms.ValidationError('该email不存在或密码错误，请重新填写！')
