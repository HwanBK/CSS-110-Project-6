# CSC 110
# Project 6
# Hwansu Kim (Billy)
# 11/03/21
# Program that displays potential mortgage options, based on user loan information, and lists monthly payments.


# Collects user loan info via inputs.
def inputLoanData():
    negativeLoan = True
    while negativeLoan:
        userLoanAmount = round(float(input("Enter home loan amount: ")), 2)

        if userLoanAmount > 0:
            negativeLoan = False
        else:
            print("Please enter a loan greater than zero.\n")

    negativeInterest = True
    while negativeInterest:
        userAnnualInterestRate = float(input("Enter annual interest rate: ")) / 100

        if userAnnualInterestRate > 0:
            negativeInterest = False
        else:
            print("Please enter an interest rate greater than zero.\n")

    return userLoanAmount, userAnnualInterestRate


# Displays term selection menu for the user.
def showMenu():
    userTermPeriod = -99
    while userTermPeriod == -99:
        print("-" * 43)
        print("  Mid-America Mortgage - Loan report menu")
        print("-" * 43)
        print("1. 15-year loan")
        print("2. 30-year loan")
        print("0. EXIT\n")

        userChoice = input("Choice: ")
        if userChoice == "1":
            userTermPeriod = 15

        elif userChoice == "2":
            userTermPeriod = 30

        elif userChoice == "0":
            userTermPeriod = 0

        else:
            userTermPeriod = -99
            print(userChoice, "is not a valid choice.\nPlease make a valid choice.\n")

    return userTermPeriod


# Calculates monthly payments based on user's info and selected term length.
def payment(loanPV, interestRate, numOfPeriods):
    monthlyPayment = round((interestRate / 12) * loanPV / (1 - (1 + (interestRate / 12)) ** -(numOfPeriods * 12)), 2)

    return monthlyPayment


# Displays a mortgage report with monthly breakdown and totals.
def showReport(loanPV, interestRate, numOfPeriods, paymentAmount):
    print("Pmt#", format("PmtAmt", ">12"), format("Int", ">12"), format("Princ", ">12"), format("Balance", ">12"))
    print("-" * 4, format("-" * 9, ">12"), format("-" * 5, ">12"), format("-" * 6, ">12"), format("-" * 8, ">12"))

    paymentCount = 1
    totalPayment = 0
    totalInterest = 0

    for month in range(1, (numOfPeriods * 12) + 1):
        interestAmount = round(loanPV * (interestRate / 12), 2)

        # Separate calculation for final term/month to ensure a final balance of 0.
        if month in range((numOfPeriods * 12), (numOfPeriods * 12) + 1):
            paymentAmount = round(loanPV + interestAmount, 2)

        principalAmount = round(paymentAmount - interestAmount, 2)
        loanPV = round(loanPV - principalAmount, 2)

        # If the loan balance is paid-off before the full term, stops payment for remaining terms.
        if loanPV < 0:
            paymentAmount = 0
            interestAmount = 0
            principalAmount = 0
            loanPV = 0

        print(format(paymentCount, ">4"), format(paymentAmount, ">12,.2f"), format(interestAmount, ">12,.2f"),\
              format(principalAmount, ">12,.2f"), format(loanPV, ">12,.2f"))

        if month in range(12, (numOfPeriods * 12), 12):
            print("-" * 56)

        totalPayment += paymentAmount
        totalInterest += interestAmount
        paymentCount += 1

    print("-" * 56, "\n")
    print("Total of payments: $", format(totalPayment, ">14,.2f"))
    print("Interest paid:     $", format(totalInterest, ">14,.2f"), "\n")
    input("Press <Enter> to continue")
    print()


def main():
    loanAmount, annualInterestRate = inputLoanData()

    termPeriod = -99
    while termPeriod != 0:
        termPeriod = showMenu()

        if termPeriod > 0:
            print()
            monthlyPayment = payment(loanAmount, annualInterestRate, termPeriod)
            showReport(loanAmount, annualInterestRate, termPeriod, monthlyPayment)


main()


