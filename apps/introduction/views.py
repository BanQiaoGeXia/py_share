# -*- coding: utf-8 -*-

# -*- coding:utf-8 -*-

"""
    Created by m.k
    Date:  2017/10/8
    Change Activity:

"""
from django.shortcuts import render
from django.views.generic import View


class Introduction(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'introduction.html')
