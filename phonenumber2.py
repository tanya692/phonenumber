pip install phonenumbers
import streamlit as st
import pandas as pd
import numpy as np
import phonenumbers
import base64
from io import BytesIO


number_country = "GB"  # Country of interest
testnumber = ('447654789001')
# Function which extracts numbers from a list containing strings
@st.cache
def extract_number_and_standardise(list_of_text, default_country):
    
    # Preconditions
    assert isinstance(list_of_text, list)
    
    national = list()       # List to store national version of number
    international = list()  # List to store international version of number
    e164 = list()           # List to store E164 version of number
    
    # Extract numbers in each string
    for t in list_of_text:
        number = phonenumbers.PhoneNumberMatcher(t, default_country)
       
        for n in number:
        
            # Standardise to national format
            national.append(phonenumbers.format_number(n.number, phonenumbers.PhoneNumberFormat.NATIONAL))
        
            # Standardise to international format
            international.append(phonenumbers.format_number(n.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        
            # Standardise to E164 format
            e164.append(phonenumbers.format_number(n.number, phonenumbers.PhoneNumberFormat.E164))
            
    
    return national, international, e164

# Function which checks if number is possible/valid for a given country
@st.cache
def number_check(numbers, country):
    
    # Preconditions
    assert type(numbers) == list
    assert type(country) == str
    
    # Empty dictionaries which will store check results
    possibility_results = dict()
    validity_results = dict()

    # Run through each number in the input list - check they are possible/valid numbers for the specified country
    for number in numbers:
    
        number_obj = phonenumbers.parse(number, country)                 # Convert number to a 'phone number object'
        
        possibility_check = phonenumbers.is_possible_number(number_obj)  # Determine if phone number object is possible
        
        possibility_results[number] = possibility_check                  # Append result of check to dictionary
    
    
        validity_check = phonenumbers.is_valid_number(number_obj)        # Determine if phone number object is valid
        
        validity_results[number] = validity_check                        # Append result of check to dictionary
        
        
    return possibility_results, validity_results
    # Function which implements validity check and outputs the valid/non-valid numbers separately
@st.cache
def valid_results(numbers, country):
        
    # Return dict of True/False values
    validity_results = number_check(numbers, country)[1]
    
    # Extract valid numbers
    valid_numbers = [k for k, v in validity_results.items() if v == True]
    
    # Extract non-valid numbers (so we can refer to them later)
    non_valid_numbers = [k for k, v in validity_results.items() if v == False]
    
            
    return valid_numbers, non_valid_numbers

# Function which takes in a phone number and country of origin, outputs standardised version of the number
@st.cache
def standardise_phonenumber(phone_no, default_country, no_format):
    
    """Standardise a single phonenumber."""



    try:
        # Converts input number to a PhoneNumber object
        number_obj = phonenumbers.parse(phone_no, default_country)
        
        # Standardises input number
        std_number = phonenumbers.format_number(number_obj, no_format)
        return std_number
    
    except:
        
        # If above steps do not work, return 'None'
        return None

# This function applies the 'standardise_phonenumber' function to a list of phone numbers
@st.cache
def standardise_list_phonenumbers(list_phone_numbers, default_country):
    
    """Standardise a list of phone numbers."""

    
    # Original format
    original_numbers = [s for s in list_phone_numbers]
    
    # Standardise to national format
    national_numbers = [standardise_phonenumber(s, default_country, phonenumbers.PhoneNumberFormat.NATIONAL) for s in list_phone_numbers]
    
    # Standardise to international format
    int_numbers = [standardise_phonenumber(s, default_country, phonenumbers.PhoneNumberFormat.INTERNATIONAL) for s in list_phone_numbers]
    
    # Standardise to E164 format
    e164_numbers = [standardise_phonenumber(s, default_country, phonenumbers.PhoneNumberFormat.E164) for s in list_phone_numbers]
        
    
    return original_numbers, national_numbers, int_numbers, e164_numbers

@st.cache
def regex_detect(text):
    
    # Import regular expression library
    import re
    
    # Precondition
    assert type(text) == list
    
    # Define empty list to store extracted numbers
    strings = list()
    
    # Walk through each string in list
    for list_element in text:
        
        # Extract number (returned as a list - use [0] to convert to string)
        numberfinder = re.findall(r"\W?\d{2,4}?\W?\d?\W?\d{2,3}?\s?\d{3}?\s?\d{4}?", list_element)[0]
        
        # Append extracted numbers to empty list
        strings.append(numberfinder)
        
    return strings

@st.cache
def regex_subs(format3_input_list):
    
    # Import regular expression library
    import re
    
    # Precondition
    assert type(format3_input_list) == list
    
    # Define empty list to store substituted numbers
    format4 = list()
    format5 = list()
    format6 = list()
    format7 = list()
    format8 = list()
    format9 = list()
    format10 = list()
    format11 = list()
    format12 = list()
    
    # Walk through each element in list to substitute format 4
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 4
        desiredformat4=re.sub(r"\W\d{2}","0",each_number)
        
        # Append newly formatted numbers to empty list
        format4.append(desiredformat4)
  
    # Walk through each element in list to substitute format 5
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 5
        desiredformat5=re.sub(r"\W\d{2}","0044",each_number)
        
        # Append newly formatted numbers to empty list
        format5.append(desiredformat5)
        
    # Walk through each element in list to substitute format 6
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 6
        desiredformat6=re.sub(r"\W\d{2}","+44",each_number)
        
        # Append newly formatted numbers to empty list
        format6.append(desiredformat6)
   
    # Walk through each element in list to substitute format 7
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 7
        desiredformat7=re.sub(r"\W\d{2}","44",each_number)
        
        # Append newly formatted numbers to empty list
        format7.append(desiredformat7)
  
    # Walk through each element in list to substitute format 8
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 8
        desiredformat8=re.sub(r"\W\d{2}","",each_number)
       
        # Append newly formatted numbers to empty list
        format8.append(desiredformat8)
    
        # Walk through each element in list to substitute format 8
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 8
        desiredformat9=re.sub(r"\W\d{2}","440",each_number)
       
        # Append newly formatted numbers to empty list
        format9.append(desiredformat9)
        
        # Walk through each element in list to substitute format 8
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 8
        desiredformat10=re.sub(r"\W\d{2}","00440",each_number)
       
        # Append newly formatted numbers to empty list
        format10.append(desiredformat10)
        
        # Walk through each element in list to substitute format 8
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 8
        desiredformat11=re.sub(r"\W\d{2}","004",each_number)
       
        # Append newly formatted numbers to empty list
        format11.append(desiredformat11)
    
        # Walk through each element in list to substitute format 8
    for each_number in format3_input_list:
        
        # Substitute exisiting prefix with prefix for format 8
        desiredformat12=re.sub(r"\W\d{2}","+440",each_number)
       
        # Append newly formatted numbers to empty list
        format12.append(desiredformat12)
    
    
    return format4,format5,format6,format7,format8,format9,format10,format11,format12
  
  # function that generates a unique ID code for uploaded data
def generate_id(s):
  
    return abs(hash(s)) % (10 ** 10)
  
    ##############################################################################
    

# Streamlit app
    

'''
# Standardising Phone Numbers

'''
st.write ('This tool is designed to  extract phone numbers froman excel document and validate and standardise them into a variety of formats that can then be passed through M*.')

st.write('The tool works by uploading the file (excel document) into the sidebar, that contains the numbers that need validating and standardising. You can then enter the name of the column that contains this data into the side bar.')

st.write('The tool works by extracting the number and then passing it through a standardising function that uses the phonenumbers library to give us a national, international and e164 formats of the extracted number.We then use two different functions that check whether these numbers are possible and valid depending on rules for phone numbers in the specified country, which in our case is Great Britain.')

st.write('Once the numbers have been validated, they are formatted into the variety of formats that are required and displayed in a data frame that is ready to download.')

st.sidebar.write('Upload Required File')
uploaded_file = st.sidebar.file_uploader(label="")

# Upload excel document
if uploaded_file is not None:
 
    with st.spinner('Uploading...'):

        df = pd.read_excel(uploaded_file,converters={'Original Number': lambda x: str(x)})
        df['ID'] = df['Original Number'].apply(generate_id)
        st.sidebar.success('File uploaded')
        st.write('Uploaded Data')
        st.dataframe(df)

        # Allow User to input the column name of the document they have uploaded that needs to be read
        user_input = st.sidebar.text_input("Please Enter Column Name", key=None)
       
        if len(user_input) >0:

            st.sidebar.success('Column Entered')
            
            # Convert text in uploaded dataframe to a list of strings
            imported_datalist = df[user_input].values.tolist()
            list_string = map(str, imported_datalist)
            list_string2 = list(list_string)
        
        # Standardise the list of phonenumbers
        function1 = standardise_list_phonenumbers(list_string2,number_country)
    
           
            # Check that the numbers are Valid numbers
        valid_numbers = valid_results(list_string2,number_country)[0]

        # Non-valid numbers
        non_valid_numbers = valid_results(list_string2, number_country)[1]


        # Test
        assert len(valid_numbers) + len(non_valid_numbers) == len(list_string2)

        # Raw version of number
        original = standardise_list_phonenumbers(valid_numbers, number_country)[0]

        # Number standardised to national format
        national = standardise_list_phonenumbers(valid_numbers, number_country)[1]

        # Number standardised to international format
        international = standardise_list_phonenumbers(valid_numbers, number_country)[2]

        # Number standardised to E164 format
        e164 =  standardise_list_phonenumbers(valid_numbers, number_country)[3]

        # Create a df containing the original number and the formats created by the phone numbers library
        block = pd.DataFrame({
                     'Original Number': original,
                     'Format 1': national,
                     'Format 2': international,
                     'Format 3': e164
                     })
       
        # Use the df created above to extract Format 3 into a list
        list_of_input_numbers = block['Format 3'].values.tolist()
        #Use the list created to call the regex sub function which allows us to output all of the other formats required
        newlyformattednumbers=regex_subs(list_of_input_numbers)

        # Standardised and Validated Phone Numbers
        '''
        ___
        ## Standardised and Validated Phone Numbers
        '''

        st.markdown("Phone Numbers in the original document are standardised, validated and formatted into the required formats")

        # Create a df that includes all possible formats
        mydf =(pd.DataFrame({
                    'Original Number': original,
                    'Format 1': national,
                    'Format 2': international,
                    'Format 3': e164,
                    'Format 4': newlyformattednumbers[0],
                    'Format 5': newlyformattednumbers[1],
                    'Format 6': newlyformattednumbers[2],
                    'Format 7': newlyformattednumbers[3],
                    'Format 8': newlyformattednumbers[4],
                    'Format 9': newlyformattednumbers[5],
                    'Format 10': newlyformattednumbers[6],
                    'Format 11': newlyformattednumbers[7],
                    'Format 12': newlyformattednumbers[8]
                    }))
        id = df['ID']
        newdf=pd.merge(left=df, right=mydf, how='outer', left_on='Original Number', right_on='Original Number')
        # Show the df on the output
        frame = newdf[['Original Number','ID','Format 1','Format 2','Format 3','Format 4','Format 5','Format 6','Format 7','Format 8','Format 9','Format 10','Format 11','Format 12']]
        st.write(frame)
    
        # Function that exports the df to an excel file
        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data
       
        # Function that generates a download link to to the excel file
        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            val = to_excel(df)
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download Excel File</a>'# decode b'abc' => abc

      # Button that allows us the user to download the excel file


        if st.button('Generate Download Link'):

            st.markdown(get_table_download_link(frame), unsafe_allow_html=True)

    # Add the different to formats to the original downloaded dataframe
        st.markdown("The different formats are added to the original document")
        frames = [df,frame]
        result = pd.merge(left=df, right=frame, how='outer', left_on='ID', right_on='ID')
        st.write (result)
 
        # Function that exports the df to an excel file
        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data
       
        # Function that generates a download link to to the excel file
        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            val = to_excel(df)
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download Excel File</a>'# decode b'abc' => abc

      # Button that allows us the user to download the excel file


        if st.button( 'Download Link'):

            st.markdown(get_table_download_link(result), unsafe_allow_html=True)
