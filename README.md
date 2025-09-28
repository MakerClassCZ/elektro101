# 🚀 MakerClass - Kurz programování pro Raspberry Pi Pico

> **Kompletní kurz programování pro začátečníky až pokročilé**  
> Naučte se programovat Raspberry Pi Pico pomocí CircuitPython a vytvářet vlastní elektronické projekty!

## 📚 O kurzu

MakerClass je progresivní kurz programování, který vás provede od základů až po pokročilé projekty s Raspberry Pi Pico. Každý level staví na předchozích znalostech a postupně vás seznámí s různými senzory, displeji a elektronickými komponentami.

## 🎯 Co se naučíte

- **Základy programování** v CircuitPython
- **Práce s GPIO piny** a digitálními vstupy/výstupy
- **Analogové senzory** a jejich čtení
- **Displeje a LED matice** pro vizuální výstup
- **Komunikace** přes I2C, SPI a další protokoly
- **Praktické projekty** jako parkovací senzor, meteostanice, hry
- **Fyzikální simulace** a herní mechaniky

## 🔧 Požadavky

### Hardware
- **Raspberry Pi Pico** (nebo Pico W/Pico2/Pico2 W)
- **Breadboard** a propojovací vodiče
- **Základní komponenty** (LED, rezistory, tlačítka)
- **Senzory a moduly** (podle jednotlivých levelů)

