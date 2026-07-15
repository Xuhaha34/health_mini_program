from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password_confirm = serializers.CharField(write_only=True, label='确认密码')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'phone', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError('两次密码不一致')
        if len(attrs['password']) < 6:
            raise serializers.ValidationError('密码长度不能少于6位')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(label='用户名/手机号')
    password = serializers.CharField(label='密码', write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('请输入用户名和密码')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('用户名或密码错误')

        if not user.is_active:
            raise serializers.ValidationError('账号已被禁用')

        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }


class UserInfoSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'avatar', 'avatar_url', 
                  'gender', 'age', 'height', 'weight', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    class Meta:
        model = User
        fields = ['phone', 'email', 'avatar', 'gender', 'age', 'height', 'weight']
        extra_kwargs = {
            'email': {'required': False},
        }


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(label='旧密码', write_only=True)
    new_password = serializers.CharField(label='新密码', write_only=True)
    new_password_confirm = serializers.CharField(label='确认新密码', write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs.pop('new_password_confirm'):
            raise serializers.ValidationError('两次新密码不一致')
        if len(attrs['new_password']) < 6:
            raise serializers.ValidationError('新密码长度不能少于6位')
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器（管理后台用）"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'gender', 'age', 
                  'height', 'weight', 'is_active', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器（管理后台用）"""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone', 'email', 'gender', 
                  'age', 'height', 'weight', 'is_active']
    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('密码长度不能少于6位')
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器（管理后台用）"""
    
    class Meta:
        model = User
        fields = ['phone', 'email', 'gender', 'age', 'height', 'weight', 'is_active']
        extra_kwargs = {
            'email': {'required': False},
        }
