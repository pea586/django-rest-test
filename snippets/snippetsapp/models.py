from django.db import models

# Create your models here.


from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True) # 自动添加日期时间
    title = models.CharField(max_length=100, blank=True, default='') # 默认为空 blank=True
    code = models.TextField()
    linenos = models.BooleanField(default=False) # 是否开启行号码
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE,
                              null=True, blank=True)
    highlighted = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['created'] # 按照created字段排序

    def save(self, *args, **kwargs):
        """高亮显示相关"""
        lexer = get_lexer_by_name(self.language) # lexer：语法
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)
