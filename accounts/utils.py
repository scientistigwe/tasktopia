from django.contrib import messages

def add_message(request, message, level=messages.INFO):
    messages.add_message(request, level, message)