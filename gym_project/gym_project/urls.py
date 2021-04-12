
from django.contrib import admin
from django.urls import path, include
# from member.views import KhaltiRequestView, KhaltiVerifyView, EsewaRequestView, EsewaVerifyView
from member import views as member_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
    # path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),

    # path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),
    # path("esewa-verify/", EsewaVerifyView.as_view(), name="esewaverify"),

    path('', include('member.urls')),
    path('scanner', include('scanner.urls')),

    path('register/', member_views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='member/login.html',
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='member/logout.html'), name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
