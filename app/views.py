from flask import render_template, render_template, flash, request
from app import app
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .forms import BirthDateAgeForm


@app.route('/',  methods=['GET', 'POST'])
@app.route('/calendar',  methods=['GET', 'POST'])
def calendar():
    form = BirthDateAgeForm()
    if form.validate_on_submit():
        exp_age = int(form.expected_age.data) if form.expected_age.data else 90
        year, month, day = int(form.birth_year.data),  \
                           int(form.birth_month.data), \
                           int(form.birth_day.data)
        birth_date = datetime(year, month, day)
        life_months = get_months_of_life_list(exp_age, birth_date)
        months_of_life_calendar = get_months_of_life_calendar(life_months, 3) 
    else:
        exp_age = 90
        life_months = get_months_of_life_list(exp_age)
        months_of_life_calendar = get_months_of_life_calendar(life_months, 3)
    return render_template("calendar.html",
                           title='Calendar',
                           calendar=months_of_life_calendar,
                           form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

def group(iterable,n):
    n = 1 if n<=0 else n
    return [iterable[i:i + n] for i in range(0, len(iterable), n)]

def shift_month(date, n):
    mon_rel = relativedelta(months=n)
    return date+mon_rel

def get_months_of_life_list(expected_age, birth_date=None):
    months_of_life_list = []
    for n in range(expected_age*12):
        month = {}
        month['number'] = n
        if birth_date:
            month['start_date'] = shift_month(birth_date, n).date()
            month['end_date'] = shift_month(birth_date, n+1).date()
            month['is_past'] = True if month['end_date'] < datetime.now().date() else False
        else:
            month['start_date'] = None
            month['end_date'] = None
            month['is_past'] = False
        
        ### TODO
        # Брати інфу про події з бази
        # month['info'] = "info"
        ###

        months_of_life_list.append(month)
    return months_of_life_list

def get_months_of_life_calendar(months_of_life_list, n_years_in_row):
    grouped_life_months = group(months_of_life_list ,12*n_years_in_row)
    life_months_calendar = []
    for row in grouped_life_months:
        try:
            years = sorted(list({el['start_date'].year for el in row}))
            years_str = ','.join(str(year) for year in years)
            life_months_calendar.append([years_str, row])
        except AttributeError:
            life_months_calendar.append([None, row])
    return life_months_calendar
