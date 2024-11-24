from django.urls import path

app_name = "api/worklog"

from .views import CheckInView, CheckOutView, DailySummaryView, MonthlySummaryView

urlpatterns = [
    path("check-in/", CheckInView.as_view(), name="check-in"),
    path("check-out/", CheckOutView.as_view(), name="check-out"),
    path("daily-summary/", DailySummaryView.as_view(), name="daily-summary"),
    path("monthly-summary/", MonthlySummaryView.as_view(), name="monthly-summary"),
]
