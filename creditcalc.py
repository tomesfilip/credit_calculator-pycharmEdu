import math
import sys
from optparse import OptionParser


def format_periods_count(periods):
    months = 0

    while periods % 12 != 0:
        periods -= 1
        months += 1

    years = int(periods / 12)
    if months == 0 and years > 0:
        print(f"It will take {years} years to repay this credit!")
    elif months != 0 and years > 0:
        print(f"it will take {years} years and {months} months to repay this credit!")
    else:
        print("Credit was already paid.")


def get_overpay(principal, monthly_pay, periods):
    total = math.ceil(monthly_pay * periods)
    return math.ceil(abs(principal - total))


def get_interest_rate(interest):
    return interest / 1200


# formula for calculating differentiate payment:
# D = P / n + i * (P - (P * (m - 1)) / n)
# [D] = differentiated payment; [P] = credit principal; [n] = number of payments (months, periods);
# [i] = nominal interest rate, usually 1/12 of the annual interest rate; [m] = current period;
def get_differentiate_payment(credit_principal, interest, periods):
    total = 0
    interest_rate = get_interest_rate(interest)
    before_brackets = credit_principal / periods
    for period in range(1, periods + 1):
        diff_pay = math.ceil(
            before_brackets + interest_rate * (credit_principal - (credit_principal * (period - 1) / periods)))
        print(f"Month {period}: payment is {diff_pay}")
        total += diff_pay

    overpay = math.ceil(abs(credit_principal - total))
    print()
    print(f"Overpayment = {overpay}")


# formula for calculating annuity payment:
# A = P * ((i * (1+i)^n) / ((1+i)^n - 1))
# [A] = annuity payment; [P] = loan principal;
# other variables are same as in the differentiate payment formula
def ann_monthly_pay(principal, periods, interest, payment):
    interest_rate = get_interest_rate(interest)
    if payment and periods and principal is None:
        x = math.pow((1 + interest_rate), periods)
        cred_principal = math.floor(payment / (interest_rate * x / (x - 1)))
        print(f"Your credit principal = {cred_principal}!")
        print(f"Overpayment = {get_overpay(cred_principal, payment, periods)}")
    elif payment and principal:
        months = math.ceil(math.log(payment / (payment - interest_rate * principal), 1 + interest_rate))
        format_periods_count(months)
        print(f"Overpayment = {get_overpay(principal, payment, months)}")
    else:
        x = math.pow((1 + interest_rate), periods)
        monthly_pay = math.ceil(principal * ((interest_rate * x) / (x - 1)))
        print(f"It will take = {monthly_pay}!")
        print(f"Overpayment = {get_overpay(principal, monthly_pay, periods)}")


# getting command-line arguments
args = sys.argv

# initializing new OptionParser object and adding new options to it
parser = OptionParser()

parser.add_option("--type",
                  action="store", type="string", dest="type")
parser.add_option("--principal",
                  action="store", type="int", dest="principal")
parser.add_option("--periods",
                  action="store", type="int", dest="periods")
parser.add_option("--interest",
                  action="store", type="float", dest="interest")
parser.add_option("--payment",
                  action="store", type="int", dest="payment")

if len(args) < 5:
    print("Incorrect parameters")
else:
    (options, args) = parser.parse_args()
    if options.type == "annuity" and options.interest is not None:
        ann_monthly_pay(options.principal, options.periods, options.interest, options.payment)
    elif options.type == "diff" and options.payment is None:
        get_differentiate_payment(options.principal, options.interest, options.periods)
    else:
        print("Incorrect parameters")
