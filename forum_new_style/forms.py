from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, TextInput
from django.template.loader import render_to_string

from models import Post, Thread

#####################################

class PostForm(forms.Form):
    
    #spam prevention field, ala contrib.comments
    spam_prevent = forms.CharField(required=False,
                    widget=TextInput(attrs={'style': "display:none"}))
    
    as_anon = forms.BooleanField(label="Post Anonymously?", required=False)
    as_admin = forms.BooleanField(label="Post as Admin?", required=False)
    body = forms.CharField(widget=forms.Textarea())
    
class ThreadForm(forms.Form):
    title = forms.CharField(max_length=64)
    
    
def render_new_form(postform, threadform=None, user=None, captcha_error=""):
    """
    Render the new post form based on the new_post.html template
    """
    
    if getattr(settings, "FORUM_USE_RECAPTCHA", False):
        c2 = {"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
              "captcha_error": captcha_error}
        recaptcha = render_to_string('recaptcha.html', c2)
    else:
        recaptcha = ""
        
    c = {'postform': postform,
         'threadform': threadform,
         'user': user,
         'button': 'Reply',
         "recaptcha": recaptcha}
    
    if threadform:
        # if there is a thread form, then change the text of the submit button
        c.update({"button": "Thread"})
    
    return render_to_string('new_post.html', c)
