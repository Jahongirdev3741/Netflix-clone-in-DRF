from django.forms import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import Movie,Actor,Comment
from datetime import date

class MovieSerializer(ModelSerializer):
  class Meta:
    model=Movie
    fields='__all__'
    

class ActorSerializer(ModelSerializer):

  def validate_birthdate(self, value):
    head_of_date=date(1950,1,1)
    print(value)
    if value<head_of_date:
      raise ValidationError("Birthdate must not be less then head of date {01,01,1950}")
    else:
      return value
      
  class Meta:
    model=Actor
    fields='__all__'

class CommentSerializer(ModelSerializer):
  class Meta:
    model=Comment
    fields='__all__'
