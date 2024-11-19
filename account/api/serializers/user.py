from rest_framework import serializers
from account.models import User


class SimplifiedUserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def get_or_create_user(self):
        phone_number = self.validated_data['phone_number']
        user, created = User.objects.get_or_create(phone_number=phone_number)
        return user, created


class SimplifiedUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone_number', 'email', 'national_id', 'role',
            'first_name', 'last_name', 'avatar_url', 
            'is_active', 'is_staff', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SimplifiedChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        return value
