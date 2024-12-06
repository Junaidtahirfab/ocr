from django.contrib import admin
from account.models import User,OtpVerify,Company,Role
from .utils import create_roles
# Register your models here.


admin.site.register(User)
admin.site.register(OtpVerify)
admin.site.register(Company)
admin.site.register(Role)
create_roles()