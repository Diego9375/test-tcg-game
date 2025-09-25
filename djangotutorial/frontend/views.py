from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404

from backend.models import Card, Booster, Collection


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        cards = Card.objects.all()
        boosters = Booster.objects.all()
        collections = Collection.objects.all()
        context.update({
            'cards': cards,
            'boosters': boosters,
            'collections': collections,
        })
        return context


# views.py


def open_booster_view(request):
    booster = get_object_or_404(Booster)
    booster.open_booster()
    return redirect('index')



    # Redirige a la página principal o donde tengas tu lista
