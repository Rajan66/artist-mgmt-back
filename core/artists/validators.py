from datetime import datetime

from rest_framework.exceptions import ValidationError  # correct import


def validate_debut(first_release_year, dob):
    try:
        dob_obj = datetime.strptime(dob, "%m/%d/%Y").date()

        birth_year = dob_obj.year

        if int(first_release_year) < birth_year:
            raise ValidationError("Debut year cannot be less than your birth year.")

        age_at_debut = int(first_release_year) - birth_year

        if age_at_debut < 14:
            raise ValidationError("Artist should be at least 14 years old at debut.")
    except ValueError:
        raise ValidationError("Date of birth must be in YYYY-MM-DD format.")
