import serial
import time
import math
import threading
from datetime import datetime, timezone

START_LATITUDE = 59.9343
START_LONGITUDE = 30.3061
SPEED = 10.0
START_COURSE = 45.0
ALTITUDE = 15.0
SATELLITES = 8

class NMEAGenerator:
    """Генератор данных в формате NMEA."""

    def __init__(self):
        """Инициализатор начальных координат."""
        # Начальные координаты - Санкт-Петербург, Невский проспект
        self.latitude = START_LATITUDE  # Широта в градусах.
        self.longitude = START_LONGITUDE  # Долгота в градусах.
        self.speed = SPEED  # Скорость в узлах (1 узел = 1.852 км/ч).
        self.course = START_COURSE  # Курс движения в градусах (0-360).
        self.altitude = ALTITUDE  # Высота над уровнем моря в метрах.
        self.satellites = SATELLITES  # Количество видимых спутников.

    def calculate_checksum(self, nmea_sentence):
        """Вычисление контрольной суммы NMEA."""
        checksum = 0

        for char in nmea_sentence:
            checksum ^= ord(char)

        return f'{checksum:02X}'

    def decimal_to_nmea(self, value, is_latitude=True):
        """Конвертирует десятчиную запись в формат NMEA ГГГММ.ММММ."""
        if is_latitude:
            degrees = int(value)
            minutes = (value - degrees) * 60

            return f'{degrees:02d}{minutes:07.4f}'
        else:
            degrees = int(value)
            minutes = (value - degrees) * 60

            return f'{degrees:03d}{minutes:07.4f}'

    def generate_GGA(self):
        """Генератор GGA предложений."""
        now = datetime.now(timezone.utc)
        time_str = now.strftime('%H%M%S.00')

        lat_str = self.decimal_to_nmea(self.latitude, True)
        lon_str = self.decimal_to_nmea(self.longitude, False)

        nmea_data = f'GPGGA,{time_str},{lat_str},N,{lon_str},E,1,{self.satellites:02d},1.0,{self.altitude:.1f},M,,M,,'

        checksum = self.calculate_checksum(nmea_data)

        return f'${nmea_data}*{checksum}\r\n'

    def generate_RMC(self):
        """Генератор RMC предложений."""
        now = datetime.now(timezone.utc)
        time_str = now.strftime('%H%M%S.00')
        date_str = now.strftime('%d%m%y')

        lat_str = self.decimal_to_nmea(self.latitude, True)
        lon_str = self.decimal_to_nmea(self.longitude, False)

        nmea_data = f'GPRMC,{time_str},A,{lat_str},N,{lon_str},E,{self.speed:.1f},{self.course:.1f},{date_str},,E'
        checksum = self.calculate_checksum(nmea_data)

        return f'${nmea_data}*{checksum}\r\n'

    def generate_VTG(self):
        """Генератор VTG предложений."""
        speed_kmh = self.speed * 1.852

        nmea_data = f'GPVTG,{self.course:.1f},T,,M,{self.speed:.1f},N,{speed_kmh:.1f},K'
        checksum = self.calculate_checksum(nmea_data)

        return f"${nmea_data}*{checksum}\r\n"

    def update_position(self):
        """Симуляция движения."""
        self.course = (self.course + 2) % 360

        radius = 0.001
        rad_course = math.radians(self.course)

        delta_lat = radius * math.cos(rad_course) / 111.32
        delta_lon = radius * math.sin(rad_course) / (111.32 * math.cos(math.radians(self.latitude)))

        self.latitude += delta_lat
        self.longitude += delta_lon


class COMPortEmulator:
    """Класс эмуляции COM порта."""

    def __init__(self, port_name="COM4", baudrate=4800):
        """Настройка параметров соединения."""
        self.port_name = port_name
        self.baudrate = baudrate

        self.generator = NMEAGenerator()

        self.is_running = False

        self.thread = None

    def start(self):
        """Запуск эмулятора."""
        try:
            self.serial_port = serial.Serial(
                port=self.port_name,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )

            self.is_running = True

            self.thread = threading.Thread(target=self._run)
            self.thread.start()

            print('Created by Danil Danko')
            print('GitHub: https://github.com/DanilDanko')
            print('')
            print('Эмулятор COM соединения с GPS запущен')
            print('Отправляемые данные: GPGGA, GPRMC, GPVTG')
            print('Для остановки Ctrl+C')

        except Exception as e:
            print(f'Возникла ошибка при запуске: {e}')

    def _run(self):
        """Внутренний метод для генерации и отправки данных."""
        while self.is_running:
            try:
                gga, rmc, vtg = (
                    self.generator.generate_GGA(),
                    self.generator.generate_RMC(),
                    self.generator.generate_VTG()
                )

                self.serial_port.write(gga.encode('utf-8'))
                self.serial_port.write(rmc.encode('utf-8'))
                self.serial_port.write(vtg.encode('utf-8'))

                print(
                    'Отправленны:\n',
                    f'GGA:{gga}',
                    f'RMC:{rmc}',
                    f'VTG:{vtg}'
                )

                self.generator.update_position()

                time.sleep(2.0)

            except Exception as e:
                print(f'При отправке данных возникла ошибка: {e}')
                break

    def stop(self):
        """Остановка эмулятора."""
        self.is_running = False
        if hasattr(self, 'serial_port') and self.serial_port.is_open:
            self.serial_port.close()

        print('Эмулятор остановлен')


if __name__ == '__main__':
    port_name = input('Введите COM-порт в формате "COMx": ')
    baudrate = int(input('Введите скорость передачи данных: '))
    emulator = COMPortEmulator(port_name, baudrate)

    try:
        emulator.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Получен сигнал прерывания (CTRL+C)...')
        emulator.stop()
