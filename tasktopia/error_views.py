from django.shortcuts import render
from django.http import HttpResponse
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

def handler500(request):
    logger.error(f"BASE_DIR: {settings.BASE_DIR}")
    logger.error(f"Template dirs: {settings.TEMPLATES[0]['DIRS']}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"accounts/templates/registration contents: {os.listdir(os.path.join(settings.BASE_DIR, 'accounts', 'templates', 'registration'))}")
    
    try:
        return render(request, 'registration/500.html', status=500)
    except Exception as e:
        logger.error(f"Error rendering 500.html: {str(e)}")
        return HttpResponse("500 Internal Server Error", status=500)