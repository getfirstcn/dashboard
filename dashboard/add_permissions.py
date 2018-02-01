from django.contrib.auth.models import Permission, User

permission = Permission.objects.get(codename='add_server')
print(permission)
User.objects.get(username='xiluo').user_permissions.add(permission)