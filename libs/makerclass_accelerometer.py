"""
`makerclass_accelerometer`
================================================================================

MakerClass CircuitPython library for MPU6500/MPU6050 6-DoF Accelerometer and Gyroscope.
Based on official Adafruit library, adapted for various chip variants.

* Author: MakerClass (based on Adafruit CircuitPython MPU6050 library)
* Original author: Bryan Siepert for Adafruit Industries

Supported chips:
- MPU6050 (WHO_AM_I = 0x68)
- MPU6500 (WHO_AM_I = 0x70)  
- MPU9250 (WHO_AM_I = 0x71)

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

# imports
__version__ = "1.0.0"
__repo__ = "https://github.com/makerclass/workshop"

from math import radians
from time import sleep

from adafruit_bus_device import i2c_device
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_struct_array import StructArray

try:
    from typing import Tuple
    from busio import I2C
except ImportError:
    pass

# Supported I2C addresses
_MPU_DEFAULT_ADDRESS = 0x68  # Default address (AD0 = LOW)
_MPU_ALT_ADDRESS = 0x69      # Alternative address (AD0 = HIGH)

# Supported WHO_AM_I values for different chips
_SUPPORTED_CHIPS = {
    0x68: "MPU6050",  # WHO_AM_I for MPU6050
    0x70: "MPU6500",  # WHO_AM_I for MPU6500  
    0x71: "MPU9250",  # WHO_AM_I for MPU9250
}

# Registers (same for all MPU variants)
_MPU_SELF_TEST_X = 0x0D      # Self test factory calibrated values register
_MPU_SELF_TEST_Y = 0x0E      # Self test factory calibrated values register
_MPU_SELF_TEST_Z = 0x0F      # Self test factory calibrated values register
_MPU_SELF_TEST_A = 0x10      # Self test factory calibrated values register
_MPU_SMPLRT_DIV = 0x19       # sample rate divisor register
_MPU_CONFIG = 0x1A           # General configuration register
_MPU_GYRO_CONFIG = 0x1B      # Gyro specfic configuration register
_MPU_ACCEL_CONFIG = 0x1C     # Accelerometer specific configration register
_MPU_FIFO_EN = 0x23          # FIFO Enable
_MPU_INT_PIN_CONFIG = 0x37   # Interrupt pin configuration register
_MPU_ACCEL_OUT = 0x3B        # base address for sensor data reads
_MPU_TEMP_OUT = 0x41         # Temperature data high byte register
_MPU_GYRO_OUT = 0x43         # base address for sensor data reads
_MPU_SIG_PATH_RESET = 0x68   # register to reset sensor signal paths
_MPU_USER_CTRL = 0x6A        # FIFO and I2C Master control register
_MPU_PWR_MGMT_1 = 0x6B       # Primary power/sleep control register
_MPU_PWR_MGMT_2 = 0x6C       # Secondary power/sleep control register
_MPU_FIFO_COUNT = 0x72       # FIFO byte count register (high half)
_MPU_FIFO_R_W = 0x74         # FIFO data register
_MPU_WHO_AM_I = 0x75         # Device ID register

STANDARD_GRAVITY = 9.80665


class ClockSource:
    """Allowed values for clock_source."""
    CLKSEL_INTERNAL_8MHz = 0  # Internal 8MHz oscillator
    CLKSEL_INTERNAL_X = 1     # PLL with X Axis gyroscope reference
    CLKSEL_INTERNAL_Y = 2     # PLL with Y Axis gyroscope reference
    CLKSEL_INTERNAL_Z = 3     # PLL with Z Axis gyroscope reference
    CLKSEL_EXTERNAL_32 = 4    # External 32.768kHz reference
    CLKSEL_EXTERNAL_19 = 5    # External 19.2MHz reference
    CLKSEL_RESERVED = 6       # Reserved
    CLKSEL_STOP = 7           # Stops the clock and keeps the timing generator in reset


class Range:
    """Allowed values for accelerometer_range."""
    RANGE_2_G = 0   # +/- 2g (default value)
    RANGE_4_G = 1   # +/- 4g
    RANGE_8_G = 2   # +/- 8g
    RANGE_16_G = 3  # +/- 16g


class GyroRange:
    """Allowed values for gyro_range."""
    RANGE_250_DPS = 0   # +/- 250 deg/s (default value)
    RANGE_500_DPS = 1   # +/- 500 deg/s
    RANGE_1000_DPS = 2  # +/- 1000 deg/s
    RANGE_2000_DPS = 3  # +/- 2000 deg/s


class Bandwidth:
    """Allowed values for filter_bandwidth."""
    BAND_260_HZ = 0  # Docs imply this disables the filter
    BAND_184_HZ = 1  # 184 Hz
    BAND_94_HZ = 2   # 94 Hz
    BAND_44_HZ = 3   # 44 Hz
    BAND_21_HZ = 4   # 21 Hz
    BAND_10_HZ = 5   # 10 Hz
    BAND_5_HZ = 6    # 5 Hz


class Rate:
    """Allowed values for cycle_rate."""
    CYCLE_1_25_HZ = 0  # 1.25 Hz
    CYCLE_5_HZ = 1     # 5 Hz
    CYCLE_20_HZ = 2    # 20 Hz
    CYCLE_40_HZ = 3    # 40 Hz


class MakerClassAccelerometer:
    """Universal driver for MPU6050/MPU6500/MPU9250 6-DoF accelerometer and gyroscope.

    :param ~busio.I2C i2c_bus: The I2C bus the device is connected to
    :param int address: The I2C device address. Defaults to 0x68

    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`MakerClassAccelerometer` class.
        First you will need to import the libraries to use the sensor:

        .. code-block:: python

            import board
            import makerclass_accelerometer

        Once this is done you can define your I2C object and define your sensor object:

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            mpu = makerclass_accelerometer.MakerClassAccelerometer(i2c)

        Now you have access to the :attr:`acceleration`, :attr:`gyro`
        and :attr:`temperature` attributes:

        .. code-block:: python

            acc_x, acc_y, acc_z = mpu.acceleration
            gyro_x, gyro_y, gyro_z = mpu.gyro
            temperature = mpu.temperature
    """

    def __init__(self, i2c_bus: I2C, address: int = _MPU_DEFAULT_ADDRESS) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        
        # Read WHO_AM_I and identify chip
        device_id = self._device_id
        if device_id not in _SUPPORTED_CHIPS:
            supported_list = ', '.join([f'{name} (0x{id:02x})' for id, name in _SUPPORTED_CHIPS.items()])
            raise RuntimeError(f"Unsupported chip! WHO_AM_I = 0x{device_id:02x}. Supported: {supported_list}")
      
        self.reset()
        self._sample_rate_divisor = 0
        self._filter_bandwidth = Bandwidth.BAND_260_HZ
        self._gyro_range = GyroRange.RANGE_500_DPS
        self._accel_range = Range.RANGE_2_G
        self._accel_scale = 1.0 / [16384, 8192, 4096, 2048][self._accel_range]
        sleep(0.100)
        self.clock_source = ClockSource.CLKSEL_INTERNAL_X  # set to use gyro x-axis as reference
        sleep(0.100)
        self.sleep = False
        sleep(0.010)

    def reset(self) -> None:
        """Reinitialize the sensor"""
        self._reset = True
        while self._reset is True:
            sleep(0.001)
        sleep(0.100)

        _signal_path_reset = 0b111  # reset all sensors
        sleep(0.100)

    _clksel = RWBits(3, _MPU_PWR_MGMT_1, 0)
    _device_id = ROUnaryStruct(_MPU_WHO_AM_I, ">B")

    _reset = RWBit(_MPU_PWR_MGMT_1, 7, 1)
    _signal_path_reset = RWBits(3, _MPU_SIG_PATH_RESET, 3)

    _gyro_range = RWBits(2, _MPU_GYRO_CONFIG, 3)
    _accel_range = RWBits(2, _MPU_ACCEL_CONFIG, 3)

    _filter_bandwidth = RWBits(2, _MPU_CONFIG, 3)

    _raw_accel_data = StructArray(_MPU_ACCEL_OUT, ">h", 3)
    _raw_gyro_data = StructArray(_MPU_GYRO_OUT, ">h", 3)
    _raw_temp_data = ROUnaryStruct(_MPU_TEMP_OUT, ">h")

    _cycle = RWBit(_MPU_PWR_MGMT_1, 5)
    _cycle_rate = RWBits(2, _MPU_PWR_MGMT_2, 6, 1)

    sleep = RWBit(_MPU_PWR_MGMT_1, 6, 1)
    """Shuts down the accelerometers and gyroscopes, saving power. No new data will
    be recorded until the sensor is taken out of sleep by setting to `False`"""
    
    sample_rate_divisor = UnaryStruct(_MPU_SMPLRT_DIV, ">B")
    """Sample rate divisor. See datasheet for details"""

    fifo_count = ROUnaryStruct(_MPU_FIFO_COUNT, ">H")
    """The number of bytes currently stored in the sensor's FIFO buffer"""

    @property
    def temperature(self) -> float:
        """Current temperature in °C"""
        raw_temperature = self._raw_temp_data
        # Temperature calibration (according to datasheet)
        temp = (raw_temperature / 340.0) + 36.53
        return temp

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """Acceleration X, Y, and Z axis data in m/s^2"""
        raw_data = self._raw_accel_data
        return self.scale_accel([raw_data[0][0], raw_data[1][0], raw_data[2][0]])

    def scale_accel(self, raw_data) -> Tuple[float, float, float]:
        """Scale raw X, Y, and Z axis data to m/s^2"""
        accel_x = (raw_data[0] * self._accel_scale) * STANDARD_GRAVITY
        accel_y = (raw_data[1] * self._accel_scale) * STANDARD_GRAVITY
        accel_z = (raw_data[2] * self._accel_scale) * STANDARD_GRAVITY
        return (accel_x, accel_y, accel_z)

    @property
    def gyro(self) -> Tuple[float, float, float]:
        """Gyroscope X, Y, and Z axis data in °/s"""
        raw_data = self._raw_gyro_data
        return self.scale_gyro((raw_data[0][0], raw_data[1][0], raw_data[2][0]))

    def scale_gyro(self, raw_data) -> Tuple[float, float, float]:
        """Scale raw gyro data to °/s"""
        raw_x = raw_data[0]
        raw_y = raw_data[1]
        raw_z = raw_data[2]

        gyro_scale = 1
        gyro_range = self._gyro_range
        if gyro_range == GyroRange.RANGE_250_DPS:
            gyro_scale = 131
        if gyro_range == GyroRange.RANGE_500_DPS:
            gyro_scale = 65.5
        if gyro_range == GyroRange.RANGE_1000_DPS:
            gyro_scale = 32.8
        if gyro_range == GyroRange.RANGE_2000_DPS:
            gyro_scale = 16.4

        # Scale to °/s (not radians!)
        gyro_x = raw_x / gyro_scale
        gyro_y = raw_y / gyro_scale
        gyro_z = raw_z / gyro_scale

        return (gyro_x, gyro_y, gyro_z)

    @property
    def cycle(self) -> bool:
        """Enable or disable periodic measurement at a rate set by cycle_rate.
        If the sensor was in sleep mode, it will be waken up to cycle"""
        return self._cycle

    @cycle.setter
    def cycle(self, value: bool) -> None:
        self.sleep = not value
        self._cycle = value

    @property
    def gyro_range(self) -> int:
        """The measurement range of all gyroscope axes. Must be a `GyroRange`"""
        return self._gyro_range

    @gyro_range.setter
    def gyro_range(self, value: int) -> None:
        if (value < 0) or (value > 3):
            raise ValueError("gyro_range must be a GyroRange")
        self._gyro_range = value
        sleep(0.01)

    @property
    def accelerometer_range(self) -> int:
        """The measurement range of all accelerometer axes. Must be a `Range`"""
        return self._accel_range

    @accelerometer_range.setter
    def accelerometer_range(self, value: int) -> None:
        if (value < 0) or (value > 3):
            raise ValueError("accelerometer_range must be a Range")
        self._accel_range = value
        self._accel_scale = 1.0 / [16384, 8192, 4096, 2048][value]
        sleep(0.01)

    @property
    def filter_bandwidth(self) -> int:
        """The bandwidth of the gyroscope Digital Low Pass Filter. Must be a `GyroRange`"""
        return self._filter_bandwidth

    @filter_bandwidth.setter
    def filter_bandwidth(self, value: int) -> None:
        if (value < 0) or (value > 6):
            raise ValueError("filter_bandwidth must be a Bandwidth")
        self._filter_bandwidth = value
        sleep(0.01)

    @property
    def cycle_rate(self) -> int:
        """The rate that measurements are taken while in `cycle` mode. Must be a `Rate`"""
        return self._cycle_rate

    @cycle_rate.setter
    def cycle_rate(self, value: int) -> None:
        if (value < 0) or (value > 3):
            raise ValueError("cycle_rate must be a Rate")
        self._cycle_rate = value
        sleep(0.01)

    @property
    def clock_source(self) -> int:
        """The clock source for the sensor"""
        return self._clksel

    @clock_source.setter
    def clock_source(self, value: int) -> None:
        """Select between Internal/External clock sources"""
        if value not in range(8):
            raise ValueError("clock_source must be ClockSource value, integer from 0 - 7.")
        self._clksel = value

    def read_whole_fifo(self):
        """Return raw FIFO bytes"""
        # This code must be fast to ensure samples are contiguous
        count = self.fifo_count
        buf = bytearray(count)
        buf[0] = _MPU_FIFO_R_W
        with self.i2c_device:
            self.i2c_device.write_then_readinto(buf, buf, out_end=1, in_start=0)
        return buf


# Aliases for compatibility
MPU6050 = MakerClassAccelerometer  # Backward compatibility
MPU6500 = MakerClassAccelerometer  # Alias for MPU6500
