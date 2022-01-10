from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from user.models import Profile,Respondent

# 分類
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

# 外包金額
class Amount(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

# 配合模式
class Mode(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

# 目前狀態
class State(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

# 工作週期
class Period(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Case(models.Model):
    owner = models.ForeignKey(Profile,on_delete=CASCADE)
     # 標題
    title = models.CharField(max_length=200)
    # 說明
    description = models.TextField(null=True, blank=True)
    # 聯絡方式
    contact = models.CharField(max_length=100)
    # 專案分類
    category = models.ForeignKey(Category, null=True,
                                       on_delete=SET_NULL)
    # 接案金額
    amount = models.ForeignKey(
        Amount, null=True, on_delete=SET_NULL)
    # 工作週期
    period = models.ForeignKey(
        Period, null=True, on_delete=SET_NULL)
    # 需要技能
    skill = models.TextField(null=True, blank=True)
    # 接案對象
    respondent = models.ManyToManyField(Respondent)  
    # 接案狀態
    state = models.ForeignKey(
        State, null=True, on_delete=SET_NULL)
    # 接案方式
    mode = models.ManyToManyField(Mode, blank=True)
    # 建立日期
    createdon = models.DateTimeField(auto_now_add=True)
    # 檢視次數
    view = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-createdon']

    def __str__(self):
        return self.title