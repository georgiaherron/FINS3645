# Risk Profile | FINS3645 Project | T2 UNSW
# By: Georgia Herron | z5060047 | 22 Aug 21

# ************* PLEASE NOTE ****************

# This file is only a prototype of an additional model feature. It was not incorportated
# into my main files and model recommendations, as I did not have the time. 
# However, I believe it is a great addition to the product as it provides investor with
# easy access to a reputable risk tolerance questionarre resource that will inform them.
# The questions and scoring is taken directly from the reference listed below.
# Althought I created the Python code, I did not create the original questionarre questions;
# they were published by the following reputable source:
# PDD Wealth Management 2016, Risk Tolerance Assessment, PDD Wealth Management, viewed 20 August 2021,
# <https://www.pdd.com.au/sites/default/files/inline-files/Risk%20Tolerance%20Assessment_0.pdf>.
# Permission was not asked, however as it is only being seen by you, I hope you understand I 
# was simply trrying to communicate a concept; I hope this is acceptable.

# ************** START OF CODE **************

# Define the 7 individual questionarre questions
Q1 = "\n- - - - - - - - - -\n\nQ1. For how long would you expect most of your money to be invested before you would need to access it?\n1) Less than 12 months\n2) Between 1 and 3 years\n3) Between 3 and 5 years\n4) Between 5 and 7 years\n5) Longer than 7 years\n\nEnter your answer for Q1 (with an integer betwen 1-5): "

Q2 = "\nQ2. If you consider current interest rates what overall level of return (after inflation) do you reasonably expect to achieve from your investments over the period you wish to invest for?\n1) A reasonable return without losing any capital\n2) 1-3%\n3) 4-6%\n4) 7-9%\n5) Over 9%\n\nEnter your answer for Q2 (with an integer betwen 1-5): "

Q3 = "\nQ3. Assuming you had no need for capital, how long would you allow a poorly performing investment to continue before cashing it in (assuming the poor performance was mainly due to market influences)?\n1) Less than 1 year\n2) Up to 3 years\n3) Up to 5 years\n4) Up to 7 years\n5) Up to 10 years\n\nEnter your answer for Q3 (with an integer betwen 1-5): "

Q4 = "\nQ4. How familiar are you with investment markets?\n1) Very little understanding or interest\n2) Not very familiar\n3) Have had enough experience to understand the importance of diversification\n4) I understand that markets may fluctuate and that different market sectors offer different income, growth and taxation characteristics\n5) I am experienced with all investment classes and understand the various factors that may influence performance.\n\nEnter your answer for Q3 (with an integer betwen 1-5): "

Q5 = "\nQ5. There is generally a greater tax efficiency when investing in more volatile investments. With this in mind, which of the following would you be more comfortable with?\n1) Preferably guaranteed returns, ahead of tax-savings\n2) Stable, reliable returns with minimal tax savings\n3) Some variability in returns, some tax savings\n4) Moderate variability in returns, reasonable tax savings\n5) Higher variability but potentially higher returns, maximising tax savings\n\nEnter your answer for Q4 (with an integer betwen 1-5): "

Q6 = "\nQ6. What would your reaction be if six months after placing your investments, you discovered that due mainly to market conditions your portfolio had decreased in value by 20%?\n1) Horror – Security of your capital is critical and you do not intend to take risks.\n2) You would cut your losses and transfer your funds to more secure investment sectors.\n3) You would be concerned, but would wait to see if the investments improve.\n4) This was a risk you understood – you would leave your investments in place expecting\
performance to improve.\n5) You would invest more funds to take advantage of the lower unit/share prices expecting futuregrowth.\n\nEnter your answer for Q5 (with an integer betwen 1-5): "

Q7 = "\nQ7. Which of the following BEST describes your purpose for investing?\n1) You want to provide a regular income and/or totally protect the value of your investment capital.\n2) You have some specific objectives within the next 5 years for which you want to accumulate sufficient funds; AND/OR; You are nearing retirement and you are investing to ensure you have sufficient funds available to enjoy your retirement.\n3) You have a lump sum (eg inheritance or a superannuation rollover payment from your employer) and you are uncertain about what sort of investment alternatives are available.\n4) You are not nearing retirement, have surplus funds to invest and are aiming to accumulate long term wealth from a balanced portfolio.\n5) You have an investment time frame of over 5 years. You understand investment markets and are mainly investing for growth to accumulate long-term wealth, or are prepared to use aggressive investments to provide income.\n\nEnter your answer for Q7 (with an integer betwen 1-5): "

# Define the entire questionarre
questionarre = [Q1, Q2, Q3, Q4, Q5, Q6, Q7]

# Set the initial score and count to zero (for use in the following "for" loop)
score = 0
count = 0

# Calculate total questionarre score
for question in questionarre:
    print(question)
    answer = int(input())
    if answer < 6 and answer > 0:
       score = score + 10 * answer
       count = count + 1
    else:
      print("\nERROR. Please re-start the questionarre. Ensure you only enter valid integer numbers, between 1-5.\n")
      break