### Software
- **CircuitPython** firmware na Pico
- **Mu Editor** nebo **Thonny** pro programování
- **VS Code** s [CircuitPython rozšířením](https://marketplace.visualstudio.com/items?itemName=wmerkens.vscode-circuitpython-v2) pro pokročilé uživatele
- **Knihovny** (automaticky se stáhnou při prvním spuštění)

## 🛒 Potřebný materiál

### Základní vybavení (osvědčené tipy)
- **[Breadboard](https://www.digikey.cz/cs/products/detail/busboard-prototype-systems/BB830/19200392)** - kvalitní, pro zapojování obvodů
- **[Propojovací vodiče](https://www.digikey.cz/cs/products/detail/adafruit-industries-llc/4635/13157993)** - kvalitní silikonové
- **[Vývojová deska s podporou CircuitPython](https://pajenicko.cz/raspberry-pi-pico-rp2040-32bit-arm-cortex-m0)** - RPi Pico/Pico W/Pico2/Pico2 W
- **[uŠup/StemmaQT/Qwiic propojovací kabely](http://laskakit.cz/--sup--stemma-qt--qwiic-jst-sh-4-pin-kabel-20cm/)** - pro jednoduché propojování podporovaných senzorů, varianty 
- **[uŠup/StemmaQT/Qwiic připojovací kabel](https://www.laskakit.cz/--sup--stemma-qt--qwiic-jst-sh-4-pin-kabel-dupont-samec/)** - pro připojení k breadboardu (případně i female varianta)


### Základní komponenty
- **[Rezistory 330Ω](https://pajenicko.cz/metal-oxidovy-rezistor-330r-14w-1-percent)** - pro LED diody, 2x
- **[LED diody](https://www.laskakit.cz/led-dioda-5mm/)** - červené LED, 2x
- **[Tlačítko](https://www.laskakit.cz/mikrospinac-tc-1212t-12x12x7-3mm/)** - pro interaktivní ovládání
- **[Potenciometr 10kΩ](https://www.laskakit.cz/potenciometr-10kohm-linearni/)** - pro analogové vstupy
- **[Rotační enkodér](https://www.laskakit.cz/keyes-ky-040-rotacni-encoder-s-tlacitkem/)** - pro přesné ovládání
- **[Pasivní bzučák](https://www.laskakit.cz/keyes-ky-006-pasivni-bzucak/)** - pro generování tónů

### Motory a serva
- **[Servo motor SG90](https://pajenicko.cz/plastove-micro-servo-sg90-9g-180)**

### Senzory
- **[Modul s fotorezistorem](https://www.laskakit.cz/arduino-svetelny-senzor--4-pin-modul/)** - detekce osvětlení
- **[Ultrazvukový senzor HC-SR04](https://pajenicko.cz/ultrazvukovy-meric-vzdalenosti-hc-sr04)** - pro měření vzdálenosti
- **[DHT11](https://www.laskakit.cz/arduino-senzor-teploty-a-vlhkosti-vzduchu-dht11--modul/)** - teplotní a vlhkostní senzor (volitelně)
- **[DS18B20](https://www.laskakit.cz/digitalni-cidlo-teploty-dallas-ds18b20--modul/)** - přesný teplotní senzor, 2ks pro test sběrnice
- **[SHT40](https://www.laskakit.cz/laskakit-sht40-senzor-teploty-a-vlhkosti-vzduchu/)** - pokročilý teplotní a vlhkostní senzor, i2c
- **[MPU6050](https://www.laskakit.cz/laskakit-oled-displej-128x64-0-96-i2c/?variantId=13843)** - akcelerometr s gyroskopem

### Displeje a LED
- **[OLED displej SSD1306 128x64](https://www.laskakit.cz/laskakit-oled-displej-128x64-0-96-i2c/?variantId=13843)** - pro zobrazení dat
- **[NeoPixel Matrix 4x4](https://pajenicko.cz/inteligentni-rgb-led-modul-s-16x-ws2812-neopixel-ctverec)** - barevná LED matice



## 📁 Struktura kurzu

### 🟢 **Základní techniky (1-5)**
| Level | Název | Popis | Komponenty |
|-------|-------|-------|------------|
| **1** | Blikání LED | První program - ovládání GPIO | LED, rezistor |
| **2** | Tlačítko a LED | Interaktivní ovládání | LED, tlačítko, rezistory |
| **3** | Asynchronní programování | Pokročilé časování | LED, tlačítko |
| **4** | PWM řízení jasu | Analogové výstupy | LED, rezistor |
| **5** | Potenciometr | Analogové vstupy | LED, potenciometr, rezistor |

### 🟡 **Jednoduché moduly a senzory (6-10)**
| Level | Název | Popis | Komponenty |
|-------|-------|-------|------------|
| **6** | Rotární enkodér | Čtení otáček | LED, rotární enkodér |
| **7** | Servomotor | Precizní ovládání | Servomotor |
| **8** | Melodie a zvuky | Zvukové výstupy | Bzučák |
| **9** | Časovač s alarmem | Pokročilé časování | LED, bzučák |
| **10** | Parkovací senzor | Ultrazvukové měření | Bzučák, HC-SR04 |

### 🔴 **Pokročilejší projekty (11-15)**
| Level | Název | Popis | Komponenty |
|-------|-------|-------|------------|
| **11** | Teplotní senzory | I2C komunikace | DHT11, DS18B20, SHT40 |
| **12** | Více na I2C | I2C, Objevování zařízení | SHT40, OLED display |
| **13** | Akcelerometr | 3D pohyb | MPU6500/MPU6050, OLED display |
| **14** | NeoPixel matice | Barevné LED displeje | NeoPixel 4x4 |
| **15** | Kulička na náklonu | Herní fyzika | NeoPixel, MPU6500, bzučák |

## 🚀 Jak začít

### 1. Instalace CircuitPython
```bash
# Stáhněte CircuitPython firmware z oficiálních stránek
# https://circuitpython.org/downloads
# Najděte Raspberry Pico a stáhněte verzi 9.x
# Nasaďte na Pico (přetažením .uf2 souboru)
```

### 2. První spuštění
```python
# V level01/code.py najdete první program
# Otevřete v Mu Editor nebo Thonny
# Uložte na Pico jako code.py
```

### 3. Postupujte postupně
- Začněte **Level 1** - blikání LED
- Postupujte po levelu až k **Level 15**
- Každý level má vlastní `code.py` soubor
- Pokud je v levelu více souborů, `code.py` je nejjednodušší řešení a další ukazují efektivnější postupy 
- Dodržujte zapojení podle komentářů v kódu
- Po skončení levelu ihned nerozpoujujte, mnoho levelů na sebe v zapojení navazuje
- Na připojení CIRCUITPY disk můžete nahrát celou složku `code.py`, jsou v ní všechny potřebné moduly pro kurz

### 4. Rozšířené příklady
Některé levely obsahují rozšířené příklady ve složkách `extra-[název]/`, například:
- **extra-keypad/**, **extra-async/** - pokročilé techniky programování
- **extra-rotaryio/**, **extra-melodie/** - vylepšené knihovny a funkce
- **extra-ds18b20/**, **extra-dht11/**, **extra-sht40/** - různé typy senzorů
- **extra-demo/**, **extra-interactive/**, **extra-encoder/** - pokročilé projekty

## 🔌 Zapojení obvodů

Každý level obsahuje detailní popis zapojení v komentářích kódu:

```python
"""
ZAPOJENÍ OBVODU:
- LED anoda (+) → GP00
- LED katoda (-) → rezistor 330Ω → GND
"""
```

## 📖 Užitečné odkazy

- [**CircuitPython dokumentace**](https://docs.circuitpython.org/)
- [**Raspberry Pi Pico datasheet**](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- [**Adafruit knihovny**](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)
- [**Mu Editor**](https://codewith.mu/)
- [**VS Code CircuitPython rozšíření**](https://marketplace.visualstudio.com/items?itemName=wmerkens.vscode-circuitpython-v2) - profesionální vývojové prostředí

## 🤝 Přispívání

Pokud najdete chybu nebo máte návrh na vylepšení:

1. **Fork** repozitáře
2. Vytvořte **feature branch**
3. **Commit** změny
4. **Push** do branch
5. Otevřete **Pull Request**

## 📄 Licence

Tento kurz je dostupný pod licencí **MIT**. Můžete ho volně používat pro vzdělávací účely i komerční projekty.

## 🙏 Poděkování

- **Raspberry Pi Foundation** za skvělé hardware
- **Adafruit** za CircuitPython a knihovny
- **[Pájeníčko](https://pajenicko.cz/)** a **[LaskaKit](https://www.laskakit.cz/)** za pomoc s pořízením hardware a elektronických komponent
- A samozřejmě mé **[skvělé ženě](https://x.com/xamulka)**, která mě během příprav ohromně podporovala ❤!

---

## 🎉 Začněte s programováním!

**Level 1** je připraven a čeká na vás! Připojte LED, spusťte kód a uvidíte první světýlko blikat. 

> *"Každý expert byl jednou začátečník. Začněte dnes a zítra budete programovat vlastní projekty!"*

---

**📧 Kontakt:** Vláďa Smitka[vlada@makerclass.cz]  
**🌐 Web:** [https://makerclass.cz]  

