from secrets import token_hex

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from yamdb.models import User

from api.serializers import SignUpSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            code = token_hex(16)
            self.send_code(email, code)
            # Громоздко выглядит, потом поправлю.
            if not User.objects.filter(username=username, email=email).exists():
                if (User.objects.filter(username=username).exists()
                        or User.objects.filter(email=email).exists()):
                    message = 'Username or Email already taken'
                    return Response(
                        data={'error:': message},
                        status=status.HTTP_400_BAD_REQUEST)
                User.objects.create(
                    email=email, username=username, confirmation_code=code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_code(self, email, code):
        subject = 'YaMDB Confirmation Code'
        message = f'Confirmation Code: {code}'
        from_email = 'YaMDB@email.com'
        send_mail(subject, message, from_email, [email, ], fail_silently=False)

