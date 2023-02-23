from django import forms
from .models import Listing
from django.utils.translation import gettext_lazy as _


class CreateListingForm(forms.ModelForm):
    class Meta:
        AGE_CHOICES = (
            ('', 'Select an age'),
            ('10', '10'),  # First one is the value of select option and second is the displayed value in option
            ('15', '15'),
            ('20', '20'),
            ('25', '25'),
            ('26', '26'),
            ('27', '27'),
            ('28', '28'),
        )
        model = Listing
        fields = ('selling', 'selling_currency', 'buying', 'buying_currency', 'purpose', 'is_published')
        # fields = '__all__'
        labels = {
            'selling': _('I have'),
            'buying': _('I want'),
            'is_published': _('publish')
        }
        help_texts = {
            'selling': _('you are selling'),
            'buying': _('you are buying'),
        }
        # error_messages = {
        #     'selling': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
        widgets = {
            'selling': forms.TextInput(attrs={'placeholder': ''}),
            'buying': forms.TextInput(attrs={'placeholder': ''}),
            'selling_currency': forms.Select(choices=AGE_CHOICES, attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(
            #     attrs={'placeholder': 'Enter description here'}),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
    #     super().__init__(*args, **kwargs)
    #     # self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(user=user)
    #     self.fields['user'] = user
    #     x = 5


