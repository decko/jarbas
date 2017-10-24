import csv
import lzma

from django.utils.timezone import now

from celery import shared_task

from jarbas.core.models import Reimbursement
from jarbas.core.management.commands import LoadCommand


def reimbursements(path):
    """Returns a Generator with a dict object for each row."""
    with lzma.open(path, mode='rt', encoding='utf-8') as file_handler:
        yield from csv.DictReader(file_handler)


@shared_task
def create_or_update(path):
    for count, row in enumerate(reimbursements(path), 1):
        create_or_update_reimbursement.delay(row)
        # print_count(Reimbursement, count=count)

    # print('{} reimbursements scheduled to creation/update'.format(count))
    #
    # TODO: Log all create_or_update operations


@shared_task
def mark_not_updated_reimbursements(nothing, started_at):
    qs = Reimbursement.objects.filter(last_update__lt=started_at)
    qs.update(available_in_latest_dataset=False)


@shared_task
def start_reimbursements_import(path):
    started_at = now()
    print("Reimbursement Job Queued!")

    chain = create_or_update.s(path) | mark_not_updated_reimbursements.s(started_at)

    chain()


@shared_task
def create_or_update_reimbursement(data):
    """
    :param data: (dict) reimbursement data (keys and data types must mach
    Reimbursement model)
    """
    serialized = serialize_reimbursement(data)
    kwargs = dict(document_id=serialized['document_id'], defaults=serialized)
    Reimbursement.objects.update_or_create(**kwargs)


def serialize_reimbursement(data):
    """Read the dict generated by DictReader and fix types"""

    missing = ('probability', 'suspicions')
    for key in missing:
        data[key] = None

    rename = (
        ('subquota_number', 'subquota_id'),
        ('reimbursement_value_total', 'total_reimbursement_value')
    )
    for old, new in rename:
        data[new] = data.pop(old)

    integers = (
        'applicant_id',
        'batch_number',
        'congressperson_document',
        'congressperson_id',
        'document_id',
        'document_type',
        'installment',
        'month',
        'subquota_group_id',
        'subquota_id',
        'term',
        'term_id',
        'year'
    )
    for key in integers:
        data[key] = LoadCommand.to_number(data[key], int)

    floats = (
        'document_value',
        'remark_value',
        'total_net_value',
        'total_reimbursement_value'
    )
    for key in floats:
        data[key] = LoadCommand.to_number(data[key])

    issue_date = LoadCommand.to_date(data['issue_date'])
    data['issue_date'] = issue_date.strftime('%Y-%m-%d')

    return data
