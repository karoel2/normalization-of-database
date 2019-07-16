from copy import copy
baza = []
temp = []
bfunkcje = []
with open('test.txt') as file:
    baza = file.readline().strip().split(',')
    for i in range(len(baza)):
        baza[i] = "".join(baza[i].split())
    for line in file:
        temp = line.strip().split(' -> ')
        temp[0] = temp[0].strip().split(',')
        temp[1] = temp[1].strip().split(',')
        bfunkcje.append([temp[0], temp[1]])

wszystkie = []
max = 2**len(baza)
med = max

#kombinacje {A} {A,B} {B,C}
for i in range(max-1):
    wszystkie.append(set())

for item in baza:
    med /= 2
    min = 0
    while int(min + med) < int(max):
        for i in range(int(min), int(min + med)):
            wszystkie[i].add(item)
        min += 2*med

print()


#dopelnienia A+, A,B+
wszystkie.sort(key = len)
lista = []
klucze = []
for item in wszystkie:
    lista.append(copy(item))

for i in range(len(wszystkie)):
    wartownik = 1
    while wartownik != 0:
        wartownik = 0
        for fun in bfunkcje:
            if set(fun[0]).issubset(wszystkie[i]) and not(set(fun[1]).issubset(wszystkie[i])):
                wszystkie[i].update(set(fun[1]))
                wartownik = 1
                break
    if wszystkie[i] ==  set(baza):
        klucze.append(copy(lista[i]))



q = len(baza)
for item in klucze:
    if q > len(item):
        q = len(item)


kluczowe = set()
kandydaci = []
for item in klucze:
    if len(item) == q:
        kandydaci.append(item)
        kluczowe = kluczowe.union(item)
niekluczowe = set(baza).difference(kluczowe)



#baza minimalna z A -> B,C  na  A -> B   i    A -> C
baza_min_f = []
for item in bfunkcje:
    baza_min_f.append(copy(item))
short = [] #A -> B,C
long = [] #A -> B   i    A -> C
for item in baza_min_f:
    if len(item[1]) != 1:
        temp = item[1]
        long.append(item)
        for thing in temp:
            short.append([copy(item[0]), [thing]])

for item in long:
    baza_min_f.remove(item)
baza_min_f += short

#baza minimalna F+ ?= G+




def zawiera(x, y):
    nowe_fc = copy(x)
    nbaz = set(copy(y))
    wartownik = 1
    while wartownik != 0:
        wartownik = 0
        for item in nowe_fc:
            if set(item[0]).issubset(nbaz) and not(set(item[1]).issubset(nbaz)):
                nbaz.update(set(item[1]))
                wartownik = 1
                break
    return nbaz


def sprfunkcje(index, fun):
    x = copy(index[0])
    y = copy(index[1])
    f = copy(fun)
    if set(y).issubset(zawiera(f, x)):
        return True
    else:
        return False

def sprawdz(funkcje):
    wartownik1 = True
    wartownik2 = True
    for item in funkcje:
        if sprfunkcje(item, baza_min_f) == False:
            wartownik1 = False
    for item in baza_min_f:
        if sprfunkcje(item, funkcje) == False:
            wartownik2 = False
    if wartownik1 == wartownik2 == True:
        return True
    else:
        return False


 # A,B -> C   na   A -> C   lub   B -> C
wartownik = 1
while wartownik != 0:
    wartownik = 0
    for item in baza_min_f:
        if len(item[0]) != 1:
            for litera in item[0]:
                nowe_f = []
                for it in baza_min_f:
                    nowe_f.append(copy(it))
                nowe_f.remove(item)
                temp = copy(item[0])
                temp.remove(litera)
                nowe_f.append([temp, item[1]])

                if sprawdz(nowe_f):
                    baza_min_f = copy(nowe_f)
                    wartownik = 1
                    break


wartownik = 1
while wartownik != 0:
    wartownik = 0
    for item in baza_min_f: # A -> C  i   B -> C  na  B -> C
        nowe_f = []
        for it in baza_min_f:
            nowe_f.append(copy(it))
        nowe_f.remove(item)

        nowa_baza = set()
        for it in nowe_f:
            nowa_baza.update(it[0])

        if sprawdz(nowe_f):
            baza_min_f = copy(nowe_f)
            wartownik = 1
            break
