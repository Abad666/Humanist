import csv
import re

### Humanist ver 0.1 ###
### Mikolaj Jendykiewicz, 2024 ###
### Short note on how to use the program. First point the csvfile variable to the desired .csv file
### After all of this you should be done and ready to use the aforementioned files for your needs

ruleset = ""

program = ""

whenall = [ ]

features = [ ]

values = [ ]

csvfile=""

command = ''



def readFeatures(csvfile):
    with open(csvfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        first_row = csvfile.readline()
        testdict = []
        regex=r"^[a-zA-Z0-9_]*$"
        csvfile.seek(0)

        tempstring = ''
        i=0

        for feature in first_row:
            key = ""
            if re.match(regex, feature):
                tempstring += feature
            else:
                key = tempstring
                tempstring = ""
                testdict.append(key)

        return testdict




def generate(features, csvfile, program):
    with open(csvfile, newline='') as csvfile:


        ruleset = input("Name your ruleset.")
        reader = csv.DictReader(csvfile, delimiter=';')
        program += "from durable.lang import *\n"
        program += "with ruleset('"+ruleset+"'):"

        regex = r"^[a-zA-Z0-9_]*$"
        for row in reader:
            assert_fact = "\n\t\tc.assert_fact("
            command = "\n\t@when_all("
            try:
                maprowsandcols = ""
                for i in range(len(features)-1):
                    #print(row[features[i]])

                    maprowsandcols += "(m."+features[i]+"=='"+row[features[i]]+"')"
                    if(i!=len(features) - 2):
                        maprowsandcols += " & "
                    else:
                        maprowsandcols += ")\n"
                        command += maprowsandcols

                program += command
                go = row[features[len(features) - 1]]

                #go_slugified = re.sub('\s+', '_', go)
                go_slugified = re.sub("[ :,./'!@#$%^&*()+*|\d-]", '_', go)
                #print(go_slugified)
                program += "\tdef "+go_slugified+"(c):"
                assert_fact += "{ '"+ruleset+"placeholder': c.m."+ruleset+"placeholder, 'result': '"+go+"', 'metaphore': '', 'desc': '' })"
                program += assert_fact






            except KeyError:
                print("Uhh, something went wrong, dunno what")
        lastwhenall = "\n\t@when_all(+m." + ruleset + "placeholder)"
        lastdef = "\n\tdef output(c):"
        endl = "\n\t\t"

        printout = r"print('{0}.{1}\n Czemu taki wynik: {2} \n Opis: {3}\n'.format(c.m." + ruleset + "placeholder, c.m.result, c.m.metaphore, c.m.desc))"
        program += lastwhenall
        program += lastdef
        program += endl
        program += printout
        postexample = "\n\npost('" + ruleset + "', {'" + ruleset + "placeholder': '1',"
        amountofcols = len(features) - 1
        for i in range(amountofcols):
            postexample += "'"+features[i]+"': ''"
            if(i!=amountofcols-1):
                postexample+=","
        postexample += "})"
        program+="\n\n###Fill in the desired values for durable_rules to interpret"
        program += postexample
        text_file = open("generated.py", "w")
        n = text_file.write(program)
        text_file.close()

        print(n)












features = readFeatures('bruh.csv')
generate(features, 'bruh.csv', program)





