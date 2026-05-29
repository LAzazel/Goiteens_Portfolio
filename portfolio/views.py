from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Count, Avg, Sum, Min, Max, F, ExpressionWrapper, FloatField
from django.contrib.auth import get_user_model

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


def orm_demo(request):
    """Demo page for teaching Django ORM filters and Q objects."""
    User = get_user_model()

    examples = []

    # 1. Simple filter / exclude
    examples.append({
        "title": "Усі активні користувачі",
        "qs": User.objects.filter(is_active=True)[:20],
        "sql": User.objects.filter(is_active=True).query,
    })

    examples.append({
        "title": "Усі, крім суперкористувачів",
        "qs": User.objects.exclude(is_superuser=True)[:20],
        "sql": User.objects.exclude(is_superuser=True).query,
    })

    # 2. Field lookups
    examples.append({
        "title": "Користувачі з Gmail",
        "qs": User.objects.filter(email__icontains='@gmail.com')[:20],
        "sql": User.objects.filter(email__icontains='@gmail.com').query,
    })

    # 3. Q objects example (projects)
    examples.append({
        "title": "Проєкти з Django OR React",
        "qs": Project.objects.filter(Q(title__icontains='Django') | Q(technologies__icontains='React'))[:20],
        "sql": Project.objects.filter(Q(title__icontains='Django') | Q(technologies__icontains='React')).query,
    })

    # 4. Orders example
    examples.append({
        "title": "Нові замовлення (status=new)",
        "qs": Order.objects.filter(status='new').order_by('-created_at')[:20],
        "sql": Order.objects.filter(status='new').order_by('-created_at').query,
    })

    # 5. Combination filter + exclude
    examples.append({
        "title": "Активні користувачі без тестових email",
        "qs": User.objects.filter(is_active=True).exclude(email__icontains='@test.com')[:20],
        "sql": User.objects.filter(is_active=True).exclude(email__icontains='@test.com').query,
    })

    for e in examples:
        e['sql'] = str(e['sql'])

    return render(request, "lessons/orm_demo.html", {"examples": examples})


def orm_aggregations(request):
    """Demo page for aggregate() and annotate() examples."""
    User = get_user_model()

    examples = []

    # 1. Aggregates on orders
    agg_orders = Order.objects.aggregate(
        total_budget=Sum('budget'),
        avg_budget=Avg('budget'),
        max_budget=Max('budget'),
        min_budget=Min('budget'),
    )
    examples.append({
        'title': 'Агрегації по замовленням (total/avg/min/max budget)',
        'aggregate': agg_orders,
    })

    # 2. Annotate projects with review counts and avg rating
    projects_qs = Project.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-review_count')[:20]
    examples.append({
        'title': 'Проєкти з review_count та avg_rating (annotate)',
        'qs': projects_qs,
        'sql': str(projects_qs.query),
    })

    # 3. Annotate projects with count of top reviews (rating>4)
    top_reviews_qs = Project.objects.annotate(
        top_reviews=Count('reviews', filter=Q(reviews__rating__gt=4))
    ).order_by('-top_reviews')[:20]
    examples.append({
        'title': 'Кількість топ-відгуків (rating>4) для кожного проєкту',
        'qs': top_reviews_qs,
        'sql': str(top_reviews_qs.query),
    })

    # 4. Annotate users with processed orders count
    users_qs = User.objects.annotate(processed_count=Count('order')).order_by('-processed_count')[:20]
    examples.append({
        'title': 'Користувачі з кількістю оброблених замовлень (processed_count)',
        'qs': users_qs,
        'sql': str(users_qs.query),
    })

    # 5. Expression: commission on order (5% of budget)
    orders_fee_qs = Order.objects.annotate(
        commission=ExpressionWrapper(F('budget') * 0.05, output_field=FloatField())
    ).order_by('-commission')[:20]
    examples.append({
        'title': 'Замовлення з аннотованою комісією (5% від бюджету)',
        'qs': orders_fee_qs,
        'sql': str(orders_fee_qs.query),
    })

    return render(request, 'lessons/orm_aggregations.html', {'examples': examples, 'aggregates': agg_orders})


