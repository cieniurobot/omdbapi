from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class Index(APIView):
    """ OMDb API """

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome in OMDb API."})


class SearchView(APIView):
    """
        Search view
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Search view here"})
