from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# 회원가입폼 커스텀 
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

