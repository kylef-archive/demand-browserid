from django import forms

class BrowserIDForm(forms.Form):
    assertion = forms.CharField(widget=forms.HiddenInput())

    class Media:
        js = ('demandapp/browserid.js', 'https://browserid.org/include.js')
