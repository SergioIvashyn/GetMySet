from django.contrib import messages
from social_core.exceptions import AuthCanceled
from social_django.middleware import SocialAuthExceptionMiddleware
from django.shortcuts import HttpResponse, redirect
from social_core import exceptions as social_exceptions


class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        super(CustomSocialAuthExceptionMiddleware, self).process_exception(request, exception)
        if isinstance(exception, social_exceptions.AuthCanceled):
            messages.info(request, 'Auth Canceled')
            return redirect('index')
        else:
            raise exception
