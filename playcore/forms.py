from django import forms
import playcore.core as core

class TrackForm(forms.Form):
    search = forms.RegexField(regex=r'^.+$', max_length=60)
    page = forms.IntegerField(required=False)
    
    def clean_page(self):
        is_page = 'page' in self.cleaned_data
        if not ((not is_page) or (is_page and self.cleaned_data['page'])):
            return 1
        
        return self.cleaned_data['page']
        
    def get_results(self):
        return core.requestSongs(self.cleaned_data['search'], self.cleaned_data['page'])