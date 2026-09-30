import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# NOTIFICATION (async, triggered from view)
# ─────────────────────────────────────────────
@shared_task
def send_booking_notification(booking_id, user_id, event='created'):
    message = f"📩 [NOTIFICATION → user {user_id}] Booking #{booking_id}: {event}"
    logger.info(message)
    print(message)
    return message


# ─────────────────────────────────────────────
# PERIODIC #1 — complete past bookings
# ─────────────────────────────────────────────
@shared_task
def complete_past_bookings():
    """
    هر ۵ دقیقه اجرا می‌شود.
    Booking هایی که check_out آن‌ها گذشته و status=CONFIRMED
    به COMPLETED تغییر می‌کنند.
    """
    from .models import Booking
    from hotels.enums import BookingStatus

    today = timezone.now().date()

    qs = Booking.objects.filter(
        status=BookingStatus.CONFIRMED,
        check_out__lt=today,
    )

    count = qs.count()
    if count == 0:
        logger.info("[BEAT] No past bookings to complete.")
        return "no-op"

    for booking in qs:
        booking.status = BookingStatus.COMPLETED
        booking.save(update_fields=['status', 'updated_at'])
        send_booking_notification.delay(
            booking.id, booking.user_id, event='completed'
        )

    msg = f"[BEAT] Completed {count} past bookings."
    logger.info(msg)
    print(msg)
    return msg


# ─────────────────────────────────────────────
# PERIODIC #2 — cancel stale pending bookings
# ─────────────────────────────────────────────
@shared_task
def cancel_stale_pending_bookings():
    """
    هر ۱۰ دقیقه اجرا می‌شود.
    Booking هایی که بیش از ۳۰ دقیقه در status=PENDING مانده‌اند
    به CANCELLED تغییر می‌کنند.
    """
    from .models import Booking
    from hotels.enums import BookingStatus

    cutoff = timezone.now() - timedelta(minutes=30)
    qs = Booking.objects.filter(
        status=BookingStatus.PENDING,
        created_at__lt=cutoff,
    )

    count = qs.count()
    if count == 0:
        logger.info("[BEAT] No stale pending bookings.")
        return "no-op"

    for booking in qs:
        booking.status = BookingStatus.CANCELLED
        booking.save(update_fields=['status', 'updated_at'])
        send_booking_notification.delay(
            booking.id, booking.user_id, event='auto-cancelled'
        )

    msg = f"[BEAT] Cancelled {count} stale pending bookings."
    logger.info(msg)
    print(msg)
    return msg