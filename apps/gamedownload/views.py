# -*- coding:utf-8 -*-

"""
    Created by m.k
    Date:  2017/10/8
    Change Activity:
    
"""
from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import View


class GameDownload(View):

    def get(self, request):
        # do something...
        def file_iterator(fn, chunk_size=512):
            while True:
                c = fn.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        fn = open('static/download/snake.py', 'r')
        response = StreamingHttpResponse(file_iterator(fn))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="snake.py"'
        return response
