from django import forms

class ReportForm(forms.Form):
    system = forms.CharField()
    province = forms.CharField()
    city = forms.CharField()
    testNum = forms.IntegerField(min_value=0)
    passNum = forms.IntegerField(min_value=0)
    reporter = forms.CharField()
    file = forms.FileField()
    