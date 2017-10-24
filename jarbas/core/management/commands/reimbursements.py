from jarbas.core.management.commands import LoadCommand
from jarbas.core.models import Reimbursement
from jarbas.core.tasks import start_reimbursements_import


class Command(LoadCommand):
    help = 'Load Serenata de Amor reimbursements dataset'

    def handle(self, *args, **options):
        self.path = options['dataset']

        if options.get('drop', False):
            self.drop_all(Reimbursement)

        start_reimbursements_import(self.path)
