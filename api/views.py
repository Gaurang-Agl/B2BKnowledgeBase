from django.db import transaction
from django.db.models import Q, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import KBEntry, QueryLog
from .permissions import IsAdminUser
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Registration successful.",
                    "username": user.username,
                    "company_name": user.company.company_name,
                    "api_key": user.company.api_key,
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "username": user.username,
                "company_name": user.company.company_name,
                "api_key": user.company.api_key,
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )

class KBQueryView(APIView):

    def post(self, request):
        search_term = request.data.get('search')

        if not search_term or not search_term.strip():
            return Response(
                {
                    "error": "search is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        search_term = search_term.strip()

        company = request.user.company

        with transaction.atomic():

            results = KBEntry.objects.filter(
                Q(question__icontains=search_term) |
                Q(answer__icontains=search_term)
            )

            results_count = results.count()

            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=results_count
            )

        data = [
            {
                "id": entry.id,
                "question": entry.question,
                "answer": entry.answer,
                "category": entry.category,
            }
            for entry in results
        ]

        return Response(
            {
                "search": search_term,
                "count": results_count,
                "results": data
            },
            status=status.HTTP_200_OK
        )

class UsageSummaryView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_queries = QueryLog.objects.aggregate(
            total=Count('id')
        )['total']

        unique_companies = QueryLog.objects.values(
            'company'
        ).distinct().count()

        top_searches = QueryLog.objects.values(
            'search_term'
        ).annotate(
            count=Count('id')
        ).order_by(
            '-count'
        )[:5]

        return Response(
            {
                "total_queries": total_queries,
                "active_companies": unique_companies,
                "top_search_terms": list(top_searches)
            },
            status=status.HTTP_200_OK
        )