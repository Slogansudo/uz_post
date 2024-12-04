from rest_framework.permissions import BasePermission
from models.models import CustomUser



#  id |    app_label    |           model
# ----+-----------------+----------------------------
#   1 | admin           | logentry
#   2 | auth            | permission
#   3 | auth            | group
#   4 | contenttypes    | contenttype
#   5 | sessions        | session
#   6 | authtoken       | token
#   7 | authtoken       | tokenproxy
#   8 | token_blacklist | blacklistedtoken
#   9 | token_blacklist | outstandingtoken
#  10 | models          | ipaddresslog
#  11 | models          | usersrequests
#  12 | models          | customuser
#  13 | db_models       | advertisements
#  14 | db_models       | advertising
#  15 | db_models       | annualreports
#  16 | db_models       | banners
#  17 | db_models       | branchservices
#  18 | db_models       | businessplanscompleted
#  19 | db_models       | chartersociety
#  20 | db_models       | dividends
#  21 | db_models       | essentialfacts
#  22 | db_models       | executiveapparatus
#  23 | db_models       | faq
#  24 | db_models       | informationaboutissuer
#  25 | db_models       | internaldocuments
#  26 | db_models       | marks
#  27 | db_models       | menuelements
#  28 | db_models       | pages
#  29 | db_models       | postalservices
#  30 | db_models       | purchases
#  31 | db_models       | quarterreports
#  32 | db_models       | rates
#  33 | db_models       | regionalbranches
#  34 | db_models       | savemediafiles
#  35 | db_models       | securitypapers
#  36 | db_models       | services
#  37 | db_models       | shabloncontactspecialtitle
#  38 | db_models       | shablonservices
#  39 | db_models       | shablonuzposttelnumber
#  40 | db_models       | sitesettings
#  41 | db_models       | slides
#  42 | db_models       | socialmedia
#  43 | db_models       | statisticitems
#  44 | db_models       | tegbranches2
#  45 | db_models       | tegexperience
#  46 | db_models       | tegregions
#  47 | db_models       | tegvacancies
#  48 | db_models       | tegworkingdays
#  49 | db_models       | themaquestions
#  50 | db_models       | userinstructions
#  51 | db_models       | vacanciesimages
#  52 | db_models       | menu
#  53 | db_models       | partners
#  54 | db_models       | contact
#  55 | db_models       | statistics
#  56 | db_models       | events
#  57 | db_models       | organicmanagements
#  58 | db_models       | branches
#  59 | db_models       | uzpostnews
#  60 | db_models       | vacancies
#  61 | db_models       | categoryservices


class IsManagerProfileOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])
        # Ruxsatlar tekshiruvi
        if 'customuser' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("customuser", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("customuser", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("customuser", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("customuser", []):
                return True


class UserRequestsOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'usersrequests' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("usersrequests", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("usersrequests", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("usersrequests", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("usersrequests", []):
                return True
        return False


class ManageAdvertisements(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'advertisements' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("advertisements", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("advertisements", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("advertisements", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("advertisements", []):
                return True
        return False


class ManageAdvertising(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'advertising' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("advertising", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("advertising", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("advertising", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("advertising", []):
                return True
        return False


class ManageAnnualReports(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'annualreports' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("annualreports", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("annualreports", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("annualreports", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("annualreports", []):
                return True
        return False


class ManageBanners(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'banners' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("banners", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("banners", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("banners", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("banners", []):
                return True
        return False


class ManageBranchServices(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'branchservices' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("branchservices", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("branchservices", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("branchservices", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("branchservices", []):
                return True
        return False


class ManageBusinessPlansCompleted(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'businessplanscompleted' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("businessplanscompleted", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("businessplanscompleted", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("businessplanscompleted", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("businessplanscompleted", []):
                return True
        return False


class ManageCharterSociety(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'chartersociety' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("chartersociety", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("chartersociety", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("chartersociety", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("chartersociety", []):
                return True
        return False


class ManageDividends(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'dividends' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("dividends", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("dividends", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("dividends", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("dividends", []):
                return True
        return False


class ManageEssentialFacts(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'essentialfacts' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("essentialfacts", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("essentialfacts", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("essentialfacts", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("essentialfacts", []):
                return True
        return False


class ManageExecutiveApparatus(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'executiveapparatus' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("executiveapparatus", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("executiveapparatus", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("executiveapparatus", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("executiveapparatus", []):
                return True
        return False


class ManageFAQ(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'faq' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("faq", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("faq", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("faq", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("faq", []):
                return True
        return False


class ManageInformationAboutIssuer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'informationaboutissuer' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("informationaboutissuer", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("informationaboutissuer", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("informationaboutissuer", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("informationaboutissuer", []):
                return True
        return False


class ManageInternalDocuments(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'internaldocuments' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("internaldocuments", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("internaldocuments", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("internaldocuments", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("internaldocuments", []):
                return True
        return False


class ManageMarks(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'marks' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("marks", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("marks", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("marks", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("marks", []):
                return True
        return False


class ManageMenuElements(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'menuelements' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("menuelements", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("menuelements", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("menuelements", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("menuelements", []):
                return True
        return False


class ManagePages(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'pages' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("pages", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("pages", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("pages", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("pages", []):
                return True
        return False
#########


class ManageCategoryPages(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'categorypages' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("categorypages", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("categorypages", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("categorypages", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("categorypages", []):
                return True
        return False


class ManageControlCategoryPages(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                     data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'controlcategorypages' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("controlcategorypages", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("controlcategorypages", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("controlcategorypages", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("controlcategorypages", []):
                return True
        return False

#########


class ManagePostalServices(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'postalservices' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("postalservices", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("postalservices", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("postalservices", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("postalservices", []):
                return True
        return False


class ManagePurchases(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'purchases' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("purchases", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("purchases", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("purchases", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("purchases", []):
                return True
        return False


class ManageQuarterReports(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'quarterreports' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("quarterreports", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("quarterreports", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("quarterreports", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("quarterreports", []):
                return True
        return False


class ManageRates(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'rates' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("rates", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("rates", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("rates", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("rates", []):
                return True
        return False


class ManageRegionalBranches(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'regionalbranches' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("regionalbranches", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("regionalbranches", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("regionalbranches", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("regionalbranches", []):
                return True
        return False


class ManageSaveMediaFiles(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'savemediafiles' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("savemediafiles", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("savemediafiles", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("savemediafiles", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("savemediafiles", []):
                return True
        return False


class ManageSecurityPapers(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'securitypapers' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("securitypapers", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("securitypapers", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("securitypapers", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("securitypapers", []):
                return True
        return False


class ManageServices(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'services' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("services", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("services", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("services", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("services", []):
                return True
        return False


class ManageCategoryServices(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'services' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("categoryservices", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("categoryservices", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("categoryservices", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("categoryservices", []):
                return True
        return False


class ManageShablonContactSpecialTitle(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'shabloncontactspecialtitle' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("shabloncontactspecialtitle", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("shabloncontactspecialtitle", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("shabloncontactspecialtitle", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("shabloncontactspecialtitle", []):
                return True
        return False


class ManageShablonServices(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'shablonservices' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("shablonservices", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("shablonservices", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("shablonservices", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("shablonservices", []):
                return True
        return False


class ManageShablonUzPostTelNumber(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'shablonuzposttelnumber' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("shablonuzposttelnumber", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("shablonuzposttelnumber", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("shablonuzposttelnumber", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("shablonuzposttelnumber", []):
                return True
        return False


class ManageSiteSettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'sitesettings' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("sitesettings", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("sitesettings", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("sitesettings", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("sitesettings", []):
                return True
        return False


class ManageSlides(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'slides' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("slides", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("slides", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("slides", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("slides", []):
                return True
        return False


class ManageSocialMedia(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'socialmedia' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("socialmedia", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("socialmedia", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("socialmedia", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("socialmedia", []):
                return True
        return False


class ManageStatisticItems(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'statisticitems' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("statisticitems", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("statisticitems", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("statisticitems", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("statisticitems", []):
                return True
        return False


class ManageTegBranches2(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'tegbranches2' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("tegbranches2", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("tegbranches2", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("tegbranches2", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("tegbranches2", []):
                return True
        return False


class ManageTegExperience(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'tegexperience' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("tegexperience", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("tegexperience", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("tegexperience", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("tegexperience", []):
                return True
        return False


class ManageTegRegions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'tegregions' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("tegregions", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("tegregions", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("tegregions", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("tegregions", []):
                return True
        return False


class ManageTegVacancies(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'tegvacancies' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("tegvacancies", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("tegvacancies", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("tegvacancies", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("tegvacancies", []):
                return True
        return False


class ManageTegWorkingdays(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'tegworkingdays' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("tegworkingdays", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("tegworkingdays", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("tegworkingdays", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("tegworkingdays", []):
                return True
        return False


class ManageThemaQuestions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'themaquestions' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("themaquestions", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("themaquestions", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("themaquestions", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("themaquestions", []):
                return True
        return False


class ManageUserInstructions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'userinstructions' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("userinstructions", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("userinstructions", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("userinstructions", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("userinstructions", []):
                return True
        return False


class ManageVacanciesImages(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'vacanciesimages' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("vacanciesimages", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("vacanciesimages", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("vacanciesimages", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("vacanciesimages", []):
                return True
        return False


class ManageMenu(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'menu' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("menu", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("menu", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("menu", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("menu", []):
                return True
        return False


class ManagePartners(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'partners' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("partners", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("partners", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("partners", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("partners", []):
                return True
        return False


class ManageContact(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'contact' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("contact", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("contact", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("contact", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("contact", []):
                return True
        return False


class ManageStatistics(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'statistics' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("statistics", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("statistics", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("statistics", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("statistics", []):
                return True
        return False


class ManageEvents(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'events' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("events", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("events", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("events", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("events", []):
                return True
        return False


class ManageOrganicmanagements(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'organicmanagements' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("organicmanagements", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("organicmanagements", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("organicmanagements", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("organicmanagements", []):
                return True
        return False


class ManageBranches(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'branches' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("branches", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("branches", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("branches", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("branches", []):
                return True
        return False


class ManageUzPostNews(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'uzpostnews' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("uzpostnews", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("uzpostnews", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("uzpostnews", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("uzpostnews", []):
                return True
        return False


class ManageVacancies(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            exist_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            return False

        # Foydalanuvchi hech qanday guruhga tegishli bo'lmasa, ruxsat berilmaydi
        if not exist_user.groups.exists():
            return False

        # Ruxsatlar va tegishli content type modelini olish
        permissions = [perm for group in exist_user.groups.all() for perm in group.permissions.all()]
        data = {}
        for perm in permissions:
            data[perm.content_type.model] = []
            for per in permissions:
                if per.codename.split("_")[1] == perm.content_type.model:
                    data[perm.content_type.model].append(per.codename.split("_")[0])

        if 'vacancies' in data.keys():
            if request.method in ('GET', 'OPTIONS') and "view" in data.get("vacancies", []):
                return True
            if request.method in ('POST', 'OPTIONS') and "add" in data.get("vacancies", []):
                return True
            if request.method in ('PUT', 'OPTIONS') and "change" in data.get("vacancies", []):
                return True
            if request.method in ('DELETE', 'OPTIONS') and "delete" in data.get("vacancies", []):
                return True
        return False


