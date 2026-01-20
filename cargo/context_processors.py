from .models import Order


def active_order(request):
    if request.user.is_authenticated:
        return {
            "active_order": request.user.orders
            .filter(status=Order.Status.IN_PROGRESS)
            .first()
        }
    return {"active_order": None}
