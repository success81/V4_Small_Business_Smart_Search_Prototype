####ReDo-JUL2022###
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


    #Talley and Dict Analysis (For later)
    final_companies = [] #the list of companies in one list
    final_list = [] #the full list with the text field
    final_pass_list = []  #the list the user sees without text

    #Creating punctuation stop list
    punct =  set(string.punctuation)

    #Setting Stopwords
    my_stopwords = set(stopwords.words('english'))

    #Combining stopwords with puntuations
    my_stopwords |= punct

    #Jaccards Similarity Function
    def jaccard_similarity(list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return float(len(s1.intersection(s2)) / len(s1.union(s2)))

    #Function to lower and remove 
    def lowerandremove(x):
        blank_string = ""
        lower_temp = x.lower()
        tokens = word_tokenize(lower_temp)
        for x in tokens:
            if x not in my_stopwords:
                blank_string += " "
                blank_string += x
        return blank_string

    #CSV File
    #Importing excel
    filename = "big_cosine_mod_z.csv"

    #Setting up lists for csv
    fields = []
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
        temp_rows.append(x[12])
        temp_rows.append(x[13])
        temp_rows.append(x[14])
        temp_rows.append(x[15])
        temp_rows.append(x[16])
        temp_rows.append(x[17])
        temp_rows.append(x[18])
        temp_rows.append(x[19])
        temp_rows.append(x[20])
        temp_rows.append(x[21])
        temp_calc = lowerandremove(x[22])
        temp_rows.append(temp_calc)
        master_temp_rows.append(temp_rows)
        temp_rows = []

    #setting master temp rows as rows
    rows = master_temp_rows





    ###########################################################
    #The corrosponsing form letters
    """
    name = A                                            index 0
    NACICS Code(s) = B                                  index 1
    State = C                                           index 2
    Small Business                                      index 3
    Small Disadvantaged Business(SDB)                   index 4
    8(a) Program                                        index 5
    Minority-Owned                                      index 6
    Alaska Native Corporation(ANC)                      index 7
    Native Hawaiian Organization(NHO)                   index 8
    Indian Tribe                                        index 9
    Historically Underutilized Business Zone(HUBZone)   index 10
    Veteran-Owned Small Business(VOSB)                  index 11
    Service-Disabled Veteran-Owned Small Business(SDVOSB) index 12
    Woman-Owned Small Business(WOSB)                      index 13
    Economically Disadvantaged Woman-Owned Small Business
    (EDWOSB)                                            index 14
    Minority Serving Institution(MSI)                   index 15
    Historically Black Colleges and Universities(HBCU)  index 16
    Large Business                                      index 17
    DOE Experience                                      index 18
    GOV Experience                                      index 19
    NNSA Experience                                     index 20
    Link- L                                             index 21
    Text-  J                                            index 22
    Smart filter K
    #########################################################
    Women owned= D                       index 3   
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
    ##################TURN ON WHEN LIVE###########

    #Don't Uncomment/ Uncomment when you go live/This is duplicated below/Just scared to delete
    #############################
    """
    name_input = request.form['a']
    nacic_input = request.form['b']
    state_input = request.form['c']
    text_input = request.form['j']
    smart_filter_input = request.form['k']
    """
    #################################
    #Uncomment when you go live
    #This is the get list from the checkbox in the html file
    fetch_list = request.form.getlist('choices')
    #Small Business
    if "Small Business" in fetch_list:
        small_biz_input = "Yes"
    if "Small Business" not in fetch_list:
        small_biz_input = "none"
    #SDB
    if "Small Disadvantaged Business(SDB)" in fetch_list:
        sdb_input = "Yes"
    if "Small Disadvantaged Business(SDB)" not in fetch_list:
        sdb_input = "none"
    #8A
    if "8(a) Program" in fetch_list:
        eight_a_input  = "Yes"
    if "8(a) Program" not in fetch_list:
        eight_a_input  = "none"
    #Minority-Owned
    if "Minority-Owned" in fetch_list:
        minority_owned_input  = "Yes"
    if "Minority-Owned" not in fetch_list:
        minority_owned_input = "none"
    #ANC
    if "Alaska Native Corporation(ANC)" in fetch_list:
        anc_input = "Yes"
    if "Alaska Native Corporation(ANC)" not in fetch_list:
        anc_input = "none"
    #NHO
    if "Native Hawaiian Organization(NHO)" in fetch_list:
        nho_input = "Yes"
    if "Native Hawaiian Organization(NHO)" not in fetch_list:
        nho_input = "none"
    #Indian Tribe
    if "Indian Tribe" in fetch_list:
        indian_input = "Yes"
    if "Indian Tribe" not in fetch_list:
        indian_input = "none"
    #Hubzone 
    if "Historically Underutilized Business Zone(HUBZone)" in fetch_list:
        hub_zone_input = "Yes"
    if "Historically Underutilized Business Zone(HUBZone)" not in fetch_list:
        hub_zone_input = "none"
    #VOSB 
    if "Veteran-Owned Small Business(VOSB)" in fetch_list:
        vosb_input = "Yes"
    if "Veteran-Owned Small Business(VOSB)" not in fetch_list:
        vosb_input = "none"
    #SDVOSB 
    if "Service-Disabled Veteran-Owned Small Business(SDVOSB)" in fetch_list:
        sdvosb_input = "Yes"
    if "Service-Disabled Veteran-Owned Small Business(SDVOSB)" not in fetch_list:
        sdvosb_input = "none"
    #GOV 
    if "Woman-Owned Small Business(WOSB)" in fetch_list:
        wosb_input = "Yes"
    if "Woman-Owned Small Business(WOSB)" not in fetch_list:
        wosb_input = "none"
    #EDWOSB
    if "Economically Disadvantaged Woman-Owned Small Business(EDWOSB)" in fetch_list:
        edwosb_input = "Yes"
    if "Economically Disadvantaged Woman-Owned Small Business(EDWOSB)" not in fetch_list:
        edwosb_input = "none"
    #MSI 
    if "Minority Serving Institution(MSI)" in fetch_list:
        msi_input = "Yes"
    if "Minority Serving Institution(MSI)" not in fetch_list:
        msi_input = "none"
    #HBCU
    if "Historically Black Colleges and Universities(HBCU)" in fetch_list:
        hbcu_input = "Yes"
    if "Historically Black Colleges and Universities(HBCU)" not in fetch_list:
        hbcu_input = "none"
    #Large Business
    if "Large Business" in fetch_list:
        large_biz_input = "Yes"
    if "Large Business" not in fetch_list:
        large_biz_input = "none"

    #Experiences Pull
    experience_list = request.form.getlist('exp')
    #DOE Exp
    if "DOE Experience" in experience_list:
        doe_input = "Yes"
    if "DOE Experience" not in experience_list:
        doe_input = "none"
    #GOV Exp
    if "GOV Experience" in experience_list:
        gov_input = "Yes"
    if "GOV Experience" not in experience_list:
        gov_input = "none"
        
    #NNSA Exp
    if "NNSA Experience" in experience_list:
        nnsa_input = "Yes"
    if "NNSA Experience" not in experience_list:
        nnsa_input = "none"
    """

    ###########################################################
    ###############Comment out when you go live###########
    """
    """
    ######top
    name_input = "none"
    nacic_input = "none"
    state_input = "Maryland"
    #######Certs
    small_biz_input = "none"
    sdb_input = "none"
    eight_a_input = "none"
    minority_owned_input = "none"
    anc_input = "none"
    nho_input = "none"
    indian_input = "none"
    hub_zone_input = "none"
    vosb_input = "none"
    sdvosb_input = "none"
    wosb_input = "none"
    edwosb_input = "none"
    hbcu_input = "none"
    msi_input = "none"
    large_biz_input = "none"
    ########exp
    doe_input = "none"
    gov_input = "none"
    nnsa_input = "none"
    #######end
    text_input = "none"
    smart_filter_input = "cybersecurity"

    """
    ###########################################################

    ###########################################################
    ###############UNComment out when you go live###########
    #Non-Checkbox
    #uncomment
    name_input = request.form['a']
    nacic_input = request.form['b']
    state_input = request.form['c']
    #uncomment
    text_input = "none" #request.form['j']
    smart_filter_input = request.form['k']

    ###########################################################

    #tokenizing and lowering of text input
    if text_input != "none":
        text_input = lowerandremove(text_input)
    if smart_filter_input != "none":
        smart_filter_input = lowerandremove(smart_filter_input)
        smart_filter_input = nltk.word_tokenize(smart_filter_input)

    #Counts
    ######top
    name_count = 0
    nacic_count = 0
    state_count = 0
    #######Certs
    small_biz_count = 0
    sdb_count = 0
    eight_a_count = 0
    minority_owned_count = 0
    anc_count = 0
    nho_count = 0
    indian_count = 0
    hub_zone_count = 0
    vosb_count = 0
    sdvosb_count = 0
    wosb_count = 0
    edwosb_count = 0
    hbcu_count = 0
    msi_count = 0
    large_biz_count = 0
    ########exp
    doe_count = 0
    gov_count = 0
    nnsa_count = 0
    #######end
    text_count = 0
    smart_filter_count = 0

    #Temporary lists to keep the positive conditions
    temp_name = []
    temp_nacic = []
    temp_state = []

    temp_small_biz = []
    temp_sdb = []
    temp_eight_a = []
    temp_minority_owned = []
    temp_anc = []
    temp_nho = []
    temp_indian = []
    temp_hub_zone = []
    temp_vosb = []
    temp_sdvosb = []
    temp_wosb = []
    temp_edwosb = []
    temp_hbcu = []
    temp_msi = []
    temp_large_biz = []



    temp_doe = []
    temp_gov = []
    temp_nnsa = []

    temp_text = []
    temp_smart_filter = []

    #Pass list used in the if statement
    pass_list = []

    #Incrementing count if something is in the field
    if name_input != "none":
        name_count = 1
    if nacic_input != "none":
        nacic_count = 1
    if state_input != "none":
        state_count = 1
    if small_biz_input != "none":
        small_biz_count = 1
    if sdb_input != "none":
        sdb_count = 1
    if eight_a_input != "none":
        eight_a_count = 1
    if minority_owned_input != "none":
        minority_owned_count = 1
    if anc_input != "none":
        anc_count = 1
    if nho_input != "none":
        nho_count = 1
    if indian_input != "none":
        indian_count = 1
    if hub_zone_input != "none":
        hub_zone_count = 1
    if vosb_input != "none":
        vosb_count = 1
    if sdvosb_input != "none":
        sdvosb_count = 1
    if wosb_input != "none":
        wosb_count = 1
    if edwosb_input != "none":
        edwosb_count = 1
    if hbcu_input != "none":
        hbcu_count = 1
    if msi_input != "none":
        msi_count = 1
    if large_biz_input != "none":
        large_biz_count = 1
    if doe_input != "none":
        doe_count = 1
    if gov_input != "none":
        gov_count = 1
    if nnsa_input != "none":
        nnsa_count = 1
    if text_input != "none":
        text_count = 1
    if smart_filter_input != "none":
        smart_filter_count = 1


    #Adding up all the counts
    total_talley = name_count + nacic_count + state_count + small_biz_count + sdb_count + eight_a_count + minority_owned_count + anc_count + nho_count + indian_count + hub_zone_count + vosb_count + sdvosb_count + wosb_count + edwosb_count + hbcu_count + msi_count + large_biz_count + doe_count + gov_count + nnsa_count + text_count

    #delete
    #mystery = [name_count, nacic_count, state_count, small_biz_count, sdb_count, eight_a_count, minority_owned_count, anc_count, nho_count, indian_count, hub_zone_count,vosb_count, sdvosb_count, wosb_count, edwosb_count, hbcu_count, msi_count, large_biz_count, doe_count, gov_count, nnsa_count, text_count]


    #Setting up all companies from rows.
    all_companies = rows



    #Analyze input
    #Name Analyze
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_name.append(pass_list)
                    pass_list = []

    #NACIC
    if nacic_count == 1:
        for x in all_companies:
            if x[1] == nacic_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_state.append(pass_list)
                    pass_list = []


    #Small Biz Analyze
    if small_biz_count == 1:
        for x in all_companies:
            if x[3] == small_biz_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_small_biz.append(pass_list)
                    pass_list = []

    #sdb analyze
    if sdb_count == 1:
        for x in all_companies:
            if x[4] == sdb_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_sdb.append(pass_list)
                    pass_list = []

    #8A Analyze
    if eight_a_count == 1:
        for x in all_companies:
            if x[5] == eight_a_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_eight_a.append(pass_list)
                    pass_list = []

    #Minority owned
    if minority_owned_count == 1:
        for x in all_companies:
            if x[6] == minority_owned_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_minority_owned.append(pass_list)
                    pass_list = []

    #ANC Analyze
    if anc_count == 1:
        for x in all_companies:
            if x[7] == anc_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_anc.append(pass_list)
                    pass_list = []
                    

    #NHO Analyze
    if nho_count == 1:
        for x in all_companies:
            if x[8] == nho_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_nho.append(pass_list)
                    pass_list = []
    #Indian Analyze
    if indian_count == 1:
        for x in all_companies:
            if x[9] == indian_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_indian.append(pass_list)
                    pass_list = []

    #Hubzone Analyze
    if hub_zone_count == 1:
        for x in all_companies:
            if x[10] == hub_zone_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_hub_zone.append(pass_list)
                    pass_list = []

    #VOSB Analyze
    if vosb_count == 1:
        for x in all_companies:
            if x[11] == vosb_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_vosb.append(pass_list)
                    pass_list = []

    #SDVOSB Analyze
    if sdvosb_count == 1:
        for x in all_companies:
            if x[12] == sdvosb_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_sdvosb.append(pass_list)
                    pass_list = []

    #wosb
    if wosb_count == 1:
        for x in all_companies:
            if x[13] == wosb_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_wosb.append(pass_list)
                    pass_list = []

    #Edwosb
    if edwosb_count == 1:
        for x in all_companies:
            if x[14] == edwosb_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_edwosb.append(pass_list)
                    pass_list = []

    #msi
    if msi_count == 1:
        for x in all_companies:
            if x[15] == msi_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_msi.append(pass_list)
                    pass_list = []

    #HCBU
    if hbcu_count == 1:
        for x in all_companies:
            if x[16] == hbcu_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_hbcu.append(pass_list)
                    pass_list = []

    #Large Biz
    if large_biz_count == 1:
        for x in all_companies:
            if x[17] == large_biz_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_large_biz.append(pass_list)
                    pass_list = []

    #Doe
    if doe_count == 1:
        for x in all_companies:
            if x[18] == doe_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_doe.append(pass_list)
                    pass_list = []


    #gov
    if gov_count == 1:
        for x in all_companies:
            if x[19] == gov_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_gov.append(pass_list)
                    pass_list = []

    #NNSA 
    if nnsa_count == 1:
        for x in all_companies:
            if x[20] == nnsa_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_nnsa.append(pass_list)
                    pass_list = []

    #Text
    if text_count == 1:
        for x in all_companies:
            if text_input in x[22]:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_text.append(pass_list)
                    pass_list = []

    #Smart Filter
    if smart_filter_count == 1:
        for x in all_companies:
            if x[22] == smart_filter_input:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(x[22])
                    temp_smart_filter.append(pass_list)
                    pass_list = []
            



    #combining all temp lists into one combined list
    combined_list = temp_name + temp_nacic + temp_state + temp_small_biz + temp_sdb + temp_eight_a + temp_minority_owned + temp_anc + temp_nho + temp_indian + temp_hub_zone + temp_vosb + temp_sdvosb + temp_wosb + temp_edwosb + temp_hbcu + temp_msi + temp_large_biz + temp_doe + temp_gov + temp_nnsa + temp_text
    #We are taking the names of the companies that went to the combined list and putting them on the master_name. This will establish the count
    master_name = []
    for x in combined_list:
        master_name.append(x[0])

    #This is establishing a count in the dictionary
    osdbu_dict = {}
    for x in master_name:
        if x in osdbu_dict:
            osdbu_dict[x] += 1
        else:
            osdbu_dict[x] = 1

    #This is comparing the total talley to the Dict Value. If they are equal it makes it to the final companies list
    for k,v in osdbu_dict.items():
        if v == total_talley:
            final_companies.append(k)

    #This is matching the final companies to pull into the final list
    for x in final_companies:
        for ele in all_companies:
            if x == ele[0]:
                final_list.append(ele)

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
            pass_list.append(x[12])
            pass_list.append(x[13])
            pass_list.append(x[14])
            pass_list.append(x[15])
            pass_list.append(x[16])
            pass_list.append(x[17])
            pass_list.append(x[18])
            pass_list.append(x[19])
            pass_list.append(x[20])
            pass_list.append(x[21])
            pass_list.append(no_smart_filter)
            final_pass_list.append(pass_list)
            pass_list = []

    #Code to add in Smart filter
    if smart_filter_count == 1 and len(final_companies) > 0 and total_talley > 0:
        text_only = []

        #tokenizing the text field so that I can use Jaccard
        for x in final_list:
            text_only.append(x[22])

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
                if x[22] == ele[0]:
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
                    pass_list.append(x[13])
                    pass_list.append(x[14])
                    pass_list.append(x[15])
                    pass_list.append(x[16])
                    pass_list.append(x[17])
                    pass_list.append(x[18])
                    pass_list.append(x[19])
                    pass_list.append(x[20])
                    pass_list.append(x[21])
                    pass_list.append(my_pass)
                    final_pass_list.append(pass_list)
                    pass_list = []
        #Code to remove the 0 scores of Jaccard
        temp_final_pass_list = []
        for x in final_pass_list:
            if x[22] != "0.0":
                temp_final_pass_list.append(x)
        final_pass_list = temp_final_pass_list
    return render_template('after.html', data = final_pass_list)

if __name__ == "__main__":
    app.run(debug=True)

