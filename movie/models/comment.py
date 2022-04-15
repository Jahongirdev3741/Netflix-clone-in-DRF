from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Comment(models.Model):
  movie=models.ForeignKey('movie.Movie',on_delete=models.CASCADE)
  user=models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True, blank=True)
  comment=models.CharField(max_length=128)
  order=models.IntegerField()
  created_at=models.DateField(auto_now_add=True)
  updated_at=models.DateField(auto_now=True)

  def __str__(self) -> str:
    return self.comment
  
  class Meta:
    db_table='comments'
    verbose_name_plural = 'Comments'