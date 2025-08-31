from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Cache response for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    return JsonResponse({"data": list(properties)})

from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver([post_save, post_delete], sender=Property)
def clear_property_cache(sender, **kwargs):
    cache.delete("all_properties")
