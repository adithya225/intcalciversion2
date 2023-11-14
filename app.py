import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Initialize history and summation variables
history = []
summation = 0

def total_days(s_date,e_date):
    start_date = list(map(int, s_date.split('-')))
    end_date = list(map(int, e_date.split('-')))
    print(start_date)
    print(end_date)
    sy, sm, sd = start_date[0], start_date[1], start_date[2]
    ey, em, ed = end_date[0], end_date[1], end_date[2]
    if ed<sd:
        ed1=ed+30
        em1=em-1
        days=ed1-sd
        if em1<sm:
            em2=em1+12
            ey1=ey-1
            months=em2-sm
            if ey1<sy:
                print("please check your values")
            else:
                years=ey1-sy
        else:
            months=em1-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy
    else:
        days=ed-sd
        if em<sm:
            em3=em+12
            ey2=ey-1
            months=em3-sm
            if ey2<sy:
                print("please check your details")
            else:
                years=ey2-sy
        else:
            months=em-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy

    td=days+(months*30)
    td1=td+(years*360)
    return td1
def c_interest(p,r,s_date,e_date):
    rt=(r*12)/100
    start_date = list(map(int, s_date.split('-')))
    end_date = list(map(int, e_date.split('-')))
    print(start_date,end_date)
    sy, sm, sd = start_date[0], start_date[1], start_date[2]
    ey, em, ed = end_date[0], end_date[1], end_date[2]
    if ed<sd:
        ed1=ed+30
        em1=em-1
        days=ed1-sd
        if em1<sm:
            em2=em1+12
            ey1=ey-1
            months=em2-sm
            if ey1<sy:
                print("please check your values")
            else:
                years=ey1-sy
        else:
            months=em1-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy
    else:
        days=ed-sd
        if em<sm:
            em3=em+12
            ey2=ey-1
            months=em3-sm
            if ey2<sy:
                print("please check your details")
            else:
                years=ey2-sy
        else:
            months=em-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy


    td=days+(months*30)
    td1=td+(years*360)
    t=td1/360

    i1 = (p*(1+rt)**(int(t))) - p
    p1 = i1 + p
    i2 = (p1*rt*(t-int(t))) + p1
    return i2
def s_interest(principle, r, s_date, e_date):
    rt=(r*12)/100
    start_date = list(map(int, s_date.split('-')))
    end_date = list(map(int, e_date.split('-')))
    sy, sm, sd = start_date[0], start_date[1], start_date[2]
    ey, em, ed = end_date[0], end_date[1], end_date[2]
    if ed < sd:
        ed1 = ed + 30
        em1 = em - 1
        days = ed1 - sd
        if em1 < sm:
            em2 = em1 + 12
            ey1 = ey - 1
            months = em2 - sm
            if ey1 < sy:
                print("please check your values")
            else:
                years = ey1 - sy
        else:
            months = em1 - sm
            if ey < sy:
                print("please check your values")
            else:
                years = ey - sy
    else:
        days = ed - sd
        if em < sm:
            em3 = em + 12
            ey2 = ey - 1
            months = em3 - sm
            if ey2 < sy:
                print("please check your details")
            else:
                years = ey2 - sy
        else:
            months = em - sm
            if ey < sy:
                print("please check your values")
            else:
                years = ey - sy

    td = days + (months * 30)
    td1 = td + (years * 360)
    t = td1 / 360

    interest = principle*t*rt
    return interest

c_model = c_interest
s_model = s_interest

@app.route('/')
def home():
    return render_template('index3.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [str(x) for x in request.form.values()]
    p = int(features[0])
    r = float(features[1])
    s_date = str(features[2])
    e_date = str(features[3])

    # Perform calculations
    c_prediction = c_model(p, r, s_date, e_date)
    s_prediction = s_model(p, r, s_date, e_date)
    days = total_days(s_date, e_date)

    # Update history and summation
    global history, summation
    history.append({
        'principle': p,
        'rate': r,
        'start_date': s_date,
        'end_date': e_date,
        'c_interest': c_prediction,
        's_interest': s_prediction,
        'total_days': days
    })
    summation += c_prediction  # You can choose to use s_prediction or both if needed

    out1 = [p, r, s_date, e_date, days, round(s_prediction, 0), round(s_prediction + p, 0), round(c_prediction - p, 0), round(c_prediction, 0)]

    s1 = "1) Principle Amount is: {0}".format(out1[0])
    s2 = "2) Rate of Interest is: {0} x 12 %".format(out1[1])
    s3 = "3) Start Date: {0}".format(out1[2])
    s4 = "4) End Date: {0}".format(out1[3])
    s5 = "5) Total Number of Days is:  {0}".format(out1[4])
    s6 = "6) Interest for the Amount with respect to SI is: {0}".format(out1[5])
    s7 = "7) Final Amount with respect to SI is: {}".format(out1[6])
    s8 = "8) Interest for the Amount with respect to CI is: {}".format(out1[7])
    s9 = "9) Final Amount with respect to CI is: {}".format(out1[8])

    # Format output for display
    out2 = {
        'principle': s1,
        'rate': s2,
        'start': s3,
        'end': s4,
        'total_days': s5,
        's_interest': s6,
        'final_s_amount': s7,
        'c_interest': s8,
        'final_c_amount': s9
    }

    return render_template('index3.html', prediction_text=out2, history=history, summation=summation)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    # Reset history and summation
    global history, summation
    history = []
    summation = 0
    return render_template('index3.html', prediction_text=None, history=history, summation=summation)

if __name__ == "__main__":
    app.run(debug=True)
