from django.urls import (
	path
)

from .views import (
	login_view,
	logout_view
)

app_name = 'accounts'

urlpatterns = [
	path('login/', login_view),
	path('logout/', logout_view),

]