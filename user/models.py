from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL

# 縣市
class City(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


# 接案身分
class Respondent(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


# Create your models here.
class Profile(AbstractUser):
    # 點數
    point = models.IntegerField(default=0)
    # 是否通過認證
    certification = models.BooleanField(default=False)
    # 居住縣市
    city = models.ForeignKey(City,on_delete=SET_NULL,null=True)
    # 身分
    respondent = models.ForeignKey(Respondent,on_delete=SET_NULL,null=True)

    
    def __str__(self):
        return self.username


    # Create your models here.
