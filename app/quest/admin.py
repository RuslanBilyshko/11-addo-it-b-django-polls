from django.contrib import admin

# Register your models here.
from .models import Quest, Choise_type, Choise, Question, Choise_result

admin.site.register(Quest)
# admin.site.register(Choise_type)
admin.site.register(Choise)
admin.site.register(Question)
admin.site.register(Choise_result)