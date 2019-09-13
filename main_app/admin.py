from django.contrib import admin
from .models import Fantasticbeast, Feeding, Toy, Photo

# Register your models here.
admin.site.register(Fantasticbeast)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)