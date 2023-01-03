from django.shortcuts import render
from django.core.validators import validate_email
from django.views.generic import View
from django.http import JsonResponse


class UserSignUpView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse()
