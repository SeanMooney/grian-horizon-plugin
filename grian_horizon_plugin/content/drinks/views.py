from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'metrics/index.html'