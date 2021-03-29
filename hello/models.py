import re
from django.db import models
import datetime
from django.urls import reverse
from datetime import datetime as dt
from django.contrib.auth.models import User

now = datetime.datetime.now()
y = now.year
m = now.month
d = now.day
Year_data = [(2018, 2018),(2019, 2019),(2020, 2020),(2021, 2021),(2022, 2022),(2023, 2023),(2024, 2024), (2025, 2025)]
Month_data = [(1,1),(2,2), (3,3),(4,4),(5,5), (6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)]
Day_data = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31)]

class Study(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField('year', choices=Year_data, default=y)
    month = models.IntegerField('month',choices=Month_data, default=m)
    day = models.IntegerField('day', choices=Day_data, default=d)
    hour = models.FloatField('hour', default=0)
    comment = models.CharField('comment', max_length=250, blank=True)
     
    def __str__(self):
        return  '(' + str(self.year) + '.' + str(self.month) + '.' + str(self.day) + ')'

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    purpose_data = [
        ('現在の仕事', '現在の仕事'), 
        ('転職', '転職'), 
        ('趣味', '趣味'), 
        ('その他', 'その他')]
    or_continue = [
        ('1', '使用中'),
        ('0', '退会希望'),
    ]
    language = models.CharField('language', max_length=250, blank=True)
    purpose = models.CharField('purpose', choices=purpose_data, max_length=250, blank=False, default=purpose_data[3])
    weekday_study = models.FloatField('weekdays', default=0)
    holiday_study = models.FloatField('holidays', default=0)
    is_private = models.TextField('is_private', max_length=250, blank=True)
    is_continue = models.CharField('is_continue', choices=or_continue, max_length=250, blank=False, default=or_continue[0])
    