from django.db import models
from .actor import Actor

class Movie(models.Model):
  GENRES = (
    ('adventure', 'Adventure'),
    ('comedy', 'Comedy'),
    ('crime and mystery', 'Crime and mystery'),
    ('fantasy', 'Fantasy'),
    ('historical', 'Historical'),
    ('horror', 'Horror'),
    ('romance', 'Romance'),
    ('satire', 'Satire'),
    ('speculative', 'Speculative'),
    ('thriller', 'Thriller'),
    ('western', 'Western'),
    ('erotic', 'Erotic'),
  )
  name=models.CharField(max_length=128)
  year=models.DateField()
  imdb=models.IntegerField()
  ganre=models.CharField(max_length=20,choices=GENRES)
  actors=models.ManyToManyField(Actor)
  watch=models.IntegerField(default=0)

  def __str__(self) -> str:
    return self.name