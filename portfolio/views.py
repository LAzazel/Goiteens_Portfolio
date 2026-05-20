from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings

from .models import Experience, Project, Skill, Order, Review
from .forms import OrderForm, ReviewForm


def home(request):
    projects = Project.objects.order_by("-created_at")[:6]
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    return render(
        request,
        "home.html",
        {
            "projects": projects,
            "skills": skills,
            "experiences": experiences,
        },
    )


def projects_list(request):
    qs = Project.objects.order_by("-created_at")
    tech = request.GET.get("tech")
    if tech:
        qs = qs.filter(technologies__icontains=tech)
    return render(request, "projects/list.html", {"projects": qs, "filter_tech": tech})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.project = project
            review.visible = False
            review.save()
            return redirect(f"{request.path}?review=sent")
    else:
        review_form = ReviewForm()

    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
            "review_form": review_form,
            "visible_reviews": project.reviews.filter(visible=True),
        },
    )


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # send notification to site owner (console or real backend from settings)
            subject = f"Нова заявка: {order.title}"
            body = (
                f"Нова заявка від {order.client_name}\n"
                f"Email: {order.client_email}\n"
                f"Телефон: {order.client_phone}\n"
                f"Бюджет: {order.budget}\n"
                f"Дедлайн: {order.deadline}\n\n"
                f"Опис:\n{order.description}\n\n"
                f"Переглянути в адмінці: {request.build_absolute_uri('/admin/portfolio/order/{}/change/'.format(order.pk))}"
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            # confirmation to client
            if order.client_email:
                send_mail(
                    f"Підтвердження заявки: {order.title}",
                    "Дякуємо! Ми отримали вашу заявку і зв'яжемося незабаром.",
                    settings.DEFAULT_FROM_EMAIL,
                    [order.client_email],
                )
            return redirect("order_thanks")
    else:
        form = OrderForm()
    return render(request, "order_form.html", {"form": form})


def order_thanks(request):
    return render(request, "order_thanks.html")


def staff_required(user):
    return user.is_active and user.is_staff


@user_passes_test(staff_required)
def dashboard_orders(request):
    qs = Order.objects.order_by("-created_at")
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    return render(request, "dashboard/orders.html", {"orders": qs})


def reviews_list(request):
    reviews = Review.objects.filter(visible=True).select_related("project").order_by("-created_at")
    return render(request, "reviews/list.html", {"reviews": reviews})


