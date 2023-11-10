import csv
import matplotlib.pyplot as plt
import pandas as pd

plik = open('shopping_behavior_updated.csv', 'r')
dane = []

def zadanie1_1(dane):
    sezon = [0, 0, 0, 0]
    for linijka in dane[1:]:
        # 1.1
        if linijka[9] == "Spring":
            sezon[0] += int(linijka[5])
        if linijka[9] == "Summer":
            sezon[1] += int(linijka[5])
        if linijka[9] == "Fall":
            sezon[2] += int(linijka[5])
        if linijka[9] == "Winter":
            sezon[3] += int(linijka[5])
    return sezon

def zadanie1_2(dane):
    kolory = {}
    for linijka in dane[1:]:
        if linijka[3] == 'Handbag':
            if linijka[8] in kolory:
                kolory[linijka[8]] += 1
            else:
                kolory[linijka[8]] = 1
    return kolory

def zadanie1_3(dane):
    mezczyzna_z_bluzka_xl = []
    for linijka in dane[1:]:
        if linijka[2] == 'Male' and int(linijka[1]) in range(18, 26) and linijka[3] == 'Blouse' and linijka[7] == 'XL':
            mezczyzna_z_bluzka_xl.append(linijka[0])
    return mezczyzna_z_bluzka_xl

def zadanie1_4(dane):
    rodzaj_ubran = {}
    for linijka in dane[1:]:
        if int(linijka[1]) in range(25, 46) and linijka[2] == 'Female':
            if linijka[3] in rodzaj_ubran:
                rodzaj_ubran[linijka[3]] += 1
            else:
                rodzaj_ubran[linijka[3]] = 1
    return rodzaj_ubran

def zadanie1_5(dane):
    wiek = {}
    for linijka in dane[1:]:
        if linijka[1] in wiek:
            wiek[linijka[1]] += 1
        else:
            wiek[linijka[1]] = 1
    return wiek

#1.6 najczęściej kupowane kategorie przez mężczyzn i kobiety
def zadanie1_6(dane):
    kategoria_mezczyzni = {}
    kategoria_kobiety = {}
    for linijka in dane[1:]:
        if linijka[2] == 'Male':
            if linijka[4] in kategoria_mezczyzni:
                kategoria_mezczyzni[linijka[4]] += 1
            else:
                kategoria_mezczyzni[linijka[4]] = 1
        elif linijka[2] == 'Female':
            if linijka[4] in kategoria_kobiety:
                kategoria_kobiety[linijka[4]] += 1
            else:
                kategoria_kobiety[linijka[4]] = 1
    return kategoria_mezczyzni, kategoria_kobiety


def zadanie2_1(df):
    return df.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()

def zadanie2_2(df):
    sukienki = df[df['Item Purchased'] == 'Dress']
    return sukienki['Location'].value_counts().reset_index()

def zadanie2_3(df):
    plec = df["Gender"] == "Female"
    wiek = df["Age"] < 40
    subskrypcja = df["Subscription Status"] == "Yes"
    ilosc_zakupow = df["Previous Purchases"] > 15
    wynik = df[plec & wiek & ilosc_zakupow & subskrypcja]
    if wynik.empty:
        return "Nie ma takiej osoby"
    else:
        return wynik

def zadanie2_4(df):
    return df.groupby('Age')['Payment Method'].value_counts().reset_index()

def zadanie2_5(df):
    return df.groupby('Gender')['Shipping Type'].value_counts().reset_index()

def zadanie2_6(df):
    return df.groupby('Gender')['Review Rating'].mean().reset_index()

#wczytywanie pliku csv
#bez pandas
for linia in plik:
    dane.append(linia.split(','))
#z uzyciem pandas
df = pd.read_csv('shopping_behavior_updated.csv')

#1.1
sezon = zadanie1_1(dane)
print(f"1.1\nWiosna: {sezon[0]}\nLato: {sezon[1]}\nJesien: {sezon[2]}\nZima: {sezon[3]}\n")

