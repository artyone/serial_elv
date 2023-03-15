from serial import Serial, EIGHTBITS
import serial.tools.list_ports as list_ports
import time


class Elvis(object):
    """Класс программирования микросхемы интегральной 1508ПЛ8Т"""
    
    def __init__(self):
        self.command = ''
        self.answer = ''
        self.state_CH1 = False
        self.state_CH2 = False
        self.processor_frequency = 1000
        self.COMMAND_SETA = 0x0010 # Команда установки регистра
        self.COMMAND_WR = 0x0020 # Команда записи
        self.SEL_REG = 0x0002 # Выбор профиля канала 1
        self.SEL_REG_CH1_p_1 = 0x0000
        self.SEL_REG_CH1_p_2 = 0x0001
        self.CTR = 0x0003
        # канал 1 профили и их регистры
        self.CLR = 0x0005
        self.SYNC = 0x0004
        self.CH1 = {
            0: {
                'registers': {
                    'CH1_dPh0_L': 0x1400,
                    'CH1_dPh0_M': 0x1401,
                    'CH1_dPh0_H': 0x1402,
                    'CH1_p0': 0x1404,
                    'CH1_Mul0': 0x1405,
                    'CH1_Offset0': 0x1406
                },
                'data': {
                    # 'CH1_dPh0_L_d' : 0x0000,
                    # 'CH1_dPh0_M_d' : 0x0000,
                    # 'CH1_dPh0_H_d' : 0x0000,
                    'CH1_p0_d': 0x0000,
                    'CH1_Mul0_d': 0x7FFF,
                    'CH1_Offset0_d': 0x0000
                }
            },
            1: {
                'registers': {
                    'CH1_dPh1_L': 0x1410,
                    'CH1_dPh1_M': 0x1411,
                    'CH1_dPh1_H': 0x1412,
                    'CH1_p1': 0x1414,
                    'CH1_Mul1': 0x1415,
                    'CH1_Offset1': 0x1416
                },
                'data': {
                    # 'CH1_dPh1_L_d' : 0x0000,
                    # 'CH1_dPh1_M_d' : 0x0000,
                    # 'CH1_dPh1_H_d' : 0x0000,
                    'CH1_p1_d': 0x0000,
                    'CH1_Mul1_d': 0x7FFF,
                    'CH1_Offset1_d': 0x0000
                }
            },
            2: {
                'registers': {
                    'CH1_dPh2_L': 0x1420,
                    'CH1_dPh2_M': 0x1421,
                    'CH1_dPh2_H': 0x1422,
                    'CH1_p2': 0x1424,
                    'CH1_Mul2': 0x1425,
                    'CH1_Offset2': 0x1426
                },
                'data': {
                    # 'CH1_dPh2_L_d' : 0x0000,
                    # 'CH1_dPh2_M_d' : 0x0000,
                    # 'CH1_dPh2_H_d' : 0x0000,
                    'CH1_p2_d': 0x0000,
                    'CH1_Mul2_d': 0x7FFF,
                    'CH1_Offset2_d': 0x0000
                }
            }
        }
        # канал 2 профили и их регистры
        self.CH2 = {
            0: {
                'registers': {
                    'CH2_dPh0_L': 0x2400,
                    'CH2_dPh0_M': 0x2401,
                    'CH2_dPh0_H': 0x2402,
                    'CH2_p0': 0x2404,
                    'CH2_Mul0': 0x2405,
                    'CH2_Offset0': 0x2406
                },
                'data': {
                    # 'CH2_dPh0_L_d' : 0x0000,
                    # 'CH2_dPh0_M_d' : 0x0000,
                    # 'CH2_dPh0_H_d' : 0x0000,
                    'CH2_p0_d': 0x0000,
                    'CH2_Mul0_d': 0x7FFF,
                    'CH2_Offset0_d': 0x0000
                }
            },
            1: {
                'registers': {
                    'CH2_dPh1_L': 0x2410,
                    'CH2_dPh1_M': 0x2411,
                    'CH2_dPh1_H': 0x2412,
                    'CH2_p1': 0x2414,
                    'CH2_Mul1': 0x2415,
                    'CH2_Offset1': 0x2416
                },
                'data': {
                    # 'CH2_dPh1_L_d' : 0x0000,
                    # 'CH2_dPh1_M_d' : 0x0000,
                    # 'CH2_dPh1_H_d' : 0x0000,
                    'CH2_p1_d': 0x0000,
                    'CH2_Mul1_d': 0x7FFF,
                    'CH2_Offset1_d': 0x0000
                }
            },
            2: {
                'registers': {
                    'CH2_dPh2_L': 0x2420,
                    'CH2_dPh2_M': 0x2421,
                    'CH2_dPh2_H': 0x2422,
                    'CH2_p2': 0x2424,
                    'CH2_Mul2': 0x2425,
                    'CH2_Offset2': 0x2426
                },
                'data': {
                    # 'CH2_dPh2_L_d' : 0x0000,
                    # 'CH2_dPh2_M_d' : 0x0000,
                    # 'CH2_dPh2_H_d' : 0x0000,
                    'CH2_p2_d': 0x0000,
                    'CH2_Mul2_d': 0x7FFF,
                    'CH2_Offset2_d': 0x0000
                }
            }
        }

    def get_ports(self):
        """Получение ком-портов компьютера"""
        ports_list = list_ports.comports()
        return ports_list

    def __get_data_for_registers(self, frequency):
        """Рассчет фактических значений для отправки на микросхему"""
        if self.processor_frequency <= frequency:
            raise ValueError('частота должна быть меньше частоты прцессора')

        f = hex(int(frequency / self.processor_frequency * 2**48))
        data_L = int(str(f)[-4:], 16)
        data_M = int(str(f)[-8:-4], 16)
        data_H = int(str(f)[2:-8], 16)
        return [data_L, data_M, data_H]

    def set_fout(self, 
                frequency, 
                port_index, 
                channel_number, 
                profile_index, 
                timeout, 
                baudrate):
        """Формирование массивов для исполнения команд и загрузки данных на микросхему.
        Обязетально данные в функцию исполнения должны подаваться в виде 2 массивов:
        1. Массив регистров
        2. Массив данных, которые будут записаны в необходимые регистры
        """
        if channel_number == 1:
            all_dPh_registers = self.CH1[profile_index]['registers'].values()
        else:
            all_dPh_registers = self.CH2[profile_index]['registers'].values()

        all_dPh_data = self.__get_data_for_registers(frequency)

        if channel_number == 1:
            all_dPh_data += self.CH1[profile_index]['data'].values()
        else:
            all_dPh_data += self.CH2[profile_index]['data'].values()

        return self.__exec_command(all_dPh_registers, all_dPh_data, port_index, timeout, baudrate)

    def __exec_command(self, registers, datas, port_index, timeout_command, baudrate):
        """Функция исполнения команд и записи данных. 
        Формат данных см. в описании set_fout.
        Команды всегда выполняются в связке 2 из команд. 
        1. Команда SET + регистр
        2. Команда WRITE + данные
        Коды см. в инициализации класса в словарях. 
        """
        with Serial(baudrate=baudrate, bytesize=EIGHTBITS, timeout=0.2) as ser:
            ser.port = list(map(lambda x: x.device, self.get_ports()))[
                port_index]
            ser.open()
            ser.flush()
            self.command = []
            # print('------send------')
            for ch, data in zip(registers, datas):
                #print('st', hex(ch), 'wr', hex(data))
                send_message = self.COMMAND_SETA.to_bytes(1, byteorder='big') \
                    + ch.to_bytes(2, byteorder='big')
                ser.write(send_message)
                self.command.append(hex(int.from_bytes(send_message, byteorder='big')))
                time.sleep(timeout_command)
                send_message = self.COMMAND_WR.to_bytes(1, byteorder='big') \
                    + data.to_bytes(2, byteorder='big')
                ser.write(send_message)
                self.command.append(hex(int.from_bytes(send_message, byteorder='big')))
                time.sleep(timeout_command)
            #self.__output_console(ser)
            self.command = ', '.join(self.command)
            self.set_answer(ser)
            return True

    def switch_CH1_state(self, port_index, timeout, baudrate):
        """Функция смены статуса 1 канала на обратный.
        Статус канала может быть либо ВКЛ, либо ВЫКЛ, но в связи с тем,
        что на микросхеме не реализован вывод данных, то весь процесс
        сохраняется только в сессии программы.
        Для смены статуса первого канала отвечает 12 бит из 15, но
        изменять отдельные биты в регистре мы не можем, приходится менять статус 
        сразу 2 каналов.   
        """
        if not self.state_CH1 and not self.state_CH2:
            answer = self.__exec_command([self.CTR], [0x1000], port_index, timeout, baudrate)
            self.state_CH1 = True
            return answer
        if not self.state_CH1 and self.state_CH2:
            answer = self.__exec_command([self.CTR], [0x3000], port_index, timeout, baudrate)
            self.state_CH1 = True
            return answer
        if self.state_CH1 and not self.state_CH2:
            answer = self.__exec_command([self.CTR], [0x0000], port_index, timeout, baudrate)
            self.state_CH1 = False
            return answer
        if self.state_CH1 and self.state_CH2:
            answer = self.__exec_command([self.CTR], [0x2000], port_index, timeout, baudrate)
            self.state_CH1 = False
            return answer
        return False

    def switch_CH2_state(self, port_index, timeout, baudrate):
        """Функция смены статуса 2 канала на обратный.
        Статус канала может быть либо ВКЛ, либо ВЫКЛ, но в связи с тем,
        что на микросхеме не реализован вывод данных, то весь процесс
        сохраняется только в сессии программы.
        Для смены статуса первого канала отвечает 13 бит из 15, но
        изменять отдельные биты в регистре мы не можем, приходится менять статус 
        сразу 2 каналов.   
        """
        if not self.state_CH2 and not self.state_CH1:
            answer = self.__exec_command([self.CTR], [0x2000], port_index, timeout, baudrate)
            self.state_CH2 = True
            return answer
        if not self.state_CH2 and self.state_CH1:
            answer = self.__exec_command([self.CTR], [0x3000], port_index, timeout, baudrate)
            self.state_CH2 = True
            return answer
        if self.state_CH2 and not self.state_CH1:
            answer = self.__exec_command([self.CTR], [0x0000], port_index, timeout, baudrate)
            self.state_CH2 = False
            return answer
        if self.state_CH2 and self.state_CH1:
            answer = self.__exec_command([self.CTR], [0x1000], port_index, timeout, baudrate)
            self.state_CH2 = False
            return answer
        return False

    # Не используется, реализовано будет аппаратно
    def switch_to_CH1_profile_1(self, port_index):
        self.__exec_command([self.SEL_REG], [self.SEL_REG_CH1_p_1], port_index)
    # Не используется, реализовано будет аппаратно
    def switch_to_CH1_profile_2(self, port_index):
        self.__exec_command([self.SEL_REG], [self.SEL_REG_CH1_p_2], port_index)

    def set_sel_reg(self, ch_1, ch_2, port_index, timeout, baudrate):
        ch_1 = bin(int(ch_1))[2:].zfill(8)
        ch_2 = bin(int(ch_2))[2:].zfill(8)
        data = int(ch_2 + ch_1, 2)
        answer = self.__exec_command([self.SEL_REG], [data], port_index, timeout, baudrate)
        return answer

    def set_answer(self, ser):
        """Получение ответа"""
        self.answer = []
        while True:
            a = ser.read(3)
            if a == b'':
                break
            if len(a) < 3:
                self.answer.append(hex(int.from_bytes(a, byteorder='big')))
                break
            self.answer.append(hex(int.from_bytes(a, byteorder='big')))

        self.answer = ', '.join(self.answer)

    def set_clear(self, port_index, timeout, baudrate):
        answer = self.__exec_command([self.CLR], [0x000F], port_index, timeout, baudrate)
        self.state_CH1 = False
        self.state_CH2 = False
        return answer

    def set_sync(self, number, port_index, timeout, baudrate):
        answer = self.__exec_command([self.SYNC], [number], port_index, timeout, baudrate)
        return answer


    def __output_console(self, ser):
        """Вывод в консоль для отладки"""
        print('------input-----')
        b = b''
        while True:
            a = ser.read(1)
            if a == b'':
                break
            b += a
            #a = a.hex()
            # if a == '10':
            #     print('st', ser.read(2).hex(), end=' ')
            # elif a == '20':
            #     print('wr', ser.read(2).hex())
        print(b.hex())
