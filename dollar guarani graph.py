from sys import float_repr_style
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import datetime as dt 

df= pd.read_csv(r"C:\Users\Lolo\Downloads\Datos_históricos_USD_PYG.csv")
df.head()
df.info()
df["Fecha"]=pd.to_datetime(df["Fecha"])
df["Último"]=df["Último"].str.replace(".","")
df["Último"]=df["Último"].str.replace(",",".").astype(float)
df["Apertura"]=df["Apertura"].str.replace(".","")
df["Apertura"]=df["Apertura"].str.replace(",",".").astype(float)
df["% var."]=df["% var."].str.replace("%","")
df["% var."]=df["% var."].str.replace(",",".").astype(float)

df["promedio"]=(df["Último"]+df["Apertura"])/2
df["promedio"]
guarani_promedio=df[["Fecha","promedio","% var."]].copy()
guarani_promedio.sort_values('Fecha', inplace=True)
guarani_promedio.reset_index(drop=True, inplace=True)
guarani_promedio.head()


plt.plot(guarani_promedio['Fecha'], guarani_promedio['promedio'],)
plt.show()


plt.figure(figsize=(9,6))

plt.subplot(3,2,1)
plt.plot(guarani_promedio['Fecha'], guarani_promedio['promedio'])
plt.title('Original values', weight='bold')
for i, rolling_mean in zip([2, 3, 4, 5, 6],
                           [7, 10, 30, 100, 365]):
    plt.subplot(3,2,i)
    plt.plot(guarani_promedio['Fecha'],
             guarani_promedio['promedio'].rolling(rolling_mean).mean())
    plt.title('Rolling Window:' + str(rolling_mean), weight='bold')
    
plt.tight_layout() # Auto-adjusts the padding between subplots
plt.show()

guarani_promedio["30"]=guarani_promedio['promedio'].rolling(30).mean()
guarani_promedio["año"]=guarani_promedio['Fecha'].dt.year
guarani_promedio["mes"]=guarani_promedio['Fecha'].dt.month

lugo_franco = guarani_promedio.copy( )[guarani_promedio['año'] < 2014 ]
lugo_franco.head()
lugo_franco.tail()
lugo_franco = lugo_franco.drop(lugo_franco[(lugo_franco.año == 2013) & (lugo_franco.mes > 8)].index)
lugo_franco.describe()
lugo_franco

cartes = guarani_promedio.copy()[(guarani_promedio['Fecha'].dt.year >= 2013) & (guarani_promedio['Fecha'].dt.year < 2019)]
cartes = cartes.drop(cartes[(cartes.año == 2013) & (cartes.mes < 9)].index)
cartes = cartes.drop(cartes[(cartes.año == 2018) & (cartes.mes > 8)].index)
cartes.describe()
cartes
abdo = guarani_promedio.copy()[(guarani_promedio['Fecha'].dt.year >= 2018) & (guarani_promedio['Fecha'].dt.year < 2023)]
abdo=abdo.drop(abdo[(abdo.año == 2018) & (abdo.mes < 9)].index)
abdo
abdo.describe()



### Adding the FiveThirtyEight style
style.use('fivethirtyeight')

### Adding the subplots
plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2,3,1)
ax2 = plt.subplot(2,3,2)
ax3 = plt.subplot(2,3,3)
ax4 = plt.subplot(2,1,2)
axes = [ax1, ax2, ax3, ax4]

### Changes to all the subplots
for ax in axes:
    ax.set_ylim(3500, 8000)
    ax.set_yticks([3500, 4500, 5500, 6500,7500,8000])
    ax.set_yticklabels(['3,500', '4,500','5,500', '6,500',"7,500","8,000"],
                   alpha=0.3)
    

### Ax1: lugo_franco
ax1.plot(lugo_franco['Fecha'], lugo_franco['30'],
        color='#BF5FFF')
ax1.set_xticklabels(['2008',  '2009',  '2010', 
                     '2011',  '2012',  "2013"],
                   alpha=0.3)
ax1.text(14500,8300,'Lugo - Franco', fontsize=18, weight='bold',
        color='#BF5FFF')
ax1.text(14500, 8000,'(2008-2013)', weight='bold',
        alpha=0.3)
ax1.grid(b=True, which='major', color='	#B5B5B5', linestyle='-',alpha=0.3)

### Ax2: cartes
ax2.plot(cartes['Fecha'], cartes['30'],
        color='#ffa500')
ax2.set_xticklabels(['2013', '2014', '2015', 
                     '2016', '2017',"2018"],
                   alpha=0.3)
ax2.text(16300, 8300, 'Horacio Cartes', fontsize=18, weight='bold',
        color='#ffa500')
ax2.text(16300, 8000, '(2013-2018)', weight='bold',
         alpha=0.3)
ax2.grid(b=True, which='major', color='	#B5B5B5', linestyle='-',alpha=0.3)

### Ax3: abdo
ax3.plot(abdo['Fecha'], abdo['30'],
        color='#00B2EE')
ax3.set_xticklabels(["",'2018', '', '2019', '', '2020', '',
                     '2021', '', '2022'],
                   alpha=0.3)
ax3.text(18200, 8300, 'Mario Abdo', fontsize=18, weight='bold',
        color='#00B2EE')
ax3.text(18200, 8000, '(2018-2022)', weight='bold',
         alpha=0.3)
ax3.grid(b=True, which='major', color='	#B5B5B5', linestyle='-',alpha=0.3)
### Ax4: lugo-cartes-abdo
ax4.plot(lugo_franco['Fecha'], lugo_franco['30'],
        color='#BF5FFF')
ax4.plot(cartes['Fecha'], cartes['30'],
        color='#ffa500')
ax4.plot(abdo['Fecha'], abdo['30'],
        color='#00B2EE')
ax4.grid(b=True, which='major', color='	#B5B5B5', linestyle='-',alpha=0.3)
ax4.set_xticks([])


### Adding a title and a subtitle
ax1.text(13500, 8700, '''GUARANI-USD tipo de cambio bajo Lugo - Franco (2008 - 2013), Horacio Cartes (2013-2018),
y Mario Abdo (2018-2022)''',
         fontsize=18, weight='bold')


### Adding a signature
ax4.text(13400, 2850, '©Perspectiva' + ' '*103 + 'Fuente: Banco Central del Paraguay',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',
        size=14)

plt.show()
