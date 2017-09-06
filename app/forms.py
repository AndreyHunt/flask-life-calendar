from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime


class BirthDateAgeForm(FlaskForm):
    birth_month = IntegerField("birth_month", 
        [
            DataRequired("Month of birth is required field")
        ])
    birth_day = IntegerField("birth_day", 
        [
            DataRequired("Day of birth is required field")
        ]) 
    birth_year = IntegerField("birth_year", 
        [
            DataRequired("Year of birth is required field"), 
            NumberRange(min=datetime.now().year-100, message="You can't be that old!"), 
            NumberRange(max=datetime.now().year, message="Are you from future?")
        ])
    expected_age = IntegerField("expected_age", 
        [
            Optional(), 
            NumberRange(min=1, max=100, message="Age have to be in range 1-100")
        ])


    def validate(self):
        #http://flask.pocoo.org/snippets/64/ - Complex Validation with Flask-WTF
        #https://stackoverflow.com/questions/21815067/how-do-i-validate-wtforms-fields-against-one-another
        if not FlaskForm.validate(self):
            return False    
        try:
            year, month, day = int(self.birth_year.data), int(self.birth_month.data), int(self.birth_day.data)
            birth_date = datetime(year, month, day)
        except ValueError:
            self.birth_day.errors.append('Incorrect date entered')
            return False
        return True