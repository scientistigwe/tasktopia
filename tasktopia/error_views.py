from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def handler500(request):
    """Custom 500 error handler"""
    # Log the error
    logger.error('Server Error: %s', request.path,
                 exc_info=True,
                 extra={
                     'status_code': 500,
                     'request': request
                 })
    
    # Render the error template
    return render(request, '500.html', status=500)