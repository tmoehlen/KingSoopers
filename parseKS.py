import sys
from tkinter import Tk
from tkinter import filedialog
 
def read_raw_data_to_dict(file_name):
    """Get a filename, read the raw data into a list of dictionaries"""
    my_dict = []
 

    try:
        file_ptr = open(file_name)
    except OSError:
        print("Cannot open " + file_name)
    else:
        team_name = file_ptr.readline()
        for line in file_ptr:
            if line.split(',')[0] == '':
                break
            if line[:11] == "Transaction":
                keylist = []
                keylist = line.split(",")
            else:
                valuelist = line.split(",")
                my_dict.append(dict(zip(keylist, valuelist)))
        return my_dict
 
def read_csv_to_dict(file_name):
    """Read a CSV file into a dict.  The first column will be the keys.  The other columns will be a list."""
 
    local_dict = {}
    MAX_CARDS = 21
 
    try:
        file_ptr = open(file_name)
    except OSError:
        print("Cannot open " + file_name)
    else:
        for line in file_ptr:
            numlist = []
            keyitem = line.split(",")[0]
            #User can have 20 cards max!
            for _ii_ in range(1, MAX_CARDS):
                try:
                    numlist.append(line.split(",")[_ii_].replace('-', '').replace('\n', ''))
                except:
                    continue
 
            local_dict[keyitem] = numlist
    return local_dict
 
Tk().withdraw()
fn = filedialog.askopenfilename(title = "Please select the Raw Data CSV file.", \
                     filetypes = (("CSV files", "*.csv"), ("All Files", "*.*")))
cn = filedialog.askopenfilename(title = "Now select the Card Numbers CSV file.", \
                     filetypes = (("CSV files", "*.csv"), ("All Files", "*.*")))
 
#fn = "C:\\Users\\tmoehlen\\Documents\\PPP\\ks-stmt.csv"
#cn = "C:\\Users\\tmoehlen\\Documents\\PPP\\KS Card Numbers.csv"
 
MYDICT = read_raw_data_to_dict(fn)
NUM_DICT = read_csv_to_dict(cn)
NEW_DICT = {}
 
total = 0
for _xx_ in MYDICT:
    #Remove all hyphens from the card number and use only the last 9 digits
    cust_card_no = _xx_['Customer Card No.'].replace('-', '')[-9:]
    reload_amt = _xx_['Reload Amount'][1:]  #Remove the leading dollar sign
    match = 0
    for kk,value in NUM_DICT.items():
        if cust_card_no in value:
            match += 1
            total += float(reload_amt)
            if kk not in NEW_DICT.keys():
                NEW_DICT[kk] = []
                NEW_DICT[kk].append(reload_amt)
            else:
                NEW_DICT[kk].append(reload_amt)
    if match == 0:
        print(reload_amt + "   " + "Unknown" + "   " + cust_card_no)
        if "Unknown" not in NEW_DICT.keys():
            NEW_DICT["Unknown"] = []
            NEW_DICT["Unknown"].append(reload_amt)
        else:
            NEW_DICT["Unknown"].append(reload_amt)
 
        total += float(reload_amt)
 
rounded_total = format(total, '.2f')
print("")
print("Total = $" + str(rounded_total))
print("Check amount = $" + str(format(total * 0.05, '.2f')))
print("")
 
subtotal = 0
confirm_amt = 0
for keys, values in NEW_DICT.items():
    subtotal = sum(float(i) for i in values) * 0.05
    subtotal_print = "$" + str(format(subtotal, '.2f'))
    print('%-15s%-15s' % (keys, subtotal_print))
    confirm_amt += subtotal
 
print("")
if abs(total * 0.05 - confirm_amt) < 0.001:
    print("Check amount confirmed!!")
else:
    print("Check amount MISMATCH!!")
    print("Total = {}".format(total * 0.05))
    print("Confirm = {}".format(confirm_amt))
#print "Confirm = $" + str(format(confirm_amt, '.2f'))
 