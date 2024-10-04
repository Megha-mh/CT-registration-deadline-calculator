import streamlit as st
from datetime import datetime, timedelta

# Title for the app
st.title("Corporate Tax Registration Deadline Calculator")

# Create two columns
col1, col2 = st.columns(2)

# Date input widget in the first column with smaller heading
with col1:
    st.markdown("#### Trade License Issue Date")
    
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
    st.markdown("#### Deadline For Corporate Tax Registration")
    
    if date_input_str:
        try:
            # If input date is after March 1, 2024, apply the 90-day rule
            if input_date > threshold_date:
                calculated_date = input_date + timedelta(days=90)
                st.markdown(f"### {calculated_date.strftime('%B %d, %Y')}")
            else:
                # Apply the table rules based on the month and day (ignoring the year)
                deadline = get_deadline_based_on_rules(input_date)
                if deadline:
                    st.markdown(f"### {deadline}")
                else:
                    st.write("The selected date does not fall within the specified ranges.")
        except NameError:
            st.error("Please enter a valid date.")
