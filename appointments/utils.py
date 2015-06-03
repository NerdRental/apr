from appointments.models import Appointment
from appointments.emails import send_email_reminder


def send_period_reminders(event_ids, turn_off_reminders=False):
    """
    takes a Period object
    uses the Period to get appointments and then send reminders
    """
    appointments = Appointment.objects.filter(event__id__in=event_ids).exclude(no_reminders=True)

    if appointments:
        for appointment in appointments:
            if appointment.client.email:
                send_email_reminder(appointment)
                if turn_off_reminders:
                    appointment.no_reminders = True
                    appointment.save()
                if appointment.status != Appointment.CONFIRMED and appointment.status != Appointment.CANCELED:
                    appointment.status = Appointment.NOTIFIED
                    appointment.save()
