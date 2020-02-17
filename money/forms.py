from django import forms
from .models import Money
class SpendingForm(forms.Form):
    choices = (
            ('食費', '食費'),
            ('学費', '学費'),
            ('交通費', '交通費'),
            ('趣味', '趣味'),
            )
    use_date = forms.DateTimeField(label='日付')
    cost = forms.IntegerField(label='金額')
    detail = forms.CharField(
            max_length=200,
            label='用途'
            )
    category = forms.ChoiceField(choices=choices, label='カテゴリー')