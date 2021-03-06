from django.db import models
from senders.models import Sender
from accounts.models import Account
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import serializers
from django.core.exceptions import ValidationError
import datetime
from senders.models import Oauth2Token
from config import settings


class Event(models.Model):
    sender = models.ForeignKey(Sender, related_name='sender_events', on_delete=models.CASCADE)
    summary = models.CharField(max_length=254, blank=True, default='')
    description = models.TextField(blank=True, default='')
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    accounts = models.ManyToManyField(
        Account,
        verbose_name=_('accounts'),
        blank=True,
        help_text=_(
            'The accounts this event belongs to. A event will be sent to all accounts '
            'granted to each of their accounts.'
        ),
        related_name='event_set',
        related_query_name='account',
    )
    # calendar_id = models.CharField(max_length=1024, blank=True, default='')
    # calendar_event_id = models.CharField(max_length=1024, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{sender}: {start} - {end}: {summary}".format(
            sender=self.sender.email,
            start=self.start,
            end=self.end,
            summary=self.summary
        )

    class Meta:
        db_table = "events"
        ordering = ('start', 'end', 'sender')
        unique_together = ('id',)
        managed = True
    
    def clean(self):
        # Check oauth2 info of sender
        if not self.sender.google_oauth2_client_id:
            raise ValidationError({'sender': ['This sender don\'t include OAuth2 client id. Please add it into this sender.']})
        if not self.sender.google_oauth2_secrete:
            raise ValidationError({'sender': ['This sender don\'t include OAuth2 google oauth2_secrete. Please add it into this sender.']})
        # Check credentials
        oauth2token = Oauth2Token.objects.filter(sender_id=self.sender.id).first()
        credentials = None
        if oauth2token and oauth2token.text:
            credentials = oauth2token.text
        if not credentials:
            error_message = 'This sender {sender_email} don\'t have oauth2 access-token, yet. Please send this link {register_link} to the sender. So he can register with his google account, again.'.format(
                sender_email=self.sender.email,
                register_link=settings.REGISTER_URL
            )
            raise ValidationError({'sender': [error_message]})    
        # Check validations
        start_date = self.start
        end_date = self.end
        if end_date < start_date:
            raise ValidationError({'end': ['End date should be greater than start date.']})


class CalendarEvent(models.Model):
    calendar_event_id = models.CharField(max_length=1024, blank=False)
    event = models.ForeignKey(Event, related_name='calendar_event_events', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{caldendar_event_id}".format(
            caldendar_event_id=self.caldendar_event_id
        )

    class Meta:
        db_table = "calendar_event"
        ordering = ('created_at',)
        unique_together = ('id', 'calendar_event_id')
        managed = True

"""
Reminder model for event
"""
class Reminder(models.Model):
    event = models.OneToOneField(
        Event,
        # verbose_name=_('reminder'),
        related_name='reminder',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    useDefault = models.BooleanField(blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ''

    class Meta:
        ordering = ('created_at',)
        unique_together = ('event',)
        verbose_name = _("Reminder")
        verbose_name_plural = _("Reminders")
        managed = True


REMINDER_OVERRIDE_METHODS = (
    ('email', 'email'),
    ('popup', 'popup'),
    ('sms', 'sms'),
)

class OverrideManager(models.Manager):
    def get_queryset(self):
        return super(OverrideManager, self).get_queryset().filter(active=True)

class Override(models.Model):
    reminder = models.ForeignKey(Reminder, related_name='overrides', on_delete=models.CASCADE)
    method = models.CharField(max_length=5, blank=False, choices=REMINDER_OVERRIDE_METHODS)
    minutes = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(40320)])

    def __str__(self):
        return '{' + "'method':'{method}', 'minutes':{minutes}'".format(
                method=self.method,
                minutes=self.minutes
            ) + '}'

    class Meta:
        managed = True
        ordering = ('id',)
        # unique_together = ('id', )
        verbose_name = _("Override")
        verbose_name_plural = _("Overrides")


"""
Recurrence model for event
"""
RECURRENCE_RULES = (
    ('RRULE', 'RRULE'),
    ('EXRULE', 'EXRULE'),
    ('RDATE', 'RDATE'),
    ('EXDATE', 'EXDATE'),
)
RECURRENCE_FREQUENCES = (
    ('DAILY', 'days'),
    ('WEEKLY', 'weeks'),
    ('MONTHLY', 'monthds'),
    ('MONTHLY', 'years')
)
RECURRENCE_ENDS = (
    ('Never', 'Never'),
    ('On', 'On'),
    ('After', 'After')
)
def recurrence_json_2_string(obj):
    res = '{rule}'.format(rule=obj.rule)
    freq = ''
    ends = ''
    
    if obj.rule:
        res = '{rule}'.format(rule=obj.rule)
    else:
        res = 'RRULE'

    if obj.interval > 0:
        freq = 'FREQ={freq};INTERVAL={interval}'.format(
            freq=obj.freq, 
            interval=obj.interval
        )

    if obj.ends == 'On':
        ends = 'UNTIL={until}'.format(until=obj.until.strftime("%Y%m%dT%H%M%SZ"))

    if obj.ends == 'After':
        ends = 'COUNT={count}'.format(count=obj.count)

    if freq != '' or ends != '':
        res = res + ':'
        if freq != '':
            res = res + freq
        if ends !='':
            res = res + ';' + ends
    else :
        res = ''

    return res

def recurrence_dict_2_string(obj):
    res = ''
    freq = ''
    ends = ''

    if 'rule' in obj:
        res = '{rule}'.format(rule=obj['rule'])
    else:
        res = 'RRULE'
    
    if obj['interval'] > 0:
        freq = 'FREQ={freq};INTERVAL={interval}'.format(
            freq=obj['freq'], 
            interval=obj['interval']
        )

    if obj['ends'] == 'On':
        ends = 'UNTIL={until}'.format(until=obj['until'].strftime("%Y%m%dT%H%M%SZ"))

    if obj['ends'] == 'After':
        ends = 'COUNT={count}'.format(count=obj['count'])

    if freq != '' or ends != '':
        res = res + ':'
        if freq != '':
            res = res + freq
        if ends !='':
            res = res + ';' + ends
    else :
        res = None

    return res

class Recurrence(models.Model):
    event = models.ForeignKey(Event, related_name='recurrences', on_delete=models.CASCADE)
    rule = models.CharField(max_length=6, blank=False, choices=RECURRENCE_RULES, default='RRULE')
    freq = models.CharField(max_length=10, blank=False, choices=RECURRENCE_FREQUENCES, default='DAILY')
    count = models.IntegerField(blank=True, default=0)
    ends = models.CharField(max_length=10, blank=False, choices=RECURRENCE_ENDS, default='Never')
    until = models.DateField(blank=True, default=datetime.datetime.now)
    interval = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return recurrence_json_2_string(self)


    class Meta:
        ordering = ('created_at',)
        unique_together = ('id',)
        verbose_name = _("Recurrence")
        verbose_name_plural = _("Recurrences")
        managed = True