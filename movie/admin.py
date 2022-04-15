from django.contrib import admin
from .models import Movie,Actor,Comment

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  search_fields=('name',)
  list_display=('name','year',)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#   search_fields=['first_name','last_name']
#   list_display=['first_name','role']

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
  search_fields=('name',)
  list_display=['name','birthdate','gender']

admin.site.register(Comment)