# SUMMARY
#    I started this project by studying the call hierarchy of the project, as well as which functions needed loops and
# where in those functions the loops should be. After developing a mental outline of how each function will execute, I
# started coding the functions in the order of the call hierarchy; starting with inputLoanData and ending with
# showReport. I also tested each function separately, independent of the main function, to ensure they were returning
# the appropriate results when fed specific arguments and variables.
#    The most memorable instance of getting stuck would be with the showMenu function, as I had trouble deciding on
# the looping conditions; initially, I set the indefinite loop to continue based on the actual user input, 1, 2, and 0,
# but this caused the loop to not function properly at all. So, I changed the loop conditions to be based on the term
# length, based on the user's input; this resulted in proper looping, when inputs were not valid, and the loop being
# exited, when a valid input was provided.
#    I did most of my tests within a separate Python file or externally. For all math and calculations, I did testing
# with a calculator, to ensure my code was outputting the proper results. For the rest of the project, that did not
# handle calculations, I tested them by calling the functions independently and called them in a print statement to
# see exactly what the returns would be. One thing that doesn't work would be providing an interest of zero to the
# monthly payment calculation because it results in division by zero; mathematically, division by zero results in a DNE,
# but in reality an interest rate of zero can exist. I'd like to figure out how to work around the ZeroDivisionErrors.
#    This project was really good practice for writing definite and indefinite loops, but especially for writing loops
# that incorporated and relied on selection statements. As a result, the project really tested my ability to correctly
# set up loops, making sure the loop conditions I established actually resulted in proper looping. As for future
# projects, I'd like to take more time establishing appropriate looping conditions, before I commit them to code,
# because I definitely feel like I started writing the loops before fully fleshing them out.

# TEST CASES & CHANGES

# inputLoanData Function
#   -Only numerical values are valid.
#       -All values are converted to floating-point numbers for the userLoanAmount input. userAnnualInterestRate is not
#        rounded.
#           -All values are rounded to the nearest hundredth decimal point; nearest penny.
#   -String type values will cause a ValueError; strings cannot be converted to floats.
#       -Includes no inputs/blank space.
#   -Positive/negative value validation works as intended.
#       -Positive values progress the program to the next step.
#       -Negative values will return an error message/instructions to enter a positive value and will re-prompt the
#        user input.

# showMenu Function
#   -Only the three valid inputs, 1, 2, and 0, will work.
#       -The valid inputs will return the userTermPeriod variable and progress to the next function call.
#       -Invalid inputs will loop the showMenu function's display to re-prompt the user for a selection.
#           -Negative values
#           -Values in between 0 and 2 inclusive, but not 0, 1, or 2.
#               -1.2, 0.4, etc.

# payment Function
#   -Calculation tested externally, with a calculator, to ensure results are the same.
#       -Output also compared to project rubric's example output to ensure the results were the same when using the
#        same inputs.
#   -Cannot take in a interest rate of zero(0), will result in a ZeroDivisionError; i.e. cannot divide a number by 0.
#       -10 / 0 == DNE(Does not exist).

# showReport Function
#   -Initial working version properly output a report, but with issues.
#       -The final term did not completely pay off the loan balance.
#           -Created selection statements, for the 180th and 360th terms, based on the term's length; then, adjusted
#            the paymentAmount variable to compensate for any leftover balance on the final term. (OUTDATED)
#               -Separated the terms, since having a single selection statement check for 180 terms would incorrectly
#                pay off the entire loan on term 180 in a 30 year/360 term loan. (OUTDATED)
#                   -Changed this to work for ALL term lengths, even those not covered by the program, without coding
#                    for each term individually.
#                       -The final term always accounts for the leftover balance and changes the final month's payment
#                        and principal, so that the final balance is zero.
#       -Weird starting loan amounts and interest rates would result in odd reports; i.e. $1.00 loan with a 1% annual
#        interest rate.
#           -The above example would cause the loan to be paid off, before the full term length, which then caused the
#            loan balance to enter into negatives.
#               -Wrote code to stop payments if a payment would result in a negative balance; i.e. if the balance is 0,
#                monthly payment, interest, and principal would also all be 0.
#   -At the end of the program, when prompted to press ENTER, it does not matter if other characters are typed/input
#    prior to pressing ENTER; the input will have no effect on the program's functionality.
#   -Added a line of hyphens for every year's worth of terms, to increase readability.
#       -Initially coded incorrectly, would add a line of hyphens every 13 months after the first year.
#   -Tested with nice and easily calculated numbers, such as 100000, to ensure total payments and interest paid were
#    correct.
#   -Alignment will break with large numbers/digit counts.


# main Function
#   -Indefinite loop
#       -Term condition set to exit loop when the user's term number is 0; a result of the user choosing choice 0 during
#        the showMenu input.
#           -Properly loops between showMenu and showReport until choice 0 is chosen.
#       -Properly maintains returns from previous function calls, namely inputLoanData, until the loop ends.


