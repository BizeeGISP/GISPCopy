from os import listdir
import csv
import configUtilities



CSV_PATH = configUtilities.getProperties('E1-CSV', 'PATH')

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

filenames = find_csv_filenames(CSV_PATH)
print(filenames)
for name in filenames:
    print("FileName",CSV_PATH + name)
    with open(CSV_PATH + name, 'r') as f:

        reader = csv.reader(f)
        counter = 0
        values = []
        for row in reader:

            url = row[0]
            if (url != None):

                counter += 1
                data = (url, 'New')
                values.append(data)
                if (counter == 10000):

                    counter = 0
                    values = []

    print( values)