#1.2
top3 = zadanie1_2(dane)
top3 = sorted(top3.items(), key = lambda x:x[1], reverse = True)
print("1.2\n3 najczęściej kupowane kolory torebek:")
for kolor, licznik in top3[:3]:
    print(f"{kolor}: {licznik}")

#1.3
mezczyzna_z_bluzka_xl = zadanie1_3(dane)
print("1.3\nMężczyźni w wieku 18-25, którzy kupili bluzkę XL:")
for item in mezczyzna_z_bluzka_xl:
    print(f"ID: {item}")

#1.4
labels = []
wartosci = []
rodzaj_ubran = zadanie1_4(dane)
print("1.4\nWykres ubrań kupowanych przez kobiety w wieku 25-45:")
for ubranie, licznik in rodzaj_ubran.items():
    labels.append(ubranie)
    wartosci.append(licznik)
fig, ax = plt.subplots()
ax.pie(wartosci, labels = labels, autopct = '%1.1f%%')
plt.show()

# 1.5
lata = []
licznik = []
wiek = zadanie1_5(dane)
wiek = sorted(wiek.items())
wiek_lista = [int(pozycja[0]) for pozycja in wiek for _ in range(pozycja[1])]
plt.hist(wiek_lista, bins= 53, edgecolor='black')
plt.xlabel('Wiek')
plt.ylabel('Liczba osób')
plt.title('Rozkład wieku')
print("1.5\nHistogram rozkładu wieku klientów:")
plt.show()

#1.6
kategorie = zadanie1_6(dane)
kat_mez = kategorie[0]
kat_kob = kategorie[1]
kat_mez = sorted(kat_mez.items(), key = lambda x:x[1], reverse = True)
kat_kob = sorted(kat_kob.items(), key = lambda x:x[1], reverse = True)
print("1.6")
for kategoria, licznik in kat_mez[:1]:
    print(f'Najczesciej kupowana kategoria przez mężczyzn: {kategoria} z wynikiem {licznik}')
for kategoria, licznik in kat_kob[:1]:
    print(f'Najczesciej kupowana kategoria przez kobiety: {kategoria} z wynikiem {licznik}')

#2.1
print(f"2.1\nWydatki kupujących w podzaile na kategorię produktu:\n{zadanie2_1(df)}")

#2.2
print(f"2.2\nTop 5 miast, gdzie kupiono najwięcej sukienek:\n{zadanie2_2(df)[:5]}")

#2.3
print(f"2.3\nKobiety poniżej 40 roku życia z subskrypcją, które zrobiły więcej niż 15 zakupów:\n{zadanie2_3(df)}")

#2.4
print("2.4\nRozkład metod płatności w zależności od wieku")
dane2_4 = zadanie2_4(df)
pivot_dane2_4 = dane2_4.pivot(index = "Age", columns = 'Payment Method', values = 'count')
pivot_dane2_4.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Rozkład metod płatności w zależności od wieku')
plt.xlabel('Wiek')
plt.ylabel('Liczba transakcji')
plt.legend(title='Metoda płatności')
plt.show()

#2.5
print("2.5\nRodzaj dostawy w zależności od płci")
dane2_5 = zadanie2_5(df)
pivot_dane2_4 = dane2_5.pivot(index = "Gender", columns = 'Shipping Type', values = 'count')
pivot_dane2_4.T.plot.pie(subplots = True, autopct = '%1.1f%%', figsize = (18, 9), legend = True)
plt.axis('equal')
plt.title('Rodzaj dostawy w zależności od płci')
plt.legend(title='Rodzaj dostawy')
plt.show()

#2.6
print(f"2.6\nŚrednia ocen klientów w zależności od ich płci:\nŚrednia ocen dla mężczyzn: {zadanie2_6(df[df['Gender'] == 'Male'])['Review Rating'].values[0]}\nŚrednia ocen dla kobiet: {zadanie2_6(df[df['Gender'] == 'Female'])['Review Rating'].values[0]}")