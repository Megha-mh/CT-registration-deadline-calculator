import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for button styling and overall theme
st.markdown("""
    <style>
    h2 {font-size: 28px; color: #ff6347;}  /* Title styling */
    h3 {font-size: 24px; color: #4682B4;}  /* Subheading styling */
    .box {
        border: 2px solid #4682B4;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
        white-space: pre-wrap; /* Preserve new lines */
    }
    .smaller-heading {
        font-size: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #2e8b57;  /* Darker green for headings */
    }
    .stButton > button {
        background-color: #4682B4; /* Button background color */
        color: white;  /* Button text color */
        border-radius: 12px;
        border: 1px solid #2e8b57;  /* Button border */
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #2e8b57;  /* Hover color for button */
        color: #ffffff;
        border-color: #4682B4;
    }
    </style>
""", unsafe_allow_html=True)

# Title for the app
st.markdown("<h2>Corporate Tax Registration Deadline Calculator</h2>", unsafe_allow_html=True)

# Create two columns, giving more width to the second column
col1, col2 = st.columns([1, 2])  # Adjust ratio here (1:2 ratio)

# Date input widget in the first column with smaller heading
with col1:
    st.markdown('<div class="smaller-heading">Trade License Issue Date</div>', unsafe_allow_html=True)
    
    # Text input for manual date entry in DD-MM-YYYY or DD/MM/YYYY format
    date_input_str = st.text_input("Enter the Trade License Issue Date (DD-MM-YYYY or DD/MM/YYYY)", "")

    # If a date is manually typed, try to parse it
    if date_input_str:
        # Replace slashes with dashes to normalize the date format
        date_input_str = date_input_str.replace("/", "-")
        
        try:
            # Parse the manually entered date in DD-MM-YYYY format
            input_date = datetime.strptime(date_input_str, "%d-%m-%Y").date()
        except ValueError:
            st.error("Please enter a valid date in DD-MM-YYYY or DD/MM/YYYY format.")

# Input company name in the first column (after date input)
with col1:
    st.markdown('<div class="smaller-heading">Company Name</div>', unsafe_allow_html=True)
    company_name = st.text_input("Enter the Company Name")

# Function to get deadline based on the month and day (ignoring the year)
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

# Define the threshold date for 90-day rule
threshold_date = datetime(2024, 3, 1).date()

# Display the calculated date in the second column with smaller heading
with col2:
    st.markdown('<div class="smaller-heading">Deadline For Corporate Tax Registration</div>', unsafe_allow_html=True)
    
    if date_input_str and company_name:
        try:
            # If input date is after March 1, 2024, apply the 90-day rule
            if input_date > threshold_date:
                calculated_date = input_date + timedelta(days=90)
                st.markdown(f"<h3>{calculated_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)
            else:
                # Apply the table rules based on the month and day (ignoring the year)
                deadline = get_deadline_based_on_rules(input_date)
                if deadline:
                    calculated_date = datetime.strptime(deadline, "%d %b %Y").date()
                    st.markdown(f"<h3>{deadline}</h3>", unsafe_allow_html=True)
                else:
                    st.write("The selected date does not fall within the specified ranges.")
            
            # Get the current date
            current_date = datetime.today().date()
            
            # Check if the calculated deadline is past the current date
            if calculated_date < current_date:
                # Button to show the template message if the deadline has passed
                if st.button("Get Template"):
                    # Now generate the template message
                    st.markdown('<div class="smaller-heading">Template</div>', unsafe_allow_html=True)
                    
                    # Create the formatted message
                    message = f"""
I would like to bring to your attention that {company_name}, whose license was issued on {input_date.strftime('%d/%m/%Y')}, may potentially face a late registration penalty of AED 10,000.
                    
The deadline for registering licenses issued was {calculated_date.strftime('%d/%m/%Y')}, and it appears this deadline has been missed.
                    
We wanted to inform you in advance to avoid any surprises. If the penalty is imposed, the client will receive notification by both message and email, confirming the approval of the registration and the associated penalty.
                    
Please inform the client that there is no need to pay the penalty immediately, as it will not accumulate or increase. As discussed, we will be exploring the possibility of requesting a waiver for the penalty through the FTA, and we will keep you updated on any developments.
                    
Should you have any questions or need further clarification, please feel free to reach out.

Thank you for your cooperation.
                    """

                    # Display the formatted message using text_area for easy copying
                    st.text_area("Template Message", value=message, height=300)
            
            else:
                st.markdown('<div class="box">The registration is not past due date.</div>', unsafe_allow_html=True)
            
        except NameError:
            st.error("Please enter a valid date.")