narusza = []
PN2 = "Tak"

def czy2pn(kluczowe, baza_min_f):#W podanym schemacie istnieje przyjemniej jedna częściowa zależność nowe_fcyjna, która narusza 2PN.
    k = []
    global PN2

    for item in kluczowe:
        k.append(set(copy([item])))

    b = copy(baza_min_f)
    for item in k:
        wartownik = 1
        while wartownik != 0:
            wartownik = 0
            for fun in b:
                if set(fun[0]).issubset(item) and not(set(fun[1]).issubset(item)):
                    item.update(set(fun[1]))
                    wartownik = 1
                    temp = bool(item.intersection(set(niekluczowe)))
                    if temp == True:
                        narusza.append(copy(fun))
                        PN2 = "Nie"#, {}".format(fun)

                    break
        temp = bool(item.intersection(set(niekluczowe)))

czy2pn(kluczowe, baza_min_f)


PN3 = 'Tak'
if PN2[0] == 'N':
    PN3 = 'Nie'#, nie jest 2PN'
for item in baza_min_f: # lewa nadkluczem 2.
    #print(item[0])
    bb = False
    for it in kandydaci:
        if it.issubset(set(item[0])):
            if len(set(item[0]).difference(it)) != 0:
                bb = True
    if set(item[1]).issubset(kluczowe):
        bb = True
    if bb == False:
        PN3 = "Nie"

#print(baza_min_f)# prawa kluczowym 3.
for item in baza_min_f:
    if set(item[1]).issubset(kluczowe):
        PN3 = "Nie"




def zawiera(x, y, w):
    nowe_fc = copy(x)
    nbaz = set(copy(y))
    wartownik = 1
    while wartownik != 0:
        wartownik = 0
        for item in nowe_fc:
            if set(item[0]).issubset(nbaz) and not(set(item[1]).issubset(nbaz)):
                #print(nbaz, end="   ")
                nbaz.update(set(item[1]))
                #print(nbaz)
                wartownik = 1
                break


def sprfunkcje():#trywialne 1,
    for item in baza_min_f:
        zawiera(baza_min_f, item[0], item[1])

sprfunkcje()









#print("B.min:", baza_min_f)



def dekonstrukcja(x, y):
    nowe_fc = copy(x)
    nbaz = set(copy(y))
    fwyko = []
    sba = set()
    wartownik = 1
    while wartownik != 0:
        wartownik = 0
        for item in nowe_fc:
            if set(item[0]) == (nbaz) and not((set(item[1]).issubset(nbaz)) or (set(item[1]).issubset(sba))):
                sba.update(set(item[1]))
                fwyko.append([item[0], item[1]])
                wartownik = 1
                break
    nbaz.update(sba)

    return [nbaz, fwyko]


#dekompozycja
dek = []
for f in baza_min_f:
    dek.append(dekonstrukcja(baza_min_f, f[0]))

wart = False
for item in dek:
    for key in kandydaci:
        if key.issubset(set(item[0])):
            wart = True
if wart == False:
    dek.append([kandydaci[0], None])



wartownik = 1
while wartownik != 0:
    wartownik = 0
    for item in dek:
        temp = copy(dek)
        temp.remove(item)
        for it in temp:
            if set(it[0]).issubset(set(item[0])) :
                wartownik = 1
                for i in it[1]:
                    item[1].append(i)
                dek.remove(it)



print("Atrybuty kluczowe: ", end='')
print(*kluczowe, sep=', ')
print("Atrybuty niekluczowe: ", end='')
print(*niekluczowe, sep=', ')
print("F_min = ", end='')
for item in baza_min_f:
    print(*item[0], "->", *item[1], end="; ")
print()
print('2PN:', PN2)
print('3PN:', PN3)
print("Synteza do 3PN:")
for item in dek:
    print('(', end='')
    print(*item[0], end="")
    print(')  :  ', end='')

    if item[1] == None:
        print("(brak)")
    else:
        jup = set()
        for thing in item[1]:
            jup.update(['{} -> {}'.format(thing[0], thing[1])])
        for i in jup:

            print(i.replace('[', '').replace(']', '').replace("'", '').replace(", ", ','), sep='', end='; ')


        print()

print()
