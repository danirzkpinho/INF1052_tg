from player_validation import *
import os
import tempfile
from shutil import copyfile

players_file = "data/players.txt"
items_per_listing = 10

fields = {
    'Nome': validate_name,
    'DataDeNascimento': validate_date,
    'Posicao': validate_position,
    'Clube': validate_club,
    'Email': validate_email,
    'Contacto': validate_contact,
    'Agente': validate_agent,
    'Estado': validate_state,
    'Vencimento': validate_salary}

posicoes_campo = ["GL = Guarda Redes", "L = Libero", "LE = Lateral Esquerdo", "LD = Lateral Direito", "T = Trinco", "MAL = Medio Ala", "MAT = Medio Atacante", "MC = Medio Centro", "MCL = Medio Campista Lateral", "MA = Meia-Atacante", "AL = Avançado Lateral / Extremo", "SA = Segundo Avançado", "PL = Ponta de lança"]

def insert():
    new_row = []
    print(posicoes_campo)
    with open(players_file, 'r', encoding='utf-8') as file:
        field_names = [x.strip() for x in file.readline().split("\t")]

        print(field_names)

        for field in field_names:
            new_field = input(field + ": ")
            while not fields[field](new_field):
                print("Invalid Input:", field, "cannot be", new_field, end='\n\n')
                new_field = input(field + " -> ")
            new_row.append(new_field)

    with open(players_file, 'a', encoding='utf-8') as file:
        file.write("\t".join(new_row) + "\n")


def update():
    print(posicoes_campo)
    player_modify = str(input("Que jogador pretende alterar [nome]? "))
    old_row = []
    with open(players_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

        for line in lines:
            f = line.split("\t")
            if player_modify == f[0]:
                old_row = f
                break

    if len(old_row) == 0:
        print("The player with name " + player_modify + " doesnt exist")
        return

    new_row = []

    print("\nPara manter o valor anterior, deixar em branco\n")

    with open(players_file, 'r', encoding='utf-8') as file:
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
    with open(players_file, 'r', encoding='utf-8') as infile, open(fd, 'w',
                                                                     encoding='utf-8') as outfile:
        lines = infile.readlines()

        for line in lines:
            f = line.split("\t")
            if old_row[0] != f[0]:
                outfile.write(line)
            else:
                outfile.write("\t".join(new_row) + "\n")

    copyfile(filename, players_file)


def delete():
    player_delete = str(input("Que jogador deseja apagar [Nome]? "))
    fd, filename = tempfile.mkstemp()

    found = False
    with open(players_file, 'r', encoding='utf-8') as infile, open(fd, 'w',
                                                                   encoding='utf-8') as outfile:
        lines = infile.readlines()

        for line in lines:
            fields = line.split("\t")
            if player_delete != fields[0]:
                outfile.write(line)
            else:
                print("Deleted " + line)
                found = True

    if not found:
        print("O jogador " + player_delete + " nao existe")
    else:
        copyfile(filename, players_file)


def search_by():
    print(posicoes_campo)
    with open(players_file, 'r', encoding='utf-8') as file:
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


def quicksort(alist, i):
    quicksorthelper(alist, 0, len(alist) - 1, i)


def quicksorthelper(alist, first, last, i):
    if first < last:
        splitpoint = partition(alist, first, last, i)

        quicksorthelper(alist, first, splitpoint - 1, i)
        quicksorthelper(alist, splitpoint + 1, last, i)


def partition(alist, first, last, i):
    pivotvalue = alist[first][i]

    leftmark = first + 1
    rightmark = last

    done = False
    while not done:

        while leftmark <= rightmark and alist[leftmark][i] <= pivotvalue:
            leftmark = leftmark + 1

        while alist[rightmark][i] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp

    return rightmark


def sort_by():
    with open(players_file, 'r', encoding='utf-8') as file:
        fields = file.readline().strip().split("\t")
        for i, field in enumerate(fields):
            print(str(i) + " -> " + field)

        try:
            choice = int(input("Field: "))
            if choice < 0 or choice >= len(fields):
                print("Invalid option", end='\n\n')
                return

            lines = [line.strip().split("\t") for line in file.readlines()]

            quicksort(lines, choice)

            for line in lines:
                print(line)

        except ValueError:
            print("Invalid option", end='\n\n')
            return
        print(posicoes_campo)

def list_all():
    with open(players_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines()):
            fields = line.split("\t")
            print(" ".join(fields))
            if i > 0 and i % items_per_listing == 0:
                opt = input("Prima qq tecla para continuar, N para sair... ")
                if opt == 'N':
                    return


menu_options = [
    ("Insert", insert),
    ("Update", update),
    ("Delete", delete),
    ("Search by...", search_by),
    ("Sort by...", sort_by),
    ("List all", list_all),
    ("Exit", exit, 0)
]


def menu_global():
    if not os.path.isfile(players_file):
        with open(players_file, 'w+', encoding='utf-8') as file:
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
