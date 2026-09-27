from django.core.management.base import BaseCommand

from api.models import KBEntry


class Command(BaseCommand):
    help = 'Seed the knowledge base with sample entries'

    def handle(self, *args, **options):
        entries = [
            {
                'question': 'What is a REST API?',
                'answer': 'A REST API is an HTTP-based interface that allows applications to communicate using resources and standard HTTP methods.',
                'category': 'api',
            },
            {
                'question': 'What is Django REST Framework?',
                'answer': 'Django REST Framework is a toolkit for building Web APIs with Django.',
                'category': 'framework',
            },
            {
                'question': 'How does JWT authentication work?',
                'answer': 'JWT authentication uses a signed token to securely identify an authenticated user when making API requests.',
                'category': 'api',
            },
            {
                'question': 'What is PostgreSQL?',
                'answer': 'PostgreSQL is an open-source relational database management system.',
                'category': 'database',
            },
            {
                'question': 'What is a database index?',
                'answer': 'A database index improves the speed of data retrieval operations on a table.',
                'category': 'database',
            },
            {
                'question': 'What is Docker?',
                'answer': 'Docker is a platform used to package and run applications in isolated containers.',
                'category': 'cloud',
            },
            {
                'question': 'What is Docker Compose?',
                'answer': 'Docker Compose is a tool for defining and running multi-container applications.',
                'category': 'cloud',
            },
            {
                'question': 'What is Django ORM?',
                'answer': 'Django ORM allows developers to interact with databases using Python objects instead of writing SQL directly.',
                'category': 'framework',
            },
            {
                'question': 'What is an API endpoint?',
                'answer': 'An API endpoint is a specific URL through which a client can access a particular API operation or resource.',
                'category': 'api',
            },
            {
                'question': 'What is a database transaction?',
                'answer': 'A database transaction groups multiple database operations into a single unit that can be committed or rolled back.',
                'category': 'database',
            },
            {
                'question': 'What is cloud computing?',
                'answer': 'Cloud computing provides computing resources such as servers, storage, and databases over the internet.',
                'category': 'cloud',
            },
            {
                'question': 'Why is API authentication important?',
                'answer': 'API authentication verifies the identity of clients before allowing access to protected resources.',
                'category': 'general',
            },
        ]

        created_count = 0

        for entry in entries:
            _, created = KBEntry.objects.get_or_create(
                question=entry['question'],
                defaults={
                    'answer': entry['answer'],
                    'category': entry['category'],
                },
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seed completed. {created_count} KB entries created.'
            )
        )