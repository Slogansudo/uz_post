from uuid import uuid4


class SaveMediaFiles(object):

    def save_banner_image(instance, filename):
        image = filename.split('.')[-1]
        return f'banners/{uuid4()}.{image}'

