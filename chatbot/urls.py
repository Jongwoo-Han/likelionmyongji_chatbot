from django.conf.urls import url, include
from .views import chatbotView

urlpatterns = [
    url(r'^07212a3b56af23fd34af882775a00e222097411895e28f5301/?$', chatbotView.as_view())
]
