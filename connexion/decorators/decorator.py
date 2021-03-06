import functools
import logging

logger = logging.getLogger('connexion.decorators.decorator')


class BaseDecorator(object):

    def __call__(self, function):
        """
        :type function: types.FunctionType
        :rtype: types.FunctionType
        """
        return function

    def __repr__(self):  # pragma: no cover
        """
        :rtype: str
        """
        return '<BaseDecorator>'


class BeginOfRequestLifecycleDecorator(BaseDecorator):
    """Manages the lifecycle of the request internally in Connexion.

    Transforms the operation handler response into a `ConnexionRequest`
    that can be manipulated by the series of decorators during the
    lifecycle of the request.
    """

    def __init__(self, api, mimetype):
        self.api = api
        self.mimetype = mimetype

    def __call__(self, function):
        """
        :type function: types.FunctionType
        :rtype: types.FunctionType
        """
        @functools.wraps(function)
        def wrapper(request):
            response = function(request)
            return self.api.get_response(response, self.mimetype, request)

        return wrapper


class EndOfRequestLifecycleDecorator(BaseDecorator):
    """Manages the lifecycle of the request internally in Connexion.
    Filter the ConnexionRequest instance to return the corresponding
    flask.Response object.
    """

    def __init__(self, api, mimetype):
        self.api = api
        self.mimetype = mimetype

    def __call__(self, function):
        """
        :type function: types.FunctionType
        :rtype: types.FunctionType
        """
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            request = self.api.get_request(*args, **kwargs)
            response = function(request)
            return self.api.get_response(response, self.mimetype, request)

        return wrapper
