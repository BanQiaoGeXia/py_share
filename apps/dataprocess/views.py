# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View


class DataProcess(View):

    def get(self, request, *args, **kwargs):
        # result_data = {}
        result_data = {
            "result_data": {
                "user1": {
                    "score": 10,
                    "max_press_key": "down"
                },
                "user2": {
                    "score": 30,
                    "max_press_key": "left"
                },
                "user3": {
                    "score": 70,
                    "max_press_key": "right"
                },
            }
        }
        return render(request, "dataprocess.html", result_data)
