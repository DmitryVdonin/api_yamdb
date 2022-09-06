from reviews.models import User
from reviews.token_generator import confirmation_code
from django.core.mail import send_mail


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer)::
    if request.method == 'POST':
        if serializer.is_valid():
            user = serializer.save(commit=False)
            password = confirmation_code.make_token(user)
            user.password = password
            user.is_active = False
            user.save()
            mail_subject = 'Confirm your email account.'
            message = f'user: {user}, password: {password}
            to_email = serializer.data.get('email')
            send_mail(
                mail_subject,
                message,
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
                )

