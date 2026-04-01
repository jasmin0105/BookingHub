from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_booking_confirmation(booking):
    """Отправляет подтверждение бронирования пользователю"""
    item_name = (
        booking.hotel.name if booking.hotel else
        booking.restaurant.name if booking.restaurant else
        booking.event.name if booking.event else f"Booking #{booking.id}"
    )
    ref = f"BH-{str(booking.id).zfill(6)}"

    subject = f"✅ Booking Confirmed — {item_name} | {ref}"

    message = f"""
Dear {booking.user.username},

Your booking has been confirmed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOOKING CONFIRMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference:    {ref}
Property:     {item_name}
Type:         {booking.booking_type.capitalize()}
Guests:       {booking.guests}
Total Price:  ${booking.total_price}
Status:       Confirmed
{"Check-in:    " + str(booking.check_in) if booking.check_in else ""}
{"Check-out:   " + str(booking.check_out) if booking.check_out else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for choosing BookingHub!
For support: support@bookinghub.com

BookingHub — Diploma Project
Yusupova Zhasmin, COM-22
Ala-Too International University
"""

    send_mail(
        subject=subject,
        message=message,
        from_email='BookingHub <noreply@bookinghub.com>',
        recipient_list=[booking.user.email],
        fail_silently=True,
    )


def send_booking_cancelled(booking):
    """Отправляет уведомление об отмене"""
    item_name = (
        booking.hotel.name if booking.hotel else
        booking.restaurant.name if booking.restaurant else
        booking.event.name if booking.event else f"Booking #{booking.id}"
    )
    ref = f"BH-{str(booking.id).zfill(6)}"

    subject = f"❌ Booking Cancelled — {item_name} | {ref}"

    message = f"""
Dear {booking.user.username},

Your booking has been cancelled.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANCELLATION NOTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference:    {ref}
Property:     {item_name}
Status:       Cancelled
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you did not request this cancellation,
please contact us at support@bookinghub.com

BookingHub Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email='BookingHub <noreply@bookinghub.com>',
        recipient_list=[booking.user.email],
        fail_silently=True,
    )


def send_owner_notification(booking):
    """Уведомляет владельца объекта о новой брони"""
    owner = (
        booking.hotel.owner if booking.hotel and booking.hotel.owner else
        booking.restaurant.owner if booking.restaurant and booking.restaurant.owner else
        booking.event.owner if booking.event and booking.event.owner else None
    )
    if not owner or not owner.email:
        return

    item_name = (
        booking.hotel.name if booking.hotel else
        booking.restaurant.name if booking.restaurant else
        booking.event.name if booking.event else "Your property"
    )
    ref = f"BH-{str(booking.id).zfill(6)}"

    subject = f"🏨 New Booking for {item_name} | {ref}"

    message = f"""
Dear {owner.username},

You have a new booking!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW BOOKING NOTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference:    {ref}
Property:     {item_name}
Guest:        {booking.user.username} ({booking.user.email})
Guests:       {booking.guests}
Total:        ${booking.total_price}
{"Check-in:    " + str(booking.check_in) if booking.check_in else ""}
{"Check-out:   " + str(booking.check_out) if booking.check_out else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View your dashboard: http://localhost:5173/dashboard

BookingHub Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email='BookingHub <noreply@bookinghub.com>',
        recipient_list=[owner.email],
        fail_silently=True,
    )
