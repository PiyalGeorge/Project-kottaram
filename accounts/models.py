import datetime

from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from requests import request, ConnectionError


class User(AbstractUser):
    '''
    model for User model
    '''
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(_('Date of birth'), null=True, blank=True)
    profile_picture = models.ImageField(_('Profile picture'), upload_to='user_profile_picture', null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=15, null=True, blank=True)
    nickname = models.CharField(_('Nickname'), max_length=200, null=True, blank=True)

    class Meta:
        abstract = False
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


@receiver(user_signed_up, sender=User)
def save_account_details(sender, **kwargs):
    user = kwargs.pop('user')
    if user.socialaccount_set.filter(provider='facebook'):
        extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        if extra_data:
            id = extra_data['id']
            name = extra_data['name']
            if 'gender' in extra_data:
                gender = extra_data['gender']
                if gender == 'female':
                    user.gender = 'F'
                else:
                    user.gender = 'M'
            if 'birthday' in extra_data:
                birthday = extra_data['birthday']
                user.dob = datetime.date(int(birthday[6:]), int(birthday[:2]), int(birthday[3:5])).strftime("%Y-%m-%d")
            if id:
                profile_picture_url = "http://graph.facebook.com/{0}/picture?type=large".format(id)

                try:
                    response = request('GET', profile_picture_url)
                    response.raise_for_status()
                except ConnectionError:
                    pass
                else:
                    user.profile_picture.save(name+"_"+str(id)+".jpg", ContentFile(response.content), save=False)

            if name:
                user.nickname = name
            user.save()
    if user.socialaccount_set.filter(provider='google'):
        extra_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        if extra_data:
            id = extra_data['id']
            name = extra_data['name']
            if 'gender' in extra_data:
                gender = extra_data['gender']
                if gender == 'female':
                    user.gender = 'F'
                else:
                    user.gender = 'M'
            if 'picture' in extra_data:
                profile_picture_url = extra_data['picture']

                try:
                    response = request('GET', profile_picture_url)
                    response.raise_for_status()
                except ConnectionError:
                    pass
                else:
                    user.profile_picture.save(name+"_"+str(id)+".jpg", ContentFile(response.content), save=False)

            if name:
                user.nickname = name
            user.save()
    if user.socialaccount_set.filter(provider='twitter'):
        extra_data = user.socialaccount_set.filter(provider='twitter')[0].extra_data
        if extra_data:
            id = extra_data['id']
            name = extra_data['name']
            if 'profile_image_url' in extra_data or 'profile_image_url_https' in extra_data:
                if 'profile_image_url' in extra_data:
                    picture = extra_data['profile_image_url']
                    profile_picture_url = picture.replace('_normal','')

                    try:
                        response = request('GET', profile_picture_url)
                        response.raise_for_status()
                    except ConnectionError:
                        pass
                    else:
                        user.profile_picture.save(name+"_"+str(id)+".jpg", ContentFile(response.content), save=False)

                elif 'profile_image_url_https' in extra_data:
                    picture = extra_data['profile_image_url_https']
                    profile_picture_url = picture.replace('_normal','')

                    try:
                        response = request('GET', profile_picture_url)
                        response.raise_for_status()
                    except ConnectionError:
                        pass
                    else:
                        user.profile_picture.save(name+"_"+str(id)+".jpg", ContentFile(response.content), save=False)

                else:
                    pass
            if name:
                user.nickname = name
            user.save()
