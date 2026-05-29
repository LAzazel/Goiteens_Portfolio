from django.urls import path

from .views import (
    home,
    projects_list,
    project_detail,
    create_order,
    order_thanks,
    dashboard_orders,
    reviews_list,
    orm_demo,
    orm_aggregations,
)

urlpatterns = [
    path("", home, name="home"),
    path("projects/", projects_list, name="projects_list"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("order/", create_order, name="create_order"),
    path("order/thanks/", order_thanks, name="order_thanks"),
    path("dashboard/orders/", dashboard_orders, name="dashboard_orders"),
    path("reviews/", reviews_list, name="reviews_list"),
    path("lessons/orm/", orm_demo, name="orm_demo"),
    path("lessons/orm/aggregations/", orm_aggregations, name="orm_aggregations"),
]

