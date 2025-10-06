from django import forms
from django.contrib.auth.models import User
from .models import Member

class MemberCreationForm(forms.ModelForm):
    # የይለፍ ቃል እና የይለፍ ቃል ማረጋገጫ መስኮችን እንጨምራለን
    password = forms.CharField(widget=forms.PasswordInput, label="የይለፍ ቃል")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="የይለፍ ቃል ማረጋገጫ")

    class Meta:
        model = Member
        # ከ Member ሞዴል ላይ በፎርሙ እንዲታዩ የምንፈልጋቸው መስኮች
        # 'user' እና 'membership_id' በራስ-ሰር ስለሚፈጠሩ እዚህ አናካትታቸውም
        fields = [
            'full_name', 'gender', 'date_of_birth', 'photo', 
            'phone_number', 'email', 'region', 'zone', 'woreda', 
            'kebele', 'city', 'education_level'
        ]
        
        # ለ date_of_birth መስክ የ DateInput widget እንጠቀማለን (calendar እንዲያሳይ)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        # መጀመሪያ የ Django'ን ነባሪ clean ሜተድ እንጠራለን
        cleaned_data = super().clean()
        
        # ከ cleaned_data ውስጥ የይለፍ ቃሎችን እናገኛለን
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # ሁለቱም የይለፍ ቃሎች መኖራቸውን እና መመሳሰላቸውን እናረጋግጣለን
        if password and confirm_password and password != confirm_password:
            # የማይመሳሰሉ ከሆነ፣ የስህተት መልዕክት እንፈጥራለን
            raise forms.ValidationError(
                "የይለፍ ቃሎች አይመሳሰሉም! እባክዎ እንደገና ይሞክሩ።"
            )
        
        # ሁሉም ነገር ትክክል ከሆነ፣ cleaned_data'ውን እንመልሳለን
        return cleaned_data
            
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError("ይህ ስልክ ቁጥር ቀደም ብሎ ተመዝግቧል!")
        return phone
class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        # ተጠቃሚው እንዲያስተካክላቸው የምንፈቅድላቸውን መስኮች ብቻ እንዘረዝራለን
        # ስልክ ቁጥር (username) እና መለያ ቁጥር መቀየር የለባቸውም
        fields = [
            'full_name', 'gender', 'date_of_birth', 'photo', 
            'email', 'region', 'zone', 'woreda', 
            'kebele', 'city', 'education_level'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    # ፎርሙ ትክክለኛ መሆኑን ስናረጋግጥ የሚጠራ ተጨማሪ ተግባር
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        # ሁለቱ የይለፍ ቃሎች የማይመሳሰሉ ከሆነ የስህተት መልዕክት እንመልሳለን
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("የይለፍ ቃሎች አይመሳሰሉም!")
        
        return confirm_password
        
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # ይህ ስልክ ቁጥር ከዚህ በፊት ተመዝግቦ እንደሆነ እናረጋግጣለን (ለ User ሞዴል)
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError("ይህ ስልክ ቁጥር ቀደም ብሎ ተመዝግቧል!")
        return phone