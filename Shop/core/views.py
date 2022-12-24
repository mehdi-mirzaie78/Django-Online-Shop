from django.shortcuts import redirect
from django.views import View
from django.utils.translation import activate


class ChangeLanguageView(View):
    def get(self, request):
        activate(request.GET.get('lang'))
        return redirect(request.GET.get('next'))
