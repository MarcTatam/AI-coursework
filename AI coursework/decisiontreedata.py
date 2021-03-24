import csv
import matplotlib.pyplot as plt

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

def get_tree_data()->list:
    """Reads data from the csv file
    
    Returns
    list of each row"""
    return_list = []
    csvfile = open("data.csv")
    csvreader = csv.reader(csvfile)
    return_list = []
    for line in csvreader:
        if line[0] != "cell_id":
            return_list.append(convert_row(line))
    csvfile.close
    return return_list


def sort_data(data:list)->(list,list,list,list,list,list):
    """Sorts the data into each age category for analysis

    Args
    data - list of data from csv file

    Returns
    6 list tuple of each age categorys dataset"""
    under_eighteen = []
    eighteen_to_thirty = []
    thirty_to_fourty = []
    fourty_to_fifty = []
    fifty_to_sixty = []
    sixty_plus = []
    for row in data:
        if row[21] == "age_under_18":
            under_eighteen.append(convert_row(row))
        elif row[21] == "age_18_30":
            eighteen_to_thirty.append(convert_row(row))
        elif row[21] == "age_30_40":
            thirty_to_fourty.append(convert_row(row))
        elif row[21] == "age_40_50":
            fourty_to_fifty.append(convert_row(row))
        elif row[21] == "age_50_60":
            fifty_to_sixty.append(convert_row(row))
        elif row[21] == "age_over_60":
            sixty_plus.append(convert_row(row))
    return (under_eighteen, eighteen_to_thirty, thirty_to_fourty, fourty_to_fifty, fifty_to_sixty, sixty_plus)

def convert_row(row:list)->list:
    """Converts all the data in a row from string to appropriate data format

    Args
    row - row to convert

    Reutrns
    list representing converted row"""
    converted = []
    converted.append(row[0])
    for i in range(1, 21):
        converted.append(float(row[i]))
    converted.append(row[21])
    return converted
    
def average_matrix(data):
    matrix = []
    for i in range(0,6):
        matrix.append([])
        row_count = 0
        temp_list =[]
        for row in data[i]:
            row_count += 1
            for cell_index in range(0, len(row)):
                if isinstance(row[cell_index], float):
                    if len(temp_list) < 20:
                        temp_list.append(row[cell_index])
                    else:
                        temp_list[cell_index-1] = temp_list[cell_index -1] + row[cell_index]
        for j in range(0,22):
            if j == 0:
                matrix[i].append("ID")
            elif j == 21:
                matrix[i].append(data[i][0][j])
            else:
                matrix[i].append(temp_list[j-1]/row_count)
    return matrix

def plot_charts(matrix, index_of_data):
    names = []
    values = []
    for i in range(0,6):
        names.append(matrix[i][21])
        values.append(matrix[i][index_of_data])
    plt.bar(names, values)
    plt.show()

def average_values(matrix):
    average_list = []
    for i in range(0,22):
        temp_value = 0
        if i == 0 or i == 21:
            average_list.append("placeholder")
        else:
            for j in range(0,6):
                temp_value += matrix[j][i]
            average_list.append(temp_value/6)
    return average_list


if __name__ == "__main__":
    data = sort_data(get_data())
    matrix = average_matrix(data)
    plot_charts(matrix, 20)