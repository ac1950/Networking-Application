#Networking-Application/networking.py

import os
from dotenv import load_dotenv
import os
from datetime import datetime
#Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#Sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from gspread_formatting import *

### This is the most recent one without the templates tho! FUCK


### Formatting Definitions - use any of these for the last parameter in the 'format_cell_range() function' 
# detailed notes found here: https://pypi.org/project/gspread-formatting/    https://stackoverflow.com/questions/54179490/gspread-how-to-change-the-color-of-an-entire-row

format_header = cellFormat(
    backgroundColor = color(204, 204, 204),
    textFormat =textFormat(bold=True, foregroundColor=color(59, 117, 203)) , 
    horizontalAlignment = 'CENTER'
)

def print_headers(rows,sheet):
    if len(rows) >= 1:
        print("No Header Printed")
    else: 
        row = ["Company", "First Name", "Last Name" , "Email", "Phone Number", "Where we met?", "Notes", "Date Added", "Date of last Contact", "2nd Most Recent Date of Contact", "Date of Last Push Notification Sent"]
        index = 1
        sheet.insert_row(row,index)
        format_cell_range(sheet, 'A1:K1', format_header)
        #gspread_formatting(sheet, 'A1:K1' , format_header)
        set_row_height(sheet, '1', 77)
        set_column_width(sheet, 'A:K', 240)
        set_frozen(sheet, rows = 1)






def get_company():
    company = input("Please input a company\n")
    while True:
        if company == "":
            print("Please input a company please")
        else:
            break
    return company
def get_first_name():
    while True:
        first_name = input("Please input the first name\n")
        if first_name == "":
            print("Please input a first name please\n")
        else:
            break
    return first_name
def get_last_name():
    last_name = input("Please input the last name\n")
    while True:
        if last_name == "":
            print("Please input a last name please\n")
        else:
            break
    return last_name
def get_email():
    email = input("Please input email. For example in form 'example@gmail.com'\n")
    return email
def get_phone_number():
    
    phone_number = input("Please input your phone number\n")
    return phone_number
def get_where_we_met():
    where_we_met = input("Where did you meet this contact?\n")
    return where_we_met
def get_notes():
    notes = input("Please input any additional notes you had on this contact\n")
    return notes
def get_date_added():
    today = datetime.today()
    d3 = today.strftime("%m/%d/%y")
    return d3
def get_date_last_contacted():
    today = datetime.today()
    date_last_contacted = today.strftime("%m/%d/%y")
    return date_last_contacted
def get_second_most_recent_date():
    return ""
def get_date_of_last_notification():
    today = datetime.today()
    date_of_last_notification = today.strftime("%m/%d/%y")
    return date_of_last_notification
def create_contact(company, first_name, last_name, email, phone_number,  where_we_met, notes, date_added, date_last_contacted, second_most_recent_date, date_of_last_notification):
    dictionary = {"company":company,"first_name": first_name , 
    "last_name" : last_name , "email" : email , "phone_number" : phone_number, "where_we_met": where_we_met, 
    "notes": notes, "date_added": date_added, "date_last_contacted" : date_last_contacted, "second_most_recent_date": second_most_recent_date, 
    "date_of_last_notification" : date_of_last_notification}
    return dictionary
def reading_from_sheet(doc,rows):
    #
    # READ SHEET VALUES
    #

    print("-----------------")
    print("SPREADSHEET:", doc.title)
    print("-----------------")
    x = 1
    for row in rows:
        print(x,"-" ,row) #> <class 'dict'>
        print(" ")
        x += 1
def writing_to_sheet(info,sheet,rows):
    next_id = len(rows) + 1 # TODO: should change this to be one greater than the current maximum id value
    
    next_row = list(info.values())#> [13, 'Product 13', 'snacks', 4.99, '2019-01-01']

    next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

    response = sheet.insert_row(next_row, next_row_number)

    print("-----------------")
    print("NEW RECORD:")
    print(next_row)
    print("-----------------")
    print("RESPONSE:")
    print(type(response)) #> dict
    print(response) #> {'spreadsheetId': '___', 'updatedRange': '___', 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}
