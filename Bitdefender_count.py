import requests , json, base64

import webbrowser, os, certifi, urllib3

urllib3.disable_warnings()


Licensed_computer = 0

unLicensed_computer = 0

organizations_ids = []

dictionary_of_organitations = {}

report_of_devices = {}

report_of_organizations = []

org_lastupdates = {}

devices_ages_and_companies = []

report_of_outdates_devices = []

bitdefender_dictionary = []

arrayOfCompanies = []

report_of_devices_bidefender = {}

report_of_organizations_bitdefender = []



def progress_bar(progress, total):

    percent = 100* (progress / float(total))

    bar = '█' * int(percent) + '-' * (100 - int(percent))

    print(f"\r|{bar}| {percent:.2f}%", end="\r")



#Connecting to Bitdefender and getting all companies

def connect_to_Bitdefender():

    apiKey = ""

    loginString = apiKey + ":"

    encodedBytes = base64.b64encode(loginString.encode())

    encodedUserPassSequence = str(encodedBytes,'utf-8')

    authorizationHeader = "Basic " + encodedUserPassSequence



    apiEndpoint_Url = "https://cloud.gravityzone.bitdefender.com/api/v1.0/jsonrpc/network"



    request = '{"params": { "filters" : {"companyType": 1, "licenseType": 3 } },"jsonrpc": "2.0","method": "getCompaniesList","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'



    result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})



    arrayOfCompanies = result.json()



#Return all companies in a Array

    return arrayOfCompanies


#Bitdefender only charges for Equipment that are mark as Managed, We get the Company I per company and we search their equipment one by one      

def get_managed_equipment_count(id_of_company):

    array_of_manage_computers = []

    apiKey = ""

    loginString = apiKey + ":"

    encodedBytes = base64.b64encode(loginString.encode())

    encodedUserPassSequence = str(encodedBytes,'utf-8')

    authorizationHeader = "Basic " + encodedUserPassSequence



    apiEndpoint_Url = "https://cloud.gravityzone.bitdefender.com/api/v1.0/jsonrpc/Network"

#Build a String for a Json Instruction this cannot be modify with Variables it has to be a string

    id = str(id_of_company)

    json1 = '{"params": { "parentId" :'

    json2 = ', "perPage": 100},"jsonrpc": "2.0","method": "getEndpointsList","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'

    newjson = json1 + ' "' + id + '"' + json2



    request = newjson



    result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

    equipment = result.json()

    equipmenttotal = len(equipment['result']['items'])

#Each [] pertains to a section on the return array, this loop iterates through each line to fine all the manage equipment

    for x in range(equipmenttotal):


        if equipment['result']['items'][x]['isManaged'] == True:

            array_of_manage_computers.append(equipment['result']['items'][x]['id'])


    return array_of_manage_computers



#Every device has a license state from 0 to 2, 0 is an pending license, 1 is a active license and 2 is a expired license   

def get_licensed_count(a):

    apiKey = ""

    loginString = apiKey + ":"

    encodedBytes = base64.b64encode(loginString.encode())

    encodedUserPassSequence = str(encodedBytes,'utf-8')

    authorizationHeader = "Basic " + encodedUserPassSequence



    apiEndpoint_Url = "https://cloud.gravityzone.bitdefender.com/api/v1.0/jsonrpc/Network"



    id = str(a)

    json1 = '{"params": { "endpointId" :'

    json2 = '},"jsonrpc": "2.0","method": "getManagedEndpointDetails","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'

    newjson = json1 + ' "' + id + '"' + json2



    request = newjson



    result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

    equipment = result.json()



    if equipment['result']['agent']['licensed'] == 1 :

        return 1

    else:

        return 0


def get_unlicensed_count(a):

    apiKey = ""

    loginString = apiKey + ":"

    encodedBytes = base64.b64encode(loginString.encode())

    encodedUserPassSequence = str(encodedBytes,'utf-8')

    authorizationHeader = "Basic " + encodedUserPassSequence



    apiEndpoint_Url = "https://cloud.gravityzone.bitdefender.com/api/v1.0/jsonrpc/Network"



    id = str(a)

    json1 = '{"params": { "endpointId" :'

    json2 = '},"jsonrpc": "2.0","method": "getManagedEndpointDetails","id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"}'

    newjson = json1 + ' "' + id + '"' + json2


    request = newjson


    result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

    equipment = result.json()



    if equipment['result']['agent']['licensed'] == 2 :

        return 1

    else:

        return 0


    

    



#Assing array of companies to a variable to be used     

arrayOfCompanies = connect_to_Bitdefender()



#we need the lenght of Array of companies results to see how many time we will iterate to the array

lenght = len(arrayOfCompanies['result'])



progress_bar(0, lenght)

for x in range(lenght):

#Returns all the manage equipement per company

    progress_bar(x + 1, lenght)

    print("gathering data from", arrayOfCompanies['result'][x]['name'] )

    managed_equipment = get_managed_equipment_count(arrayOfCompanies['result'][x]['id'])

#Separate each computer on licensed and unlicense and does the count   

    for r in range(len(managed_equipment)):

        unLicensed_computer = unLicensed_computer + get_unlicensed_count(managed_equipment[r])

        Licensed_computer = Licensed_computer + get_licensed_count(managed_equipment[r])

        



#We added values to a dictionary so we have a key and value to retrieve information and later we store in an a array so we can hold as many dictionaries we want

    report_of_devices_bidefender = {"company_name" : arrayOfCompanies['result'][x]['name'],"Managed": len(managed_equipment), "Licensed":  Licensed_computer, "Expired_License": unLicensed_computer}

    report_of_organizations_bitdefender.append(report_of_devices_bidefender)

    Licensed_computer = 0

    unLicensed_computer = 0



#print the array of Dictionary, We can also print it in diferent formatis if we use f()




html_content = f"<html> <head><h1>this are the Bitdefender Counts</h1></head>  <br> <body>{report_of_organizations_bitdefender}</body>  </html>"



with open("Result_for_bitdefender.html", "w") as html_file:

    html_file.write(html_content)

    print("success")