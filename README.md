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
- **Raspberry Pi Pico** (nebo Pico W)
- **Breadboard** a propojovací vodiče
- **Základní komponenty** (LED, rezistory, tlačítka)
- **Senzory a moduly** (podle jednotlivých levelů)

### Software
- **CircuitPython** firmware na Pico
- **Mu Editor** nebo **Thonny** pro programování
- **VS Code** s [CircuitPython rozšířením](https://marketplace.visualstudio.com/items?itemName=wmerkens.vscode-circuitpython-v2) pro pokročilé uživatele
- **Knihovny** (automaticky se stáhnou při prvním spuštění)

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
| **12** | I2C skener | Objevování zařízení | I2C zařízení |
| **13** | Akcelerometr | 3D pohyb | MPU6500/MPU6050 |
| **14** | NeoPixel matice | Barevné LED displeje | NeoPixel 4x4 |
| **15** | Kulička na náklonu | Herní fyzika | NeoPixel, MPU6500, bzučák |

## 🚀 Jak začít

### 1. Instalace CircuitPython
```bash
# Stáhněte CircuitPython firmware z oficiálních stránek
# https://circuitpython.org/downloads
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
- Dodržujte zapojení podle komentářů v kódu

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

---

## 🎉 Začněte s programováním!

**Level 1** je připraven a čeká na vás! Připojte LED, spusťte kód a uvidíte první světýlko blikat. 

> *"Každý expert byl jednou začátečník. Začněte dnes a zítra budete programovat vlastní projekty!"*

---

**📧 Kontakt:** Vláďa Smitka[vlada@makerclass.cz]  
**🌐 Web:** [https://makerclass.cz]  

