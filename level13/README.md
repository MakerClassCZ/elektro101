# Level 13 - MPU6500 Gyroscope/Accelerometer s OLED displayem

## Popis
Použití IMU (Inertial Measurement Unit) senzoru pro měření pohybu a orientace. Naučíte se pracovat s 6-axis senzorem a zobrazovat data na displeji.

## Zapojení obvodu
Na I2C sběrnici připojíme dva moduly:

1) **GY-521 MPU6500 IMU senzor:**
   - VCC k 3V3
   - GND k zemi (GND)
   - SCL k GP17 (I2C clock - žlutá)
   - SDA k GP16 (I2C data - modrá)

2) **OLED Display SSD1306 128x64:**
   - VCC k 3V3
   - GND k zemi (GND)  
   - SDA k GP16 (I2C data - modrá) - SDÍLENO
   - SCL k GP17 (I2C clock - žlutá) - SDÍLENO

## Co se naučíte
- MPU6500/MPU6050 senzor
- Akcelerometr - měření zrychlení a gravitace
- Gyroskop - měření úhlové rychlosti  
- 6-axis snímání pohybu
- Kombinace více senzorů na I2C

## Soubory
- `code.py` - Zobrazení dat z gyroskopu a akcelerometru na OLED displeji
- `code-mpu6500.py` - Komunikace se senzorem "napřímo" bez knihovny přímým čtením I2C registrů

## Vylepšení
**code-mpu6500.py**:
- Používá přímé čtení I2C registrů místo knihovny
- Ukazuje, jak funguje komunikace na nízké úrovni
