import json

from common.drf.permissions import NotAuthenticated
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.views import RevokeTokenView, TokenView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MyTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response


@sensitive_post_parameters('password')
@api_view(['POST'])
@permission_classes([NotAuthenticated])
def token(request):
    """
    Retrieves or refreshes access token

    The endpoint is used in the following flows: authorization code,
    password, client credentials.

    """

    return MyTokenView().dispatch(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_token(request):
    """
    Revokes access token

    """
    return RevokeTokenView().dispatch(request)
