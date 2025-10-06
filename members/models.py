# members/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# 1. የምርጫ አማራጮች (Choices)
REGION_CHOICES = (
    ("ADD", "አዲስ አበባ"),
    ("TIG", "ትግራይ"),
    ("AMH", "አማራ"),
    ("DD", "ድሬዳዋ"),
    ("ORO", "ኦሮሚያ"),
    ("SET", "ደቡብ ኢትዮጵያ"),
    ("SWE", "ደቡብ ምዕራብ ኢትዮጵያ"),
    ("SOM", "ሶማሌ"),
    ("GAM", "ጋምቤላ"),
    ("HAR", "ሀረሪ"),
    ("AFS", "አፋር"),
    ("BEN", "ቤኒሻንጉል ጉሙዝ"),
    ("SID", "ሲዳማ"),
)

GENDER_CHOICES = (
    ("M", "ወንድ"),
    ("F", "ሴት"),
)

EDUCATION_LEVEL_CHOICES = (
    ("NONE", "ትምህርት ደረጃ የሌለው"),
    ("PRIMARY", "የመጀመሪያ ደረጃ"),
    ("SECONDARY", "ሁለተኛ ደረጃ"),
    ("DIPLOMA", "ዲፕሎማ"),
    ("DEGREE", "ዲግሪ"),
    ("MASTERS", "ማስተርስ"),
    ("PHD", "ዶክትሬት"),
)

MEMBERSHIP_LEVEL_CHOICES = (
    ("REGULAR", "አባል"),
    ("COMMITTEE", "የኮሚቴ አባል"),
    ("LEADERSHIP", "አመራር"),
)


# 2. የአባል ሞዴል (Member Model) - በተጠየቀው መሰረት የተሻሻለ
class Member(models.Model):
    # ከበስተጀርባ የሚሰራ የሎግอิน አካውንት ማገናኛ (አይጠፋም)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="የስርዓት ተጠቃሚ አካውንት")
    
    # የተጠየቁት መስኮች በትክክለኛው ቅደም ተከተል
    full_name = models.CharField(max_length=255, verbose_name="ሙሉ ስም")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="ጾታ")
    date_of_birth = models.DateField(verbose_name="የትውልድ ቀን")
    photo = models.ImageField(upload_to='member_photos/', null=True, blank=True, verbose_name="ፎቶግራፍ")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="ስልክ ቁጥር")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="ኢሜይል")
    
    # የአድራሻ መረጃ
    region = models.CharField(max_length=3, choices=REGION_CHOICES, verbose_name="ክልል")
    zone = models.CharField(max_length=100, verbose_name="ዞን")
    woreda = models.CharField(max_length=100, verbose_name="ወረዳ")
    kebele = models.CharField(max_length=100, blank=True, null=True, verbose_name="ቀበሌ")
    city = models.CharField(max_length=100, verbose_name="ከተማ")

    # ተጨማሪ መረጃ
    education_level = models.CharField(max_length=15, choices=EDUCATION_LEVEL_CHOICES, verbose_name="የትምህርት ደረጃ")
    membership_level = models.CharField(max_length=15, choices=MEMBERSHIP_LEVEL_CHOICES, default="REGULAR", verbose_name="የአባልነት ደረጃ")

    # በስርዓቱ በራስ-ሰር የሚሞሉ
    membership_id = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="የአባልነት መለያ ቁጥር")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="የተመዘገበበት ቀን")
    is_active = models.BooleanField(default=True, verbose_name="ንቁ አባል")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # መለያ ቁጥር ከመፍጠራችን በፊት ኦብጀክቱ እንዲቀመጥ እናደርጋለን (ID ለማግኘት)
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new and not self.membership_id:
            region_code = self.region
            year = str(self.date_joined.year)[-2:]
            member_number = f"{self.id:04d}"

            self.membership_id = f"EUDP-{region_code}-{year}-{member_number}"
            # ዳግም ወደ save loop እንዳንገባ update_fields እንጠቀማለን
            super().save(update_fields=['membership_id'])

# ሌሎች ሞዴሎች (Meeting, Attendance, Announcement) እንዳሉ ይቀጥላሉ
# ... (ከዚህ በታች ያሉት ሌሎች ክላሶች ሳይለወጡ ይቀመጣሉ)
class Meeting(models.Model):
    title = models.CharField(max_length=200, verbose_name="የስብሰባ ርዕስ")
    date = models.DateTimeField(verbose_name="ቀን")
    location = models.CharField(max_length=255, verbose_name="ቦታ")
    def __str__(self): return self.title

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="አባል")
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name="ስብሰባ")
    is_present = models.BooleanField(default=True, verbose_name="ተገኝቷል")
    class Meta: unique_together = ('member', 'meeting')
    def __str__(self): return f"{self.member.full_name} - {self.meeting.title}"

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="ርዕስ")
    content = models.TextField(verbose_name="ይዘት")
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="የተለጠፈበት ቀን")
    def __str__(self): return self.title