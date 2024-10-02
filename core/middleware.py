#
# from django.utils.deprecation import MiddlewareMixin
# from django.utils import timezone
# from models.models import IPAddressLog
#
#
# class LogIPMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         ip = self.get_client_ip(request)
#         url = request.path
#         if ip and url:
#             ip_log, created = IPAddressLog.objects.get_or_create(ip_address=ip, url=url)
#             ip_log.request_count += 1
#             ip_log.last_request_time = timezone.now()
#             ip_log.save()
#
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0].strip()
#             #ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


# from models.models import IPAddressLog  # IP manzil loglarini ushlashni xohlamasangiz, import qilish shart emas


class LogIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # IP manzilini olish
        ip = self.get_client_ip(request)
        url = request.path

        # Ushbu kodni o'chirish yoki kommentga olish
        # if ip and url:
        #     ip_log, created = IPAddressLog.objects.get_or_create(ip_address=ip, url=url)
        #     ip_log.request_count += 1
        #     ip_log.last_request_time = timezone.now()
        #     ip_log.save()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
