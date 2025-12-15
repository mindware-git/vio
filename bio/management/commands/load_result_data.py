import json
from django.core.management.base import BaseCommand
from django.db import transaction
from bio.models import Person, LifeEvent


class Command(BaseCommand):
    help = "Load person data from result.json file into Django models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="result.json",
            help="Path to the result.json file (default: result.json)",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing person data instead of creating new",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        update_existing = options["update"]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON in {file_path}: {e}"))
            return

        with transaction.atomic():
            # Process Person data
            person_name = data.get("name")
            if not person_name:
                self.stdout.write(self.style.ERROR("No name found in the data"))
                return

            # Process occupation list to comma-separated string
            occupation_list = data.get("occupation", [])
            occupation_str = ",".join(occupation_list) if occupation_list else None

            # Get or create Person
            if update_existing:
                person, created = Person.objects.update_or_create(
                    name=person_name,
                    defaults={
                        "biography": data.get("biography", ""),
                        "birth_date": data.get("birth_date"),
                        "death_date": data.get("death_date"),
                        "occupation": occupation_str,
                        "nationality": data.get("nationality"),
                    },
                )
            else:
                person, created = Person.objects.get_or_create(
                    name=person_name,
                    defaults={
                        "biography": data.get("biography", ""),
                        "birth_date": data.get("birth_date"),
                        "death_date": data.get("death_date"),
                        "occupation": occupation_str,
                        "nationality": data.get("nationality"),
                    },
                )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created new person: {person_name}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Updated existing person: {person_name}")
                )

            # Delete existing life events if updating
            if update_existing:
                LifeEvent.objects.filter(person=person).delete()
                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted existing life events for {person_name}"
                    )
                )

            # Process Life Events
            life_events = data.get("life_events", [])
            events_created = 0

            for event_data in life_events:
                title = event_data.get("title")
                description = event_data.get("description")
                event_date = event_data.get("event_date")

                if not all([title, description, event_date]):
                    self.stdout.write(
                        self.style.WARNING(f"Skipping incomplete event: {title}")
                    )
                    continue

                try:
                    LifeEvent.objects.create(
                        person=person,
                        title=title,
                        description=description,
                        event_date=event_date,
                    )
                    events_created += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating event "{title}": {e}')
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully loaded data for {person_name}: "
                    f"{events_created} life events created"
                )
            )

        self.stdout.write(self.style.SUCCESS("Data loading completed successfully!"))
