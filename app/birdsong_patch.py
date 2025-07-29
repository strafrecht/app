# patch wagtail-birdsong to prepare and send mails in background
# Temporarily disabled for Wagtail 3.0 upgrade

import logging

logger = logging.getLogger(__name__)


def patch_birdsong():
    """
    Monkey patch wagtail-birdsong - temporarily disabled for Wagtail 3.0 upgrade
    """
    # Temporarily disabled for Wagtail 3.0 upgrade
    # from birdsong.options import CampaignAdmin
    # CampaignAdmin.backend_class = SMTPBackgroundBackend
    pass
