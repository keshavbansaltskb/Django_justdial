from .models import Category
from django.db.models.functions import Random

def website_content(request):
    context = {
        # "categories":categories.objects.all()[:4]
        "categoriesfooter":Category.objects.order_by(Random())[:5]
    }
    return context