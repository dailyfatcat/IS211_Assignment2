import argparse
import urllib.request
import logging
import datetime
import sys

def downloadData(url):
    """Downloads the data"""
    try:
        csvData = urllib.request.urlopen(url)
    except urllib.error.URLError as error:
        print(error.reason)
        sys.exit(1)
    except urllib.error.HTTPError as error:
        print(error.reason)
        sys.exit(1)
    except Exception as error:
        print(error.reason)
        sys.exit(1)
    # reads and decodes as utf-8 to make processing easier
    csvData = csvData.read().decode('utf-8')
    # create a list of the objects to be used for processing
    csvData = csvData.split("\n")

    return csvData

def processData(file_content):
    """Process the data"""
    format_str = "%d/%m/%Y"  # sets the format
    personData = {}

    #populate the dictionary
    for i in file_content:
        #list of id, name, bday
        parts = i.split(',')
        #Continue over blank lines, strip out CSV headers
        if parts[0] == "" or parts[0] == 'id':
            continue
        try:
            datetime_obj = datetime.datetime.strptime(parts[2], format_str)  # creates the date object
        except ValueError as error:
            logerror(i, parts[0])
            continue
        # in each iteration add values that do not error into the dictionary
        personData[parts[0]] = (parts[1], datetime_obj)

    return personData

def displayPerson(id, personData):
    """Display the requested person"""
    try:
        print(f"Person #{id} is {personData[id][0]} with a birthday of {personData[id][1].strftime('%Y/%m/%d')}")
    except KeyError as error:
        print("no user found with that id")

def logerror(linenum, id):
    """Logs the error"""
    logging.basicConfig(filename='error.log', level=logging.ERROR) #########
    errorstr = f"Error processing line {linenum} for ID #{id}"
    assignment2 = logging.getLogger()
    assignment2.error(errorstr)

def main(url):
    print(f"Running main with URL = {url}...")
    data = processData(downloadData(url))
    while True:
        #Get user input
        userinput = input("Please input user id, or number <= 0 to exit: ")
        # Get person data
        try:
            if int(userinput) <= 0:
                break
            displayPerson(userinput, data)
            print('\n')
        #If userinput is not an integer value reprompt
        except ValueError as error:
            print("Please enter an integer ID value, or <= 0 to exit")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)