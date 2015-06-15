from django import forms

class ReportForm(forms.Form):
    testNum = forms.IntegerField(min_value=0)
    passNum = forms.IntegerField(min_value=0)
    projectTeamID = forms.IntegerField(min_value=0)
    file = forms.FileField()
    