from django.db import models

# Create your models here.


from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True) # 自动添加日期时间
    title = models.CharField(max_length=100, blank=True, default='') # 默认为空 blank=True
    code = models.TextField()
    linenos = models.BooleanField(default=False) # 是否开启行号码
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created'] # 按照created字段排序