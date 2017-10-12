# -*- coding: utf-8 -*-

from django.http.response import JsonResponse
from rest_framework.views import APIView
from py_share.settings import USER_LOG_DIRS


class DataReceive(APIView):

    def post(self, request, *args, **kwargs):
        data = {
            "status": "ok",
            "message": "日志上传成功",
        }
        log_stream = request.data
        print(log_stream)
        # TODO 这里接受日志上传 当开启异步任务初步处理日志
        username = log_stream.get("username")
        f = open(USER_LOG_DIRS + "/" + username + ".log", "w+")
        f.writelines(log_stream.get("log_list"))
        f.close()
        return JsonResponse(data)
