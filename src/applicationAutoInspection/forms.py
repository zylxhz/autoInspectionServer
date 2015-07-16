from django import forms

class ReportForm(forms.Form):
    system = forms.CharField()
    province = forms.CharField()
    city = forms.CharField()
    reporter = forms.CharField()
    zip = forms.FileField()
    