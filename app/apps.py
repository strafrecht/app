from django.apps import AppConfig

class MainAppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # monkey patch Django-Wiki
        from .wiki_patch import patch_wiki
        patch_wiki()
        from .birdsong_patch import patch_birdsong
        patch_birdsong()
