import streamlit as st
from datetime import datetime, timedelta

# Add a logo from the local system at the top of the app
st.markdown('<div class="logo"><img src="https://raw.githubusercontent.com/Megha-mh/CT-registration-deadline-calculator/main/Full%20Logo%20(1).png" width="200"></div>', unsafe_allow_html=True)


# Custom CSS to add more space above the main heading, reduce header size, add borders, and make headings bold
st.markdown("""
    <style>
    h2 {
        font-size: 28px;
        margin-top: 40px; /* Increase space above the heading by 2cm */
    }
    h3 {
        font-size: 24px;
    }
    .box {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        white-space: pre-wrap; /* Preserve new lines */
    }
    .smaller-heading {
        font-size: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    /* Style the button */
    div.stButton > button {
        background-color: #2B547E; /* Professional dark blue color */
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #3C6E9C; /* Slightly lighter blue when hovered */
    }
    </style>
""", unsafe_allow_html=True)

# Title for the app
st.markdown("<h2>Corporate Tax Registration Deadline Calculator</h2>", unsafe_allow_html=True)

# Function to get the deadline based on the input date
def get_deadline_based_on_rules(input_date):
    month_day = (input_date.month, input_date.day)
    
    if (1, 1) <= month_day <= (2, 29):  # Jan 1 - Feb 29
        return "31 May 2024"
    elif (3, 1) <= month_day <= (4, 30):  # Mar 1 - Apr 30
        return "30 Jun 2024"
    elif (5, 1) <= month_day <= (5, 31):  # May 1 - May 31
        return "31 Jul 2024"
    elif (6, 1) <= month_day <= (6, 30):  # Jun 1 - Jun 30
        return "31 Aug 2024"
    elif (7, 1) <= month_day <= (7, 31):  # Jul 1 - Jul 31
        return "30 Sep 2024"
    elif (8, 1) <= month_day <= (9, 30):  # Aug 1 - Sep 30
        return "31 Oct 2024"
    elif (10, 1) <= month_day <= (11, 30):  # Oct 1 - Nov 30
        return "30 Nov 2024"
    elif (12, 1) <= month_day <= (12, 31):  # Dec 1 - Dec 31
        return "31 Dec 2024"
    return None

# Threshold for 90-day rule
threshold_date = datetime(2024, 3, 1).date()

# Step 1: Choose between the two options
option = st.radio("Choose an option:", ["Check Deadline Only", "Check Deadline and Get Template"])

# Step 2: Enter Trade License Issue Date
st.markdown('<div class="smaller-heading">Trade License Issue Date</div>', unsafe_allow_html=True)
date_input_str = st.text_input("Enter the Trade License Issue Date (DD-MM-YYYY or DD/MM/YYYY)", "")

# Check Deadline Only
if option == "Check Deadline Only":
    if date_input_str:
        try:
            # Replace slashes with dashes and parse the date
            date_input_str = date_input_str.replace("/", "-")
            input_date = datetime.strptime(date_input_str, "%d-%m-%Y").date()

            # Calculate deadline
            if input_date > threshold_date:
                calculated_date = input_date + timedelta(days=90)
            else:
                deadline = get_deadline_based_on_rules(input_date)
                if deadline:
                    calculated_date = datetime.strptime(deadline, "%d %b %Y").date()

            # Display the calculated deadline
            st.markdown(f"<h3>{calculated_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("Please enter a valid date in DD-MM-YYYY or DD/MM/YYYY format.")

# Check Deadline and Get Template
elif option == "Check Deadline and Get Template":
    # Step 3: Enter Company Name (only for this option)
    st.markdown('<div class="smaller-heading">Company Name</div>', unsafe_allow_html=True)
    company_name = st.text_input("Enter the Company Name")

    if date_input_str and company_name:
        try:
            # Replace slashes with dashes and parse the date
            date_input_str = date_input_str.replace("/", "-")
            input_date = datetime.strptime(date_input_str, "%d-%m-%Y").date()

            # Calculate deadline
            if input_date > threshold_date:
                calculated_date = input_date + timedelta(days=90)
            else:
                deadline = get_deadline_based_on_rules(input_date)
                if deadline:
                    calculated_date = datetime.strptime(deadline, "%d %b %Y").date()

            # Get the current date
            current_date = datetime.today().date()

            # Check if the calculated deadline is past the current date
            if calculated_date < current_date:
                # Inform the user that the registration is past due date
                st.markdown('<div class="box">The registration is past due date.</div>', unsafe_allow_html=True)
                
                # Button to show the template message
                if st.button("Get Template"):
                    message = f"""
Greetings {company_name} Team,

It has come to our notice that your license issue date is {input_date.strftime('%d/%m/%Y')} and the deadline for the license is {calculated_date.strftime('%d/%m/%Y')}. We regret to inform you that there is a chance of a late registration penalty of AED 10,000 imposed on the license.

Kindly confirm if we can proceed with the registration.

Thanks.
                    """
                    # Display the formatted message
                    st.text_area("Template Message", value=message, height=300)
            else:
                st.markdown('<div class="box">The registration is not past due date.</div>', unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter a valid date in DD-MM-YYYY or DD/MM/YYYY format.")
