from django.contrib import admin

# Register your models here.
from .models import (
    LineUser, Statement, Reply, Communication, KeyWord, Statement_Flow, Reply_Set,
)

admin.site.register(LineUser)
admin.site.register(Statement)
admin.site.register(KeyWord)
