from django import forms

class ReportForm(forms.Form):
    system = forms.CharField()
    province = forms.CharField()
    city = forms.CharField()
    reporter = forms.CharField()
    report_file = forms.FileField()
    log_file = forms.FileField()
    