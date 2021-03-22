import csv

def get_data()->list:
    """Reads data from the csv file
    
    Returns
    list of each row"""
    return_list = []
    csvfile = open("data.csv")
    csvreader = csv.reader(csvfile)
    return_list = []
    for line in csvreader:
        return_list.append(line)
    csvfile.close
    return return_list

if __name__ == "__main__":
    print(len(get_data()))