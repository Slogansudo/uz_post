from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled
from models.models import IPAddressLog


# class CustomRateThrottle(SimpleRateThrottle):
#     scope = 'user'
#     rate = '20/min'  # 20 requests per minute
#
#     def get_cache_key(self, request, view):
#         ident = self.get_ident(request)
#         url = request.path
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': f"{ident}:{url}"
#         }
#
#     def allow_request(self, request, view):
#         ident = self.get_ident(request)
#         url = request.path
#
#         # Retrieve or create IP address log
#         ip_log, created = IPAddressLog.objects.get_or_create(ip_address=ident, url=url)
#
#         # Get cache key and history of requests
#         self.key = self.get_cache_key(request, view)
#         self.history = self.cache.get(self.key, [])
#
#         # Get the current time
#         self.now = self.timer()
#
#         # Remove requests outside the current time window
#         self.history = [timestamp for timestamp in self.history
#                         if timestamp > self.now - self.duration]
#
#         # Update request count in IP log if not newly created
#         if not created:
#             ip_log.request_count = len(self.history)
#         ip_log.save()
#
#         # Check if request count exceeds the limit
#         if len(self.history) >= self.num_requests:
#             # Check if the IP is still throttled
#             if ip_log.request_count >= self.num_requests:
#                 raise Throttled(detail='Too many requests, please try again later.')
#
#         # Add current request time to history and update cache
#         self.history.insert(0, self.now)
#         self.cache.set(self.key, self.history, self.duration)
#
#         # Throttling successful
#         return self.throttle_success()
#
#     def wait(self):
#         # Calculate time until the next request can be made
#         time_elapsed = self.now - self.history[-1]
#         return self.duration - time_elapsed.seconds


from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled


class CustomRateThrottle(SimpleRateThrottle):
    scope = 'user'
    rate = '20/min'  # 20 requests per minute

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        url = request.path
        return self.cache_format % {
            'scope': self.scope,
            'ident': f"{ident}:{url}"
        }

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])

        # Get the current time
        self.now = self.timer()

        # Remove requests outside the current time window
        self.history = [timestamp for timestamp in self.history
                        if timestamp > self.now - self.duration]

        # Check if request count exceeds the limit
        if len(self.history) >= self.num_requests:
            raise Throttled(detail='Too many requests, please try again later.')

        # Add current request time to history and update cache
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)

        # Throttling successful
        return self.throttle_success()

    def wait(self):
        # Calculate time until the next request can be made
        time_elapsed = self.now - self.history[-1]
        return self.duration - time_elapsed.seconds
