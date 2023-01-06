from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from . import settings


class RedirectView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(settings.FRONT_URL)