def send_email(subject="[Daily Briefing] This is a test", html="<p>Hello World</p>"):
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)
    message = Mail(from_email=MY_EMAIL, to_emails=MY_EMAIL, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", e.message)
        return None




if __name__ == "__main__":
    #
    # AUTHORIZATION for google sheets and sendgrid
    #



### if cell in sheet ("Personal information") is blank then prompt for this, if not -

   #     first_nameinput = input("What is your first name, as you would like to be known by to recruiters?")
   #     last_name = input("What is your last name?")
   #     university = input("What University do you go to. Ex. 'Georgetown University' ")
   #     majors = input("What majors are you currently pursuing. Ex. Finance and Operations and Information Management ")
   #     classYear = input("What year are you? Ex. Sophomore")
#
#
#




    CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "google_api_credentials.json")

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
    
    load_dotenv()

    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
    SHEET_NAME = os.environ.get("SHEET_NAME", "Products")
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MY_EMAIL = os.environ.get("MY_EMAIL_ADDRESS")

    while True:
        print("\n Hi, this is Donnie Azoff, your Networking Virtual Assistant, how may I help you today?\n")
        choice = input("Enter 1 to input new contact information, Enter 2 to Read your contact information, Enter 3 to receive suggestions, Enter 4 to edit basic information, Enter 5 to Quit \n")
        
        if choice == "1":

            client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
            doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
            sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
            rows = sheet.get_all_records() #> <class 'list'>

            print_headers(rows,sheet)

            
            
            while True:
                #Sheets refresh stuff
                client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
                doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
                sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
                rows = sheet.get_all_records() #> <class 'list'>

                company = get_company()
                first_name = get_first_name()
                last_name = get_last_name()
                email = get_email()
                phone_number = get_phone_number()
                where_we_met = get_where_we_met()
                notes = get_notes()
                date_added = get_date_added()
                date_last_contacted = get_date_last_contacted()
                second_most_recent_date = get_second_most_recent_date()
                date_of_last_notification = get_date_of_last_notification()
            
                
                contact = create_contact(company, first_name, last_name, email, phone_number, where_we_met, notes, 
                date_added,date_last_contacted, second_most_recent_date, date_of_last_notification)

                networking_contacts = []
                networking_contacts.append(contact) # Appends contact to list (dictionary to list)
                #print(networking_contacts[0]["phone_number"]) # should print phone number
                info = networking_contacts[0]
                writing_to_sheet(info,sheet,rows)

                repeat_1 = input("\nWould you like to input another contact? Enter 1 if yes, Enter 0 if no\n")
                if repeat_1 == "1":
                    print("ok")
                elif repeat_1 == "0":
                    break
                elif (repeat_1 != "1","0"):
                    print("Invalid Choice")
                    break


        if choice == "2":
            client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
            doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
            sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
            rows = sheet.get_all_records() #> <class 'list'>
            
            reading_from_sheet(doc, rows)

        if choice == "3":
            
            example_subject = "[Daily Briefing] This is a test"
            example_html = f"""
            <h3>This is a test of the Daily Briefing Service</h3>

            <h4>Today's Date</h4>
            <p>Monday, January 1, 2040</p>

            <h4>My Stocks</h4>
            <ul>
                <li>MSFT | +04%</li>
                <li>WORK | +20%</li>
                <li>ZM | +44%</li>
            </ul>

            <h4>My Forecast</h4>
            <ul>
                <li>10:00 AM | 65 DEGREES | CLEAR SKIES</li>
                <li>01:00 PM | 70 DEGREES | CLEAR SKIES</li>
                <li>04:00 PM | 75 DEGREES | CLEAR SKIES</li>
                <li>07:00 PM | 67 DEGREES | PARTLY CLOUDY</li>
                <li>10:00 PM | 56 DEGREES | CLEAR SKIES</li>
            </ul>
            """
            send_email(example_subject, example_html)
        
            break

        if choice == "4": 
            print("Here's the basic information we have for you!:")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Place of Study: {university}")
            print(f"Year: {classYear}")
            decision = input("Are you sure you want to edit your response? - (y/n)")
            while decision != "y" or decision != "n":
                decision = input("Are you sure you want to edit your response? - (y/n)")
            if decision  == "n":
                print("Okay!")
                break
            if decision == "y":
                first_nameinput = input("What is your first name, as you would like to be known by to recruiters?")
                last_name = input("What is your last name?")
                university = input("What University do you go to. Ex. 'Georgetown University' ")
                majors = input("What majors are you currently pursuing. Ex. Finance and Operations and Information Management ")
                classYear = input("What year are you? Ex. Sophomore")

                print("Here are your updated responses: ")
                print("Here's the basic information we have for you!:")
                print(f"First Name: {first_name}")
                print(f"Last Name: {last_name}")
                print(f"Place of Study: {university}")
                print(f"Year: {classYear}")






            
        if choice == "5":
            print("Quitting...")
            break

    #TODO: Alex write and find skeleton emails and code?
    #TODO: Pytest
    #TODO: Check if requirement.txt is good
    #TODO: Fill out the README File


    #TODO:  Option to send intro email template after creating a contact
     
    #TODO: Fix Suggestions option by 1. Showing all contacts 2. Giving you the option of selecting them and giving important info like "notes" and "where we met" --> Reccomendations

    # Suggestions
        # - Introductory
        # - Cold email(It would fill in the template with the information in the contacts)
        # - Update to network
            # - Academic Performance
            # - Internships offer
        # - Thank you note
            # - Interview followup
            # - Networking event
            # - Coffee Chat 
            # - Introduction email via contact(Thank you for introducing me to blah blah blah)
            
    # Automated Email Notification(Heroku)
        # Let person know to update last contacted on sheets

    #TODO: Prompt to ask for more information to fill in email(Later goal)
    #TODO:  #contact added									
                #1	Add today's date to date added and copy that date to date last contacted (highlight this yellow) and copy also to date of last push notification sent for heroku to base off of								
                #2	After threshold -> push over date last contacted to second most recent date of contact (keep formatting)								
                #3	add today's date to date of last push notification sent and to date last contacted (highlight this)								
                #4	new date of last push notifaction sent is threshold								
									
    #TODO:  Fix Headers, Templates(Option 3), Heroku
    #TODO:  
    #TODO:  
    #TODO:  
    #TODO:  


  
"""
Dear name:

I hope this email finds you well!

My name is (me); I'm a {year}} at Georgetown's McDonough School of Business studying {major/majors}. {reccommender}} recommended that I reach out to you to learn a bit more about {firm"}.

If you have some time, I would love to chat and gain your perspective on your group and the firm overall. Would you have any availability in the coming weeks?

I've also attached my resume below, should it be of use!

Thank you for your time, I look forward to hearing from you!

Best,

{name}


Dear Chris,

My name is {name}}; I'm a {year}} at Georgetown's McDonough School of Business studying {major/majors}. 
I just wanted to thank you for taking the time to talk to me at {EVENT}}. 
I enjoyed learning about your experience at {Firm}. I would love to hear more about your experience at Perella. If you have time to talk later in the week so I can ask more about the firm, I would greatly appreciate it.

Best,
Patrick


"""




