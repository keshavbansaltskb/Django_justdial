from .models import Business
from django.db.models.functions import Random

def website_content(request):
    context = {
        # "categories":categories.objects.all()[:4]
        "busssinessfooter":Business.objects.order_by(Random())[:5]
    }
    return context