from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class VercelStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.BASE_DIR, 'media')
        if base_url is None:
            base_url = '/media/'
        super().__init__(location, base_url)

    def _save(self, name, content):
        # Create the directory if it doesn't exist
        dirname = os.path.dirname(self.path(name))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return super()._save(name, content) 