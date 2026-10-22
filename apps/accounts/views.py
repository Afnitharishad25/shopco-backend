from django.shortcuts import render
from rest_framework import generics , permissions , status
from rest_framework.response import Response
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode


from .serializers import RegisterSerializer ,  UserSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ForgotPasswordView(generics.GenericAPIView):

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "If an account exists with this email, a reset link has been sent."
                },
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        token = default_token_generator.make_token(user)

        reset_link = (
            f"https://shopco-frontend-beta.vercel.app/"
            f"reset-password/{uid}/{token}"
        )

        send_mail(
            subject="Reset your password",
            message=(
                f"Hello {user.first_name},\n\n"
                f"Click the link below to reset your password:\n\n"
                f"{reset_link}\n\n"
                f"If you did not request a password reset, you can ignore this email."
            ),
            # from_email="noreply@shopco.com",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {
                "detail": "Reset link generated successfully.",
                "reset_link": reset_link,
            },
            status=status.HTTP_200_OK
        )

class ResetPasswordView(generics.GenericAPIView):

    def post(self, request, uidb64, token):
        new_password = request.data.get("password")
        confirm_password = request.data.get("confirmPassword")

        if not new_password or not confirm_password:
            return Response(
                {"detail": "Both password fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"detail": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {"detail": "Password must be at least 8 characters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "This reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK
        )