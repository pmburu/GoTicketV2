from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

"""
1. Connect the user types with Djoser's UserCreateSerializer - inherit
2. Serialize user types data + details and present to the
endpoints
3. Create any necessary serializers
4. Unit Test
"""

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    """Create a new user - automatically triggering user_type"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "password",
            "last_login",
        ]
        read_only_fields = ["last_login"]