# Define risk profile function
def riskProfile(score):
    if score < 100:
        profile = print('\n=> Very Conservative “Cash” (0-100 Points)\n=> May be suitable for investors with a short-term investment horizon or a very low tolerance for risk, seeking a return similar to cash rates.\n=> Benchmark Asset Mix: 100% Cash\n')
    elif score < 141:
        profile = print('\n=> Conservative “Fixed Interest” (101-140 Points):\n=> May be suitable for investors with an investment horizon of at least 3 years and a low risk tolerance, seeking higher than cash returns over the investment timeframe.\n=> Benchmark Asset Mix: 100% Defensive\n')
    elif score < 171:
        profile = print('\n=> Moderately Conservative “Capital Stable” (141- 170 Points):\n=> May be suitable for investors with an investment horizon of at least 3 years and a low to moderate risk tolerance, seeking regular income and the opportunity for some growth over the investment timeframe.\n=> Benchmark Asset Mix: 70% Defensive, 30% Growth\n')
    elif score < 201:
        profile = print('\n=> Moderate “Conservative Growth” (171-200 Points)\n=> May be suitable for investors with an investment horizon of at least 3-5 years and a moderate risk tolerance, seeking a mix of income and growth over the investment timeframe from a well-diversified portfolio. This strategy suits investors aiming for a return higher than what is likely from a portfolio dominated by defensive assets but who want lower volatility than what a share fund would likely generate.\n=> Benchmark Asset Mix: 50% Defensive, 50% Growth\n')
    elif score < 251:
        profile = print('\n=> Assertive “Balanced” (201-250 Points)\n=> May be suitable for investors with an investment horizon of at least 5 years and a moderate risk tolerance, seeking more growth than income over the investment timeframe. This strategy suits investors aiming for a return higher than what is likely from a more defensive portfolio but who want lower volatility than what a share fund would likely generate.\n=> Benchmark Asset Mix: 30% Defensive 70% Growth\n')
    elif score < 301:
        profile = print('\n=> Moderately Aggressive “Growth” (251-300 Points)\n=> May be suitable for investors with an investment horizon of at least 5-7 years and a moderate to high risk tolerance, seeking a high exposure to growth assets.\n=> Benchmark Asset Mix: 15% Defensive, 85% Growth\n')
    elif score < 351:
        profile = print('\n=> Aggressive “Share” (301-350 Points)\n=> May be suitable for investors with an investment horizon of at least 7 years and high risk tolerance, comfortable with a share portfolio dominated by Australian and international shares.\n=> Benchmark Asset Mix: 100% Growth\n')
    else: 
      profile = print('Oops! You entered invalid input(s). Please try again!\n')
    return profile
# Returns: Client risk profile information [string]

# Call risk profile function when executed at run time & display information
if __name__ == "__main__":
  if count == 7:
    # Display calculated total score
    print("\n* * * * Summary of Your Estimated Risk Profile * * * *\n\nYour calculated risk tolerance score is", score)
    riskProfile(score)
    
    # Display additional notes and reference
    print("- - - - - - - - - - - - - -\n\nIMPORTANT NOTES\n\nNotes for Juraj Hric (FINS3645, UNSW):\nThis is purely an example of this feature for my model. I did not have time to integrate it into the model unfortunately, however I think it could be a great addition to the product. Please note that I have not asked permission to use this questionarre (the reference can be found at the bottom of this paragraph) as it is only for your eyes and this is simply an example to demonstrate how this feature would work.\n\nNotes for Flux clients:\n*Please be aware that this is simply OUR estimate of your risk profile; it is not to be taken as 100% accurate. Rather, our aim was to provide you with an informed estimate which can guide you to make your own decision.\n* We ask that you please do your own research and confirm the estimate for yourself. The risk level you select will have a large impact on your investment portfolio, so it is important to be sure of your response and know what the potential repercussions are.\n* For more information and educational resources, please refer to the Flux Dashboard, where you can review the resources we have provided; these will help you become educated on risk and accurately determine your Risk Tolerance.\n* If you are still unsure what your Risk Tolerance is after doing your own research, you can re-do this questionarre and compare your results.\n* It is important to review your Risk Tolerance periodically, as it will change over time; this is true for investors of all levels. The world is ever changing, and so are you; it\'s innevitable. It is your repsonsibility to keep your Risk Profile up-to-date. However, to help you remember, you can select the option to recieve periodic reminders from us.\n\n* We sourced our Risk Tolerance Questionarre questions from a reputable source: PDD Wealth Management 2016, Risk Tolerance Assessment, PDD Wealth Management, viewed 20 August 2021,<https://www.pdd.com.au/sites/default/files/inline-files/Risk%20Tolerance%20Assessment_0.pdf>.\n\n- - - - - - - - - - - - - -\n\nHappy Investing!\n\n- - - - - - - - - - - - - -\n")

# ************ END OF CODE **************
