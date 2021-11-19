from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import transaction


class MyOIDCAB(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)
        user.username = claims.get('sub', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user

    def update_groups(self, user, claims):
        """
        Transform roles obtained from keycloak into Django Groups and
        add them to the user. Note that any role not passed via keycloak
        will be removed from the user.
        """
        with transaction.atomic():
            user.groups.clear()
            for role in claims.get('roles'):
                group, _ = Group.objects.get_or_create(name=role)
                group.user_set.add(user)

    def get_userinfo(self, access_token, id_token, payload):
        """
        Get user details from the access_token and id_token and return
        them in a dict.
        """
        userinfo = super().get_userinfo(access_token, id_token, payload)
        # accessinfo = self.verify_token(access_token, nonce=payload.get('nonce'))
        # roles = accessinfo.get('realm_access', {}).get('roles', [])
        #
        # userinfo['roles'] = roles
        return userinfo

    def filter_users_by_claims(self, claims):
        email = claims.get('sub')
        if not email:
            return self.UserModel.objects.none()

        try:
            profile = User.objects.get(username=email)
            return [profile]

        except User.DoesNotExist:
            return self.UserModel.objects.none()
