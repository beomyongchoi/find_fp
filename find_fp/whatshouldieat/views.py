#-*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from .forms import WhereAreYouForm


class WhereAreYouView(FormView):
    template_name = 'whatshouldieat/whereareyou.html'
    form_class = WhereAreYouForm
    success_url = 'whatshouldieat/hereiam'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(WhereAreYouView, self).form_valid(form)


# def whereareyou(request):
#     form = WhereAreYouForm()
#     return render(request, 'whatshouldieat/whereareyou.html', {'form': form})


def hereiam(request):
    if request.method == "POST":
        form = WhereAreYouForm(request.POST)
        if form.is_valid():
            location = request.POST.get('location')
            context = {
                "location": location,
            }
            return render(request, 'whatshouldieat/hereiam.html', context)

        else:
            context = {
                "location": 'Are you on earth',
            }
            return render(request, 'whatshouldieat/hereiam.html', context)
    else:
        redirect('whatshouldieat')
# def hereiam(request):

# def results(request):
#     return render(request, 'whatshouldieat/results.html', {'hereiam': hereiam})
