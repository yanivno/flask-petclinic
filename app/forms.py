from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from datetime import date


class OwnerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[DataRequired(), Length(max=80)])
    telephone = StringField('Telephone', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message='Telephone must be a 10 digit number')
    ])
    submit = SubmitField('Submit')


class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    type_id = SelectField('Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_birth_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('Birth date cannot be in the future')


class VisitForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add Visit')
