import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def protected_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_path):
        with open(media_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(media_path)}"'
            return response
    else:
        raise Http404
