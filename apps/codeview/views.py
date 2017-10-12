# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View


class CodeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'view_code.html')
