from django.db import models

class Actor(models.Model):
  GENDER=(
    ('male',"Male"),
    ('female','Female'),
    ('other','Other')
  )

  name=models.CharField(max_length=128,unique=True)
  birthdate=models.DateField()
  gender=models.CharField(max_length=8,choices=GENDER)

  def __str__(self) -> str:
    return self.name