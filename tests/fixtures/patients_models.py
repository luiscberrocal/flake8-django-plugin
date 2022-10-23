from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel
from slugify import slugify

from .managers import PatientManager, InternmentManager
from .utils import hash_file_content
from ..core.models import Human, Auditable


class Patient(Auditable, Human):
    clinic = models.ForeignKey('clinics.Clinic', verbose_name=_('Clinic'),
                               on_delete=models.PROTECT, related_name='patients')
    email = models.EmailField(_('Email'), null=True, blank=True)
    active = models.BooleanField(_('Active'), default=True, help_text=_('Is the patient active?'))
    account_responsible = models.ForeignKey('self', verbose_name=_('Account responsible'),
                                            help_text=_('Person responsible for paying the bills'),
                                            null=True, blank=True, related_name='accountables',
                                            on_delete=models.SET_NULL)
    phone = models.CharField(_('Phone number'), max_length=30, null=True, blank=True)
    marital_status = models.CharField(_('Marital status'), max_length=15, null=True, blank=True)
    allergies = JSONField(_('Allergies'), null=True, blank=True)
    is_pensioned = models.BooleanField(_('Is pensioned'), default=False)
    is_retired = models.BooleanField(_('Is retired'), default=False)
    metadata = JSONField(_('Metadata'), null=True, blank=True)

    objects = PatientManager()

    def __str__(self):
        if self.middle_name is None:
            return '{}, {}'.format(self.last_name, self.first_name)
        else:
            return '{}, {} {}'.format(self.last_name, self.first_name, self.middle_name)

    class Meta:
        unique_together = ('national_id', 'country_for_id', 'clinic')
        ordering = ('last_name', 'first_name',)


class PatientContactInfo(TimeStampedModel):
    patient = models.ForeignKey(Patient, verbose_name=_('patient'), related_name='contact_infos',
                                on_delete=models.PROTECT)
    address = models.TextField(_('address'), null=True)
    email = models.EmailField(_('email'), null=True)
    primary_phone = models.CharField(_('primary phone'), max_length=20, null=True)
    secondary_phone = models.CharField(_('secondary phone'), max_length=20, null=True)


def path_and_rename(instance, filename):
    # FiXME This should include the clinic folder. Bug #89
    file_structure = dict()
    file_structure['extension'] = filename.split('.')[-1]
    file_structure['current_datetime'] = timezone.now().strftime('%Y%m%d_%H%M%S')
    file_structure['type'] = instance.type.lower()
    file_structure['patient'] = slugify('{}-{}-{}'.format(instance.patient.last_name,
                                                          instance.patient.first_name,
                                                          instance.patient.pk))
    filename = '{current_datetime}-{type}-{patient}.{extension}'.format(**file_structure)

    return filename


class UploadedFile(TimeStampedModel):
    LAB_RESULTS = 'LABS'
    EXAM_RESULTS = 'EXAMS'

    RESULTS_TYPES = (
        (LAB_RESULTS, _('Laboratories')),
        (EXAM_RESULTS, _('Exams')),
    )

    STARTED_STATUS = 'STARTED'
    UPLOADED_STATUS = 'UPLOADED'
    PROCESSING_STATUS = 'PROCESSING'
    PROCESSED_STATUS = 'PROCESSED'
    FAILED_STATUS = 'FAILED'

    STATUS_CHOICES = (
        (STARTED_STATUS, 'Started'),
        (UPLOADED_STATUS, 'Uploaded'),
        (PROCESSING_STATUS, 'Processing'),
        (PROCESSED_STATUS, 'Processed'),
        (FAILED_STATUS, 'Failed'),
    )
    file = models.FileField(upload_to=path_and_rename, blank=False, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    clinic = models.ForeignKey('clinics.Clinic', verbose_name=_('clinic'), on_delete=models.PROTECT, null=True)
    type = models.CharField(max_length=10, choices=RESULTS_TYPES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STARTED_STATUS)
    hash = models.CharField(max_length=128, null=True, help_text='SHA512 of file content', db_index=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        hash = hash_file_content(self.file.file)
        self.hash = hash
        return super(UploadedFile, self).save(force_insert, force_update, using, update_fields)


class Internment(Auditable, TimeStampedModel):
    patient = models.ForeignKey(Patient, verbose_name=_('patient'), on_delete=models.PROTECT,
                                related_name='internments')
    in_date = models.DateTimeField(_('internment date'))
    physician = models.ForeignKey('clinics.ClinicMember', verbose_name=_('physician'),
                                  null=True, blank=True, on_delete=models.SET_NULL, related_name='internments')
    facility = models.ForeignKey('clinics.CareTakingFacility', verbose_name=_('facility'),
                                 on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(_('room'), max_length=60, null=True, blank=True)

    out_date = models.DateTimeField(_('out date'), null=True, blank=True)
    comments = models.TextField(_('comments'), null=True, blank=True)
    display_order = models.IntegerField(_('Display Order'), default=0)

    objects = InternmentManager()


class InsuranceCompany(models.Model):
    name = models.CharField(_('name'), max_length=100)
    short_name = models.CharField(_('short name'), max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class InsurancePolicy(models.Model):
    insurance_company = models.ForeignKey(InsuranceCompany, verbose_name=_('insurance company'),
                                          related_name='policies', on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, verbose_name=_('patient'), related_name='policies', on_delete=models.PROTECT)
    number = models.CharField(_('number'), max_length=15)
