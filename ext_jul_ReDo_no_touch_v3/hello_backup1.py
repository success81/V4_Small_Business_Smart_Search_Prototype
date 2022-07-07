####JUL2022###
#Libraries
from flask import Flask, render_template, request
app = Flask(__name__)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import csv
import re
import math
from collections import Counter
import string

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():

    #lower and tokenize words

    #Creating punctuation stop list
    punct =  set(string.punctuation)

    my_stopwords = set(stopwords.words('english'))
    #print (word_tokenize(test_text))



    #Combining stopwords with puntuations
    my_stopwords |= punct

    #Jaccards Similarity Function
    def jaccard_similarity(list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return float(len(s1.intersection(s2)) / len(s1.union(s2)))

    #Function for lowering and removing
    def lowerandremove(x):
        blank_string = ""
        lower_temp = x.lower()
        tokens = word_tokenize(lower_temp)
        for x in tokens:
            if x not in my_stopwords:
                blank_string += " "
                blank_string += x
        return blank_string



    #Cosine Functions
    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator


    def text_to_vector(text):
        word = re.compile(r'\w+')
        words = word.findall(text)
        return Counter(words)

    ######Main Cosine Function#####
    def cosine(content_a, content_b):
        text1 = content_a
        text2 = content_b

        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        cosine_result = get_cosine(vector1, vector2)
        return cosine_result

    #CSV File
    #Importing excel
    filename = "big_cosine_mod_f.csv"


    #Setting up lists for csv
    Fields = []
    rows = []

    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
         
        # extracting field names through first row
        fields = next(csvreader)
     
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    #Lower and Tokenize words then remove
    master_temp_rows = []
    temp_rows = []

    #Iterating through rows and adding new lowered and tokenized text fields
    for x in rows:
        temp_rows.append(x[0])
        temp_rows.append(x[1])
        temp_rows.append(x[2])
        temp_rows.append(x[3])
        temp_rows.append(x[4])
        temp_rows.append(x[5])
        temp_rows.append(x[6])
        temp_rows.append(x[7])
        temp_rows.append(x[8])
        temp_rows.append(x[9])
        temp_rows.append(x[10])
        temp_rows.append(x[11])
        temp_calc = lowerandremove(x[12])
        temp_rows.append(temp_calc)
        master_temp_rows.append(temp_rows)
        temp_rows = []

    #setting master temp rows as rows
    rows = master_temp_rows

    #Delete
    animals = ["fish", "turtle", "yak"]

    #Talley and Dict Analysis (For later)
    final_companies = [] #the list of companies in one list
    final_list = [] #the full list with the text field
    final_pass_list = []  #the list the user sees without text

            

    #formula to get cosine for comparison / replaced cosine with jaccard. Just changed the word to the new function
    def cosine_sort_pass(inject_a, my_lib):
        my_dict = {}
        for x in my_lib:
            my_pass = jaccard_similarity(inject_a,x)
            my_dict[x] = my_pass
        
        #sort_cosine = sorted(my_dict.items(), key=lambda x:          x[1],     reverse=True)

        return my_dict


    #The corrosponsing form letters
    """"
    name = A             index 0
    Nacic = B            index 1
    State = C            index 2
    Women owned= D       index 3   
    8A = E               index 4
    Disabled Vet = F     index 5
    Hubzone = G          index 6
    Minority owned = H   index 7
    NNSA = I             index 8
    DOE Experience = L   index 9
    GOV Experience = M   index 10
    ***Website           index 11
    Text = J             index 12 (Never return)
    Smart filter = K     N/A  This will be analyzed
    Group List = N
    """

    fetch_list = request.form.getlist('choices')

    #Uncomment when you go live
    name_input = request.form['a']
    nacic_input = request.form['b']
    state_input = request.form['c']
    text_input = request.form['j']
    smart_filter_input = request.form['k']


    #Uncomment when you go live
    #This is the get list from the checkbox in the html file
    fetch_list = request.form.getlist('choices')
    #Women Owned
    if "Women-Owned" in fetch_list:
        women_owned_input = "Yes"
    if "Women-Owned" not in fetch_list:
        women_owned_input = "none"
    #8A
    if "8(a)" in fetch_list:
        eight_a_input = "Yes"
    if "8(a)" not in fetch_list:
        eight_a_input = "none"
    #Disabled Vet
    if "SDVOSB" in fetch_list:
        disabled_vet_input = "Yes"
    if "SDVOSB" not in fetch_list:
        disabled_vet_input = "none"
    #HUBZone
    if "HUBZone" in fetch_list:
        hub_zone_input = "Yes"
    if "HUBZone" not in fetch_list:
        hub_zone_input = "none"
    #Minority Owned SDB
    if "SDB" in fetch_list:
        minority_owned_input = "Yes"
    if "SDB" not in fetch_list:
        minority_owned_input = "none"
    #NNSA
    if "NNSA" in fetch_list:
        nnsa_input = "Yes"
    if "NNSA" not in fetch_list:
        nnsa_input = "none"
    #DOE
    if "Previous DOE Work" in fetch_list:
        doe_input = "Yes"
    if "Previous DOE work" not in fetch_list:
        doe_input = "none"
    #GOV 
    if "Previous Gov Work" in fetch_list:
        gov_input = "Yes"
    if "Previous Gov work" not in fetch_list:
        gov_input = "none"



    """
    #Comment out when you go live
    name_input = "none"
    nacic_input = "none"
    state_input = "Maryland"
    women_owned_input = "none"
    eight_a_input = "none"
    disabled_vet_input = "none"
    hub_zone_input = "none"
    minority_owned_input = "none"
    nnsa_input = "none"
    doe_input = "none"
    gov_input = "none"
    text_input = "none"
    smart_filter_input = "none"
    """
    #tokenizing and lowering of text input
    if text_input != "none":
        text_input = lowerandremove(text_input)
    if smart_filter_input != "none":
        smart_filter_input = lowerandremove(smart_filter_input)
        smart_filter_input = nltk.word_tokenize(smart_filter_input)



    #Counts
    name_count = 0
    nacic_count = 0
    state_count = 0
    women_owned_count = 0
    eight_a_count = 0
    disabled_vet_count = 0
    hub_zone_count = 0
    minority_owned_count = 0
    nnsa_count = 0
    doe_count = 0
    gov_count = 0
    text_count = 0
    smart_filter_count = 0

    #Temporary lists to keep the positive conditions
    temp_name = []
    temp_nacic = []
    temp_state = []
    temp_women_owned = []
    temp_eight_a = []
    temp_disabled_vet = []
    temp_hub_zone = []
    temp_minority_owned = []
    temp_nnsa = []
    temp_doe = []
    temp_gov = []
    temp_text = []
    temp_smart_filter = []

    #Pass list used in the if statement
    pass_list = []

    if name_input != "none":
        name_count = 1
    if nacic_input != "none":
        nacic_count = 1
    if state_input != "none":
        state_count = 1
    if women_owned_input != "none":
        women_owned_count = 1
    if eight_a_input != "none":
        eight_a_count = 1
    if disabled_vet_input != "none":
        disabled_vet_count = 1
    if hub_zone_input != "none":
        hub_zone_count = 1
    if minority_owned_input != "none":
        minority_owned_count = 1
    if nnsa_input != "none":
        nnsa_count = 1
    if doe_input != "none":
        doe_count = 1
    if gov_input != "none":
        gov_count = 1
    if text_input != "none":
        text_count = 1
    if smart_filter_input != "none":
        smart_filter_count = 1

    #This adds up all the input positives. 
    total_talley = name_count + nacic_count + state_count + women_owned_count + eight_a_count + disabled_vet_count + hub_zone_count + minority_owned_count + nnsa_count + doe_count + gov_count + text_count

    #Setting up all companies from rows.
    all_companies = rows

    #If statements to analyze

    #Name
    if name_count == 1:
        for x in all_companies:
            if x[0] == name_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_name.append(pass_list)
                    pass_list = []


    #NACIC
    if nacic_count == 1:
        for x in all_companies:
            if nacic_input in x[1]:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_nacic.append(pass_list)
                    pass_list = []

    #State
    if state_count == 1:
        for x in all_companies:
            if x[2] == state_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_state.append(pass_list)
                    pass_list = []

    #Women Owned
    if women_owned_count == 1:
        for x in all_companies:
            if x[3] == women_owned_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_women_owned.append(pass_list)
                    pass_list = []

    #eight a
    if eight_a_count == 1:
        for x in all_companies:
            if x[4] == eight_a_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_eight_a.append(pass_list)
                    pass_list = []

    #disabled vet
    if disabled_vet_count == 1:
        for x in all_companies:
            if x[5] == disabled_vet_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_disabled_vet.append(pass_list)
                    pass_list = []

    #hub zone
    if hub_zone_count == 1:
        for x in all_companies:
            if x[6] == disabled_vet_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_hub_zone.append(pass_list)
                    pass_list = []

    #minority owned zone
    if minority_owned_count == 1:
        for x in all_companies:
            if x[7] == minority_owned_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_minority_owned.append(pass_list)
                    pass_list = []

    #nnsa
    if nnsa_count == 1:
        for x in all_companies:
            if x[8] == nnsa_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_nnsa.append(pass_list)
                    pass_list = []

    #doe
    if doe_count == 1:
        for x in all_companies:
            if x[9] == doe_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_doe.append(pass_list)
                    pass_list = []

    #gov
    if gov_count == 1:
        for x in all_companies:
            if x[10] == gov_input:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_gov.append(pass_list)
                    pass_list = []


    #text
    if text_count == 1:
        for x in all_companies:
            if text_input in x[12]:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(x[12])
                    temp_text.append(pass_list)
                    pass_list = []

    #combining all temp lists into one combined list
    combined_list = temp_name + temp_nacic + temp_state + temp_women_owned + temp_eight_a + temp_disabled_vet + temp_hub_zone + temp_minority_owned + temp_nnsa + temp_doe + temp_gov + temp_text


    #We are taking the names of the companies that went to the combined list and putting them on the master_name. This will establish the count
    master_name = []
    for x in combined_list:
        master_name.append(x[0])

        

    #Dictionary to analyze combined list
    osdbu_dict = {}
    for x in master_name:
        if x in osdbu_dict:
            osdbu_dict[x] += 1
        else:
            osdbu_dict[x] = 1

    #We are appending the companies with the value equal to the total talley 
    for k,v in osdbu_dict.items():
        if v == total_talley:
            final_companies.append(k)

    #Error codes
    if total_talley == 0 and smart_filter_count == 1:
        error_four = [["Error four: Add another search critera along with smart filter.", "0","0","0","0","0","0","0","0","0","0","0"]]
        final_pass_list = error_four

    if total_talley == 0 and smart_filter_count == 0:
        error_three = [["Error three: Add search criteria.", "0","0","0","0","0","0","0","0","0","0","0"]]
        final_pass_list = error_three

    if len(final_companies) == 0 and smart_filter_count == 1 and total_talley > 0:
        error_one = [["Error one: No companies found.", "0","0","0","0","0","0","0","0","0","0","0"]]
        final_pass_list = error_one


    if len(final_companies) == 0 and smart_filter_count == 0 and total_talley > 0:
        error_two = [["Error two: No companies found.", "0","0","0","0","0","0","0","0","0","0","0"]]
        final_pass_list = error_two

    #Making final list
    final_list = []
    #This is matching the final companies to pull into the final list
    for x in final_companies:
        for ele in all_companies:
            if x == ele[0]:
                final_list.append(ele)
        

    #This is now taking that list and adding the proper fields


                

    #List creation of full list without smart filtering. The no smart filter is the last row for the lack of cosine
    if smart_filter_count == 0 and len(final_companies) > 0 and total_talley > 0:
        final_pass_list = []
        no_smart_filter = ["none"]
        for x in final_list:
            pass_list.append(x[0])
            pass_list.append(x[1])
            pass_list.append(x[2])
            pass_list.append(x[3])
            pass_list.append(x[4])
            pass_list.append(x[5])
            pass_list.append(x[6])
            pass_list.append(x[7])
            pass_list.append(x[8])
            pass_list.append(x[9])
            pass_list.append(x[10])
            pass_list.append(x[11])
            pass_list.append(no_smart_filter)
            final_pass_list.append(pass_list)
            pass_list = []
        
    # Delete just for reference 
    """ 
    def cosine_sort_pass(inject_a, my_lib):
        my_dict = {}
        for x in my_lib:
            my_pass = cosine(inject_a,x)
            my_dict[x] = my_pass

        return my_dict 
    """
            
            

    if smart_filter_count == 1 and len(final_companies) > 0 and total_talley > 0:
        text_only = []

        #tokenizing the text field so that I can use Jaccard
        for x in final_list:
            text_only.append(x[12])

        new_dict = {}

        #Replace with jaccard
        for x in text_only:
            my_tok = nltk.word_tokenize(x)
            cosine_pass = jaccard_similarity(smart_filter_input, my_tok)
            new_dict[x] = cosine_pass
        

        final_dict = sorted(new_dict.items(), key=lambda x:          x[1],     reverse=True)

        #For some reason it wouldn't turn into a dict. It was a       list and I had to work with it

        transfer_dict = {}
        for x in final_dict:
            transfer_dict[x[0]] = x[1]

        my_final_dict = sorted(transfer_dict.items(), key=lambda x:          x[1],     reverse=True)

        #added string function to shorten number (my_pass)
        for ele in my_final_dict:
            for x in all_companies:
                my_pass = str(ele[1])
                my_pass = my_pass[0:9]
                if x[12] == ele[0]:
                    pass_list.append(x[0])
                    pass_list.append(x[1])
                    pass_list.append(x[2])
                    pass_list.append(x[3])
                    pass_list.append(x[4])
                    pass_list.append(x[5])
                    pass_list.append(x[6])
                    pass_list.append(x[7])
                    pass_list.append(x[8])
                    pass_list.append(x[9])
                    pass_list.append(x[10])
                    pass_list.append(x[11])
                    pass_list.append(my_pass)
                    final_pass_list.append(pass_list)
                    pass_list = []
        #Code to remove the 0 scores of Jaccard
        temp_final_pass_list = []
        for x in final_pass_list:
            if x[12] != "0.0":
                temp_final_pass_list.append(x)
        final_pass_list = temp_final_pass_list


    #print (total_talley)

    total_talley = name_count + nacic_count + state_count + women_owned_count + eight_a_count + disabled_vet_count + hub_zone_count + minority_owned_count + nnsa_count + text_count

    talley_contents = [name_count,nacic_count,state_count,women_owned_count,eight_a_count,disabled_vet_count,hub_zone_count,minority_owned_count,nnsa_count,text_count,smart_filter_count]


    return render_template('after.html', data = final_pass_list)

if __name__ == "__main__":
    app.run(debug=True)
