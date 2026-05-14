from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Company
from .serializers import CompanyVerifySerializer, CompanySerializer


class VerifyCompanyView(APIView):
    """
    POST /api/company/verify/
    Body: { "company_code": "VISR" }
    Returns company info if the code is valid and active.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CompanyVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['company_code'].upper().strip()

        try:
            company = Company.objects.get(code=code, is_active=True)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Invalid or inactive company code.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                'valid': True,
                'company': CompanySerializer(company).data,
            },
            status=status.HTTP_200_OK,
        )
