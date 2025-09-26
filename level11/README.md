# Level 11 - Teplotní senzory

## Popis
Úvod do různých typů teplotních senzorů a jejich komunikačních protokolů. Naučíte se pracovat s vestavěnými i externími senzory.

## Zapojení obvodu
Různé varianty podle typu senzoru:

### Level 11A - Vestavěný senzor RP2040
- Žádné externí zapojení není potřeba! RP2040 má vestavěný teplotní senzor.

### Level 11B - DS18B20 (OneWire)
- DS18B20 modul připojte:
  - VDD k 3V3
  - GND k zemi (GND)
  - DQ k GP22

### Level 11C - DHT11/DHT22
- DHT11/DHT22 modul připojte:
  - VCC k 3V3
  - DATA k GP21
  - GND k zemi (GND)

### Level 11D - SHT40 (I2C)
- SHT40 modul připojte:
  - VDD k 3V3
  - GND k zemi (GND)
  - SDA k GP16 (I2C data - modrá)
  - SCL k GP17 (I2C clock - žlutá)

## Co se naučíte
- Vestavěný teplotní senzor mikrokontroléru
- OneWire protokol - komunikace jedním vodičem
- DHT komunikaci s přesným timingem
- I2C protokol - dvouvodičová sériová komunikace
- Různé přesnosti a rozsahy senzorů

## Soubory
- `code.py` - Vestavěný senzor RP2040 (Level 11A)
- `code-ds18b20.py` - DS18B20 senzor s OneWire protokolem (Level 11B)
- `code-dht11.py` - DHT11/DHT22 senzor s kombinovaným čtením teploty a vlhkosti (Level 11C)
- `code-sht40.py` - SHT40 senzor s I2C komunikací (Level 11D)

## Vylepšení
Každá varianta představuje jiný komunikační protokol:
1. **Vestavěný**: Přímé čtení bez externí komunikace
2. **OneWire**: Jednovodičová komunikace s možností připojení více senzorů
3. **DHT**: Vlastní protokol s kombinovaným čtením teploty a vlhkosti
4. **I2C**: Standardní dvouvodičová komunikace používaná v mnoha dalších senzorech
