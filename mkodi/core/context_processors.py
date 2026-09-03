from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum

from payments.models import Payment
from taxpayers.models import Taxpayer


def admin_metrics(request):
    if not request.path.startswith('/admin/'):
        return {}

    return {
        'admin_metrics': {
            'taxpayers': Taxpayer.objects.count(),
            'active_taxpayers': Taxpayer.objects.filter(is_active=True).count(),
            'payments': Payment.objects.count(),
            'payment_total': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'average_compliance': Taxpayer.objects.aggregate(score=Avg('tax_compliance_score'))['score'] or 0,
            'users': get_user_model().objects.count(),
        }
    }