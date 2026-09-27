"""
Одноразовая команда миграции: перешифровывает Account.password
со старого ключа (SHA256(SECRET_KEY)) на новый, отдельный FERNET_KEY.

Использование:
    python manage.py rotate_fernet_key            # выполнить миграцию
    python manage.py rotate_fernet_key --dry-run   # только проверить, ничего не менять

ВАЖНО: перед запуском без --dry-run сделайте бэкап БД.

Технический момент: Account.objects (и даже .raw()/.values()) всегда
проходят через EncryptedField.from_db_value, который САМ пытается
расшифровать значение текущим (новым) ключом при любом ORM-доступе.
Поэтому единственный надёжный способ прочитать/записать по-настоящему
сырой (as-is) столбец — работать напрямую через connection.cursor(),
в обход дескриптора поля.
"""

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from apps.security.models import get_fernet, get_legacy_fernet

TABLE = 'security_account'


class Command(BaseCommand):
    help = (
        "Перешифровывает Account.password со старого ключа "
        "(SHA256(SECRET_KEY)) на новый отдельный FERNET_KEY."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать, что было бы сделано, но не сохранять изменения.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        legacy_fernet = get_legacy_fernet()
        new_fernet = get_fernet()

        migrated = 0
        already_new = 0
        failed = []

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT id, password FROM {TABLE}')
            rows = cursor.fetchall()

        self.stdout.write(f'Найдено {len(rows)} записей Account.')

        with transaction.atomic():
            for account_id, raw_value in rows:
                try:
                    # Уже читается новым ключом — ничего делать не нужно.
                    new_fernet.decrypt(raw_value.encode())
                    already_new += 1
                    continue
                except Exception:
                    pass

                try:
                    plaintext = legacy_fernet.decrypt(raw_value.encode()).decode()
                except Exception as exc:
                    failed.append((account_id, str(exc)))
                    continue

                new_encrypted = new_fernet.encrypt(plaintext.encode()).decode()
                migrated += 1
                self.stdout.write(f'  Account #{account_id}: legacy -> new key')

                if not dry_run:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f'UPDATE {TABLE} SET password = %s WHERE id = %s',
                            [new_encrypted, account_id],
                        )

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(self.style.SUCCESS(
            f'Готово. Перешифровано: {migrated}, уже на новом ключе: {already_new}, '
            f'ошибок: {len(failed)}.'
        ))
        if failed:
            self.stdout.write(self.style.ERROR(
                'Не удалось расшифровать ни старым, ни новым ключом (проверьте вручную):'
            ))
            for account_id, error in failed:
                self.stdout.write(f'  Account #{account_id}: {error}')
        if dry_run:
            self.stdout.write(self.style.WARNING(
                '--dry-run: изменения не сохранены.'
            ))
