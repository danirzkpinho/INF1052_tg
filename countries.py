from countries_validation import *
import tempfile
from shutil import copyfile
import os

countries_file = "data/countryInfo.txt"
items_per_listing = 10

fields = {'ISO': validate_iso,
          'ISO3': validate_iso3,
          'ISO-Numeric': validate_isonumeric,
          'fips': validate_fips,
          'Country': validate_country,
          'Capital': validate_capital,
          'Area(in sq km)': validate_area,
          'Population': validate_population,
          'Continent': validate_continent,
          'tld': validate_tld,
          'CurrencyCode': validate_currencycode,
          'CurrencyName': validate_currencyname,
          'Phone': validate_phone,
          'Postal Code Format': validate_postalcodeformat,
          'Postal Code Regex': validate_postalcoderegex,
          'Languages': validate_languages,
          'geonameid': validate_geonameid,
          'neighbours': validate_neighbours,
          'EquivalentFipsCode': validate_equivalentfipscode}


def insert_country():
    new_row = []

    with open(countries_file, 'r', encoding='utf-8') as file:
        field_names = [x.strip() for x in file.readline().split("\t")]

        print(field_names)

        for field in field_names:
            new_field = input(field + ": ")
            while not fields[field](new_field):
                print("Invalid Input:", field, "cannot be", new_field, end='\n\n')
                new_field = input(field + " -> ")
            new_row.append(new_field)

    with open(countries_file, 'a', encoding='utf-8') as file:
        file.write("\t".join(new_row) + "\n")


def update_country():
    country_modify = str(input("Que país deseja modificar [ISO]? "))
    old_row = []
    with open(countries_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()  

        for line in lines:  
            f = line.split("\t")  
            if country_modify == f[0]:  
                old_row = f
                break

    if len(old_row) == 0:
        print("The country with ISO " + country_modify + " doesnt exist")
        return

    new_row = []

    print("\nPara manter o valor anterior, deixar em branco\n")

    with open(countries_file, 'r', encoding='utf-8') as file:
        field_names = [x.strip() for x in file.readline().split("\t")]

        for i, field in enumerate(field_names):
            new_field = input(field + " (" + str(old_row[i]) + "): ")

            if len(new_field) == 0:
                new_field = old_row[i]

            while not fields[field](new_field):
                print("Invalid Input:", field, "cannot be", new_field, end='\n\n')
                new_field = input(field + " (" + old_row[i] + "): ")
                if len(new_field) == 0:
                    new_field = old_row[i]
            new_row.append(new_field)

    print(new_row)

    fd, filename = tempfile.mkstemp()
    with open(countries_file, 'r', encoding='utf-8') as infile, open(fd, 'w',
                                                                     encoding='utf-8') as outfile:  
        lines = infile.readlines()  

        for line in lines:  
            f = line.split("\t")
            if old_row[0] != f[0]:
                outfile.write(line)  
            else:  
                outfile.write("\t".join(new_row) + "\n")  

    copyfile(filename, countries_file)


def delete_country():
    country_delete = str(input("Que país deseja apagar [ISO]? "))
    fd, filename = tempfile.mkstemp()  

    found = False  
    with open(countries_file, 'r', encoding='utf-8') as infile, open(fd, 'w',
                                                                     encoding='utf-8') as outfile:  
        lines = infile.readlines()  

        for line in lines:  
            fields = line.split("\t")
            if country_delete != fields[0]:  
                outfile.write(line)  
            else:  
                print("Deleted " + line)  
                found = True  

    if not found:  
        print("The country with ISO " + country_delete + " doesnt exist")
    else:  
        copyfile(filename, countries_file)


def list_countries():
    with open(countries_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines()):
            fields = line.split("\t")
            print(fields[0], fields[4])
            if i > 0 and i % items_per_listing == 0:
                opt = input("Prima qq tecla para continuar, N para sair... ")
                if opt == 'N':
                    return


def search_by():
    with open(countries_file, 'r', encoding='utf-8') as file:
        fields = file.readline().strip().split("\t")
        for i, field in enumerate(fields):
            print(str(i) + " -> " + field)

        try:
            choice = int(input("Field: "))
        except ValueError:
            print("Invalid option", end='\n\n')
            return

        query = input("Query: ")

        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.split("\t")[choice] == query:
                print(line)
                return
    print("Not found")


def list_by():
    with open(countries_file, 'r', encoding='utf-8') as file:
        fields = file.readline().strip().split("\t")
        for i, field in enumerate(fields):
            print(str(i) + " -> " + field)

        try:
            choice = int(input("Field: "))
        except ValueError:
            print("Invalid option", end='\n\n')
            return

        lines = file.readlines()
        for i, line in enumerate(lines):
            print(line.split("\t")[choice])
            if i > 0 and i % items_per_listing == 0:
                opt = input("Prima qq tecla para continuar, N para sair... ")
                if opt == 'N':
                    return


def read_countries():
    countries = {}
    names = {}

    with open(countries_file, 'r', encoding='utf-8') as file:
        file.readline()
        for line in [x.split("\t") for x in file.readlines()]:
            iso = line[0]
            name = line[4]
            names[iso] = name
            neighbours = line[17].rstrip('\n')
            if len(neighbours) > 0:
                countries[iso] = neighbours.split(",")

    return countries, names


def shortest_path():
    graph, names = read_countries()

    src = input("From: ")

    if src not in graph:
        print("Country with ISO " + src + " doesnt exist")
        return

    dst = input("To: ")

    if dst not in graph:
        print("Country with ISO " + dst + " doesnt exist")
        return

    shortest_paths = {src: (None, 0)}
    current_node = src
    visited = set()
    while current_node != dst:
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            print("No path between " + src + " and " + dst)
            return
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    path = path[::-1]
    print(" -> ".join([names[country] for country in path]))


menu_options = [
    ("List All", list_countries),
    ("List By...", list_by),
    ("Search By...", search_by),
    ("Insert...", insert_country),
    ("Delete...", delete_country),
    ("Update...", update_country),
    ("Shortest Path...", shortest_path),
    ("Exit", exit, 0)
]


def menu_global():
    if not os.path.isfile(countries_file):
        with open(countries_file, 'w+', encoding='utf-8') as file:
            file.write("\t".join(fields.keys()) + "\n")

    while True:
        for i, opt in enumerate(menu_options):
            print(i, " - ", opt[0])
        try:
            option = int(input("$ "))
        except ValueError:
            print("Invalid option", end='\n\n')
            continue

        func = menu_options[option]

        if len(func) < 3:  
            func[1]()
        else:
            func[1](func[2])


menu_global()
