from django.contrib.auth.models import UserManager


# this method ensures the user can login with case insensitive username at login screen
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username: username})