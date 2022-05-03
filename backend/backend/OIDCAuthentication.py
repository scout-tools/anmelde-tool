from basic.models import ScoutHierarchy
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class MyOIDCAB(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)
        user.save()

        self.set_user_info(user, claims)
        self.update_groups(user, claims)

        return user

    def update_user(self, user, claims):
        self.set_user_info(user, claims)
        self.update_groups(user, claims)
        return user

    def update_groups(self, user, claims):
        """
        Transform roles obtained from keycloak into Django Groups and
        add them to the user. Note that any role not passed via keycloak
        will be removed from the user.
        """
        with transaction.atomic():
            user.groups.clear()
            for role in claims.get('roles', []):
                group, _ = Group.objects.get_or_create(name=role)
                group.user_set.add(user)

    def set_user_info(self, user: User, claims):
        user.username = claims.get('email', '')

        if claims.get('fahrtenname', ''):
            user.userextended.scout_name = claims.get('fahrtenname', '')
        else:
            user.userextended.scout_name = claims.get('given_name', '')

        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        stamm = claims.get('stamm', '')
        bund = claims.get('bund', '')

        if stamm and bund and not user.userextended.scout_organisation:
            stamm = stamm.replace('stamm', '')
            found_bund = ScoutHierarchy.objects.filter(level=3, abbreviation=bund).first()
            found_stamm = ScoutHierarchy.objects.filter(
                Q(name__contains=stamm, parent=found_bund) | Q(name__contains=stamm, parent__parent=found_bund))
            if len(found_stamm) == 1:
                user.userextended.scout_organisation = found_stamm.first()
                user.userextended.successfull_initialised = True
        user.userextended.save()
        user.save()
