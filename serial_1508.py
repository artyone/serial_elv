import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import elvis as elv
import sys
from itertools import count
from serial import SerialException


class App(tk.Tk):
    """Интерфейс программы"""

    def __init__(self, program):
        super().__init__()
        self.program: elv.Elvis = program
        self.ports_list = program.get_ports()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        s = ttk.Style()
        s.theme_use('vista')
        self.title("Управление микросхемой 1.5.1")
        self.frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        self.frame.pack()

        self.lbl_com = ttk.Label(
            self.frame,
            text="COM-порт:"
        )
        self.cmb_com = ttk.Combobox(
            self.frame,
            width=70,
            values=list(map(lambda x: x.description, self.ports_list)),
            state="readonly")

        self.lbl_timeout = ttk.Label(
            self.frame,
            text='Timeout'
        )
        self.ent_timeout = ttk.Entry(
            self.frame
        )
        self.ent_timeout.insert(0, '0.2')

        self.lbl_baudrate = ttk.Label(
            self.frame,
            text='Baudrate'
        )
        self.ent_baudrate = ttk.Entry(
            self.frame
        )
        self.ent_baudrate.insert(0, '115200')

        self.lbl_fclk = ttk.Label(
            self.frame,
            text='Fclk'
        )
        self.ent_fclk = ttk.Entry(
            self.frame
        )
        self.ent_fclk.insert(0, '1000000')
        self.ent_fclk.config(state='readonly')
        self.lbl_fclk_mghz = ttk.Label(
            self.frame,
            text='КГц'
        )
        self.btn_fclk_edit = ttk.Button(
            self.frame,
            text='Изменить',
            command=self.edit_processor_frequency
        )

        self.separator_1 = tk.Frame(
            self.frame, height=2, bg='gray', relief='groove')
        self.separator_2 = tk.Frame(
            self.frame, height=2, bg='gray', relief='groove')
        self.separator_3 = tk.Frame(
            self.frame, height=2, bg='gray', relief='groove')

        self.lbl_fout1 = ttk.Label(
            self.frame,
            text='Fout1'
        )

        self.fout1_stringvar_ch = tk.StringVar()
        self.fout1_stringvar_ch.trace('w', self.insert_ch)
        self.ent_fout1_chose_ch = ttk.Entry(
            self.frame,
            textvariable=self.fout1_stringvar_ch
        )
        self.lbl_fout1_choose_ch = ttk.Label(
            self.frame,
            text='<- Номер частотного канала'
        )

        self.btn_fout1_on = ttk.Button(
            self.frame,
            text='Включить',
            command=lambda: self.set_CH_status_to_ON(1)
        )
        self.btn_fout1_off = ttk.Button(
            self.frame,
            text='Выключить',
            command=lambda: self.set_CH_status_to_OFF(1)
        )
        self.fout1_stringvar = tk.StringVar()
        self.fout1_stringvar.trace('w', self.check_button)
        self.ent_fout1 = ttk.Entry(
            self.frame,
            textvariable=self.fout1_stringvar
        )
        self.lbl_fout1_mghz = ttk.Label(
            self.frame,
            text='КГц'
        )
        self.combo_fout1 = ttk.Combobox(
            self.frame,
            width=3,
            values=['0', '1', '2', '3'],
            state="readonly")
        self.combo_fout1.current(0)

        self.ent_amplitude_fout1 = ttk.Entry(
            self.frame,
        )
        self.ent_amplitude_fout1.insert(0, '32767')

        self.btn_fout1_set = ttk.Button(
            self.frame,
            text='Установить',
            state='disabled',
            command=lambda: self.set_fout(1)
        )

        self.lbl_modulation = ttk.Label(
            self.frame,
            text='Модуляция'
        )
        self.var_modulation = tk.BooleanVar()
        self.chk_modulation = tk.Checkbutton(
            self.frame,
            text="Вкл",
            variable=self.var_modulation,
            command=self.show_modulation_fout1
        )

        self.modulation_block_fout1 = tk.Frame(self.frame)

        self.lbl_fout1_modulation = ttk.Label(
            self.modulation_block_fout1,
            text='F несущая'
        )

        self.fout1_stringvar_modulation = tk.StringVar()
        self.fout1_stringvar_modulation.trace('w', self.check_button)
        self.ent_fout1_modulation = ttk.Entry(
            self.modulation_block_fout1,
            textvariable=self.fout1_stringvar_modulation
        )

        self.lbl_delta_fout1_modulation = ttk.Label(
            self.modulation_block_fout1,
            text='Ширина модуляции'
        )
        self.delta_fout1_stringvar_modulation = tk.StringVar()
        self.delta_fout1_stringvar_modulation.trace('w', self.check_button)
        self.ent_delta_fout1_modulation = ttk.Entry(
            self.modulation_block_fout1,
            textvariable=self.delta_fout1_stringvar_modulation
        )

        self.btn_fout1_on_modulation = ttk.Button(
            self.modulation_block_fout1,
            text='Включить',
            command=lambda: self.set_CH_status_to_ON(1)
        )
        self.btn_fout1_off_modulation = ttk.Button(
            self.modulation_block_fout1,
            text='Выключить',
            command=lambda: self.set_CH_status_to_OFF(1)
        )

        self.btn_fout1_set_modulation = ttk.Button(
            self.modulation_block_fout1,
            text='Установить',
            state='disabled',
            command=lambda: self.set_fout_modulation(1)
        )

        self.lbl_fout2 = ttk.Label(
            self.frame,
            text='Fout2'
        )

        self.fout2_stringvar_ch = tk.StringVar()
        self.fout2_stringvar_ch.trace('w', self.insert_ch)
        self.ent_fout2_chose_ch = ttk.Entry(
            self.frame,
            textvariable=self.fout2_stringvar_ch
        )
        self.lbl_fout2_choose_ch = ttk.Label(
            self.frame,
            text='<- Номер частотного канала'
        )

        self.btn_fout2_on = ttk.Button(
            self.frame,
            text='Включить',
            command=lambda: self.set_CH_status_to_ON(2)
        )
        self.btn_fout2_off = ttk.Button(
            self.frame,
            text='Выключить',
            command=lambda: self.set_CH_status_to_OFF(2)
        )
        self.fout2_stringvar = tk.StringVar()
        self.fout2_stringvar.trace('w', self.check_button)
        self.ent_fout2 = ttk.Entry(
            self.frame,
            textvariable=self.fout2_stringvar
        )

        self.lbl_fout2_mghz = ttk.Label(
            self.frame,
            text='КГц'
        )
        self.combo_fout2 = ttk.Combobox(
            self.frame,
            width=3,
            values=['0', '1', '2', '3'],
            state="readonly"
        )
        self.combo_fout2.current(0)

        self.ent_amplitude_fout2 = ttk.Entry(
            self.frame,
        )
        self.ent_amplitude_fout2.insert(0, '32767')

        self.btn_fout2_set = ttk.Button(
            self.frame,
            text='Установить',
            state='disabled',
            command=lambda: self.set_fout(2)
        )

        self.lbl_sel_reg = ttk.Label(
            self.frame,
            text='SEL_REG'
        )
        self.combo_sel_reg_ch1 = ttk.Combobox(
            self.frame,
            width=3,
            values=list(range(64)),
            state="readonly")
        self.lbl_sel_reg_ch1 = ttk.Label(
            self.frame,
            text='<- CH1'
        )
        self.lbl_sel_reg_ch2 = ttk.Label(
            self.frame,
            text='<- CH2'
        )
        self.combo_sel_reg_ch2 = ttk.Combobox(
            self.frame,
            width=3,
            values=list(range(64)),
            state="readonly")

        self.combo_sel_reg_ch1.current(0)
        self.combo_sel_reg_ch2.current(0)
        self.btn_sel_reg = ttk.Button(
            self.frame,
            text='Установить',
            command=self.set_sel_reg
        )

        self.lbl_sync = ttk.Label(
            self.frame,
            text='SYNC'
        )
        self.ent_sync = ttk.Entry(
            self.frame
        )
        self.ent_sync.insert(0, '0000')
        self.btn_sync = ttk.Button(
            self.frame,
            text='Установить',
            command=self.sync
        )

        self.btn_clear = ttk.Button(
            self.frame,
            text='Очистка',
            command=self.clear
        )

        self.txt_logs = tk.Text(
            self.frame,
            width=60,
            height=12,
            state='disabled'
        )
        self.answer_logs = tk.Text(
            self.frame,
            width=60,
            height=12,
            state='disabled'
        )
        logo_64 = "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"
        image = tk.PhotoImage(data=logo_64, width=100, height=60)
        self.lbl_image = tk.Label(
            self.frame,
            image=image
        )
        self.lbl_image.image_ref = image  # type: ignore
        self.__grid_interface()

        try:
            self.cmb_com.current(0)
        except:
            mb.showinfo('Предупреждение', 'Не найдено устройство')
            sys.exit()

    def log(self, message, obj):
        """Вывод сообщений пользователю"""
        obj.config(state='normal')
        obj.insert(1.0, str(message) + '\n')
        obj.config(state='disabled')

    def edit_processor_frequency(self):
        """Изменение частоты процесса.
        Фактически частота процессора участвуют только в вычислениях. 
        """
        state = str(self.ent_fclk['state'])
        if state == 'readonly':
            self.ent_fclk['state'] = 'normal'
            self.btn_fclk_edit['text'] = 'Сохранить'
            self.ent_fclk.focus()
        if state == 'normal':
            self.ent_fclk['state'] = 'readonly'
            self.btn_fclk_edit['text'] = 'Изменить'
            if self.ent_fclk.get().isdigit():
                self.program.processor_frequency = int(self.ent_fclk.get())
            else:
                self.log('Неверно введена частота процессора')

    def set_fout(self, channel_number):
        """Изменение частоты 1 и 2 канала"""
        if channel_number == 1:
            frequency = self.ent_fout1.get()
            profile_index = self.combo_fout1.current()
            amplitude = self.ent_amplitude_fout1.get()
        else:
            frequency = self.ent_fout2.get()
            profile_index = self.combo_fout2.current()
            amplitude = self.ent_amplitude_fout2.get()
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения timeout или baudrate', self.txt_logs)
        if not frequency.isdigit() or not amplitude.isdigit():
            return self.log('Неверно введена частота Fout или амплитуда. Канал:'
                            + str(channel_number),
                            self.txt_logs)
        if int(frequency) >= self.program.processor_frequency:
            return self.log('Частота процессора должна быть больше Fout' + str(channel_number), self.txt_logs)

        try:
            if self.program.set_fout(
                frequency=int(frequency),
                amplitude=int(amplitude),
                port_index=self.cmb_com.current(),
                channel_number=channel_number,
                profile_index=profile_index,
                timeout=timeout,
                baudrate=baudrate
            ):
                message = f'Частота: {frequency}, Амплитуда: {amplitude}. timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'

                self.log(message, self.txt_logs)
                self.log(answer, self.answer_logs)
        except ValueError as e:
            return self.log(e, self.txt_logs)
        except IndexError:
            return self.log(
                'Устройство было отключено после запуска программы. Необходимо перезапустить программу',
                self.txt_logs)
        except SerialException as e:
            return self.log(e, self.txt_logs)
        except Exception as e:
            return self.log(e, self.txt_logs)

    def set_fout_modulation(self, channel_number):
        """Изменение частоты 1 и 2 канала"""
        if channel_number == 1:
            frequency = self.ent_fout1_modulation.get()
            delta_frequency = self.ent_delta_fout1_modulation.get()
            profiles_index = [2, 0, 1]
            amplitude = self.ent_amplitude_fout1.get()
        else:
            # TODO написать реализацию для фоут2
            pass
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения timeout или baudrate', self.txt_logs)
        if not frequency.isdigit() or not delta_frequency.isdigit():
            return self.log(
                'Неверно введена частота Fout или delta Fout. Канал:'
                + str(channel_number),
                self.txt_logs
            )
        if int(frequency) >= self.program.processor_frequency:
            return self.log('Частота процессора должна быть больше Fout' + str(channel_number), self.txt_logs)
        if int(delta_frequency) >= int(frequency):
            return self.log('delta fout должна быть меньше Fout' + str(channel_number), self.txt_logs)
        try:
            for profile in profiles_index:
                if profile == 2:
                    send_frequency = int(frequency)
                if profile == 0:
                    send_frequency = int(frequency) + int(delta_frequency)
                if profile == 1:
                    send_frequency = int(frequency) - int(delta_frequency)
                if self.program.set_fout(
                    frequency=send_frequency,
                    amplitude=int(amplitude),
                    port_index=self.cmb_com.current(),
                    channel_number=channel_number,
                    profile_index=profile,
                    timeout=timeout,
                    baudrate=baudrate
                ):
                    message = f'Частота: {send_frequency}, Амплитуда: {amplitude}, Профиль: {profile}. timeout: {timeout}, baudrate: {baudrate}'
                    answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'

                self.log(message, self.txt_logs)
                self.log(answer, self.answer_logs)
        except ValueError as e:
            return self.log(e, self.txt_logs)
        except IndexError:
            return self.log(
                'Устройство было отключено после запуска программы. Необходимо перезапустить программу',
                self.txt_logs)
        except SerialException as e:
            return self.log(e, self.txt_logs)
        except Exception as e:
            return self.log(e, self.txt_logs)

    def set_CH_status_to_ON(self, channel):
        message = ''
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения timeout или baudrate')

        try:
            if channel == 1:
                command = self.program.status_CH1_to_ON
            else:
                command = self.program.status_CH2_to_ON
            answer = command(self.cmb_com.current(), timeout, baudrate)
            if answer:
                message += 'FOUT1 ON - ' if self.program.state_CH1 else 'FOUT1 OFF - '
                message += 'FOUT2 ON, ' if self.program.state_CH2 else 'FOUT2 OFF, '
                message += f'timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'
                self.log(answer, self.answer_logs)
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except Exception as e:
            message = str(e)

        self.log(message, self.txt_logs)

    def set_CH_status_to_OFF(self, channel):
        message = ''
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения timeout или baudrate')

        try:
            if channel == 1:
                command = self.program.status_CH1_to_OFF
            else:
                command = self.program.status_CH2_to_OFF
            answer = command(self.cmb_com.current(), timeout, baudrate)
            if answer:
                message += 'FOUT1 ON - ' if self.program.state_CH1 else 'FOUT1 OFF - '
                message += 'FOUT2 ON, ' if self.program.state_CH2 else 'FOUT2 OFF, '
                message += f'timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'
                self.log(answer, self.answer_logs)
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except Exception as e:
            message = str(e)

        self.log(message, self.txt_logs)

    def clear(self):
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения timeout или baudrate')

        try:
            answer = self.program.set_clear(
                self.cmb_com.current(), timeout, baudrate)
            if answer:
                message = f'Очищено. timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'
                self.log(answer, self.answer_logs)
                self.program.state_CH1 = False
                self.program.state_CH2 = False
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except ValueError as e:
            message = e
        except SerialException as e:
            message = e
        except Exception as e:
            message = e

        self.log(message, self.txt_logs)

    def sync(self, number=None):
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
            if number is None:
                number = int(self.ent_sync.get(), 16)
        except:
            return self.log('Введены неверные значения sync, timeout или baudrate')

        try:
            answer = self.program.set_sync(
                number, self.cmb_com.current(), timeout, baudrate)
            if answer:
                message = f'SYNC {hex(number)} установлен. timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'
                self.log(answer, self.answer_logs)
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except ValueError as e:
            message = e
        except SerialException as e:
            message = e
        except Exception as e:
            message = e

        self.log(message, self.txt_logs)

    def set_sel_reg(self):
        try:
            timeout = float(self.ent_timeout.get())
            baudrate = float(self.ent_baudrate.get())
        except:
            return self.log('Введены неверные значения sync, timeout или baudrate')
        ch1 = self.combo_sel_reg_ch1.current()
        ch2 = self.combo_sel_reg_ch2.current()
        try:
            answer = self.program.set_sel_reg(
                ch1, ch2, self.cmb_com.current(), timeout, baudrate)
            if answer:
                message = f'SEL_REG установлен. timeout: {timeout}, baudrate: {baudrate}'
                answer = f'Команды:\n{self.program.command}\nOтвет:\n{self.program.answer}\n--------------------------\n'
                self.log(answer, self.answer_logs)
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except ValueError as e:
            message = e
        except SerialException as e:
            message = e
        except Exception as e:
            message = e

        self.log(message, self.txt_logs)

    def show_modulation_fout1(self):
        if self.var_modulation.get():
            self.chk_modulation.config(text='Выкл')
            self.modulation_block_fout1.grid()
            self.modulation_block_fout1.update()
            self.update_window_size(self.modulation_block_fout1.winfo_height())
            self.sync(int('0100', 16))
        else:
            self.chk_modulation.config(text='Вкл')
            self.modulation_block_fout1.grid_remove()
            self.update_window_size(-self.modulation_block_fout1.winfo_height())
            self.sync(int('0000', 16))

    def check_button(self, *args):
        """Функция контроля кнопки установить частоту"""
        data_fout1 = self.fout1_stringvar.get()
        try:
            float(data_fout1)
            self.btn_fout1_set.config(state='normal')
        except:
            self.btn_fout1_set.config(state='disabled')
        data_fout2 = self.fout2_stringvar.get()
        try:
            float(data_fout2)
            self.btn_fout2_set.config(state='normal')
        except:
            self.btn_fout2_set.config(state='disabled')

        data_fout1_modulation = self.fout1_stringvar_modulation.get()
        data_delta_fout1_modulation = self.delta_fout1_stringvar_modulation.get()
        try:
            float(data_fout1_modulation)
            float(data_delta_fout1_modulation)
            self.btn_fout1_set_modulation.config(state='normal')
        except:
            self.btn_fout1_set_modulation.config(state='disabled')

    def insert_ch(self, *args):
        data_fout1 = self.fout1_stringvar_ch.get()
        if data_fout1.isdigit():
            ch = int(data_fout1)
            if ch > 1601:
                ch = 1601
                self.ent_fout1_chose_ch.delete(0, tk.END)
                self.ent_fout1_chose_ch.insert(0, '1601')
            freq = 160000 + (ch - 1) * 25
            self.ent_fout1.delete(0, tk.END)
            self.ent_fout1.insert(0, str(freq))
        else:
            self.ent_fout1.delete(0, tk.END)

        data_fout2 = self.fout2_stringvar_ch.get()
        if data_fout2.isdigit():
            ch = int(data_fout2)
            if ch > 1601:
                ch = 1601
                self.ent_fout2_chose_ch.delete(0, tk.END)
                self.ent_fout2_chose_ch.insert(0, '1601')
            freq = 160000 + (ch - 1) * 25
            self.ent_fout2.delete(0, tk.END)
            self.ent_fout2.insert(0, str(freq))
        else:
            self.ent_fout2.delete(0, tk.END)

    def __grid_interface(self):
        """Отрисовать интерфейс"""
        counter = count(0)
        row = next(counter)
        self.lbl_com.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.cmb_com.grid(
            row=row, column=1, pady=5, padx=4, sticky='we', columnspan=5)

        row = next(counter)
        self.lbl_timeout.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.ent_timeout.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.lbl_baudrate.grid(
            row=row, column=2, pady=5, padx=4, sticky='e')
        self.ent_baudrate.grid(
            row=row, column=3, pady=5, padx=4, sticky='we')

        row = next(counter)
        self.lbl_fclk.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.ent_fclk.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fclk_mghz.grid(
            row=row, column=2, pady=5, padx=4, sticky='w')
        self.btn_fclk_edit.grid(
            row=row, column=5, pady=5, padx=4, sticky='we')

        row = next(counter)
        self.separator_1.grid(
            row=row, column=0, sticky='ew', padx=5, pady=5, columnspan=7)

        row = next(counter)
        self.lbl_fout1.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.ent_fout1_chose_ch.grid(
            row=row, column=1, pady=5, padx=4, sticky='e')
        self.lbl_fout1_choose_ch.grid(
            row=row, column=2, pady=5, padx=4, sticky='we', columnspan=2)
        self.btn_fout1_on.grid(
            row=row, column=4, pady=5, padx=4, sticky='e')
        self.btn_fout1_off.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.ent_fout1.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fout1_mghz.grid(
            row=row, column=2, pady=5, padx=4, sticky='w')
        self.combo_fout1.grid(
            row=row, column=3, pady=5, padx=4, sticky='we')

        self.ent_amplitude_fout1.grid(
            row=row, column=4, pady=5, padx=4, sticky='we')

        self.btn_fout1_set.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.chk_modulation.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        self.lbl_modulation.grid(row=row, column=0, sticky='e', padx=5, pady=5)

        row = next(counter)
        self.modulation_block_fout1.grid(
            row=row, column=0, columnspan=6, rowspan=2, sticky='we'
        )
        self.modulation_block_fout1.grid_remove()
        row = next(counter)

        self.lbl_fout1_modulation.grid(
            row=0, column=0, sticky='e', padx=5, pady=5)
        self.ent_fout1_modulation.grid(
            row=0, column=1, sticky='w', padx=5, pady=5)
        self.btn_fout1_on_modulation.grid(
            row=0, column=2, sticky='e', padx=5, pady=5)
        self.btn_fout1_off_modulation.grid(
            row=0, column=3, sticky='e', padx=5, pady=5)

        self.lbl_delta_fout1_modulation.grid(
            row=1, column=0, sticky='e', padx=5, pady=5)
        self.ent_delta_fout1_modulation.grid(
            row=1, column=1, sticky='w', padx=5, pady=5)
        self.btn_fout1_set_modulation.grid(
            row=1, column=3, sticky='w', padx=5, pady=5)

        row = next(counter)
        self.separator_2.grid(
            row=row, column=0, sticky='ew', padx=5, pady=5, columnspan=7)

        row = next(counter)
        self.lbl_fout2.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.ent_fout2_chose_ch.grid(
            row=row, column=1, pady=5, padx=4, sticky='e')
        self.lbl_fout2_choose_ch.grid(
            row=row, column=2, pady=5, padx=4, sticky='we', columnspan=2)
        self.btn_fout2_on.grid(
            row=row, column=4, pady=5, padx=4, sticky='e')
        self.btn_fout2_off.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.ent_fout2.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fout2_mghz.grid(
            row=row, column=2, pady=5, padx=4, sticky='w')
        self.combo_fout2.grid(
            row=row, column=3, pady=5, padx=4, sticky='we')
        self.ent_amplitude_fout2.grid(
            row=row, column=4, pady=5, padx=4, sticky='we')
        self.btn_fout2_set.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.separator_3.grid(
            row=row, column=0, sticky='ew', padx=5, pady=5, columnspan=7)

        row = next(counter)
        self.lbl_sel_reg.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.combo_sel_reg_ch1.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.lbl_sel_reg_ch1.grid(
            row=row, column=2, pady=5, padx=4, sticky='w')
        self.combo_sel_reg_ch2.grid(
            row=row, column=3, pady=5, padx=4, sticky='we')
        self.lbl_sel_reg_ch2.grid(
            row=row, column=4, pady=5, padx=4, sticky='w')
        self.btn_sel_reg.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.lbl_sync.grid(
            row=row, column=0, pady=5, padx=4, sticky='e')
        self.ent_sync.grid(
            row=row, column=1, pady=5, padx=4, sticky='we')
        self.btn_sync.grid(
            row=row, column=5, pady=5, padx=4, sticky='w')

        row = next(counter)
        self.btn_clear.grid(
            row=row, column=4, pady=5, padx=4, sticky='we', columnspan=2)

        row = next(counter)
        self.txt_logs.grid(
            row=row, column=0, pady=5, padx=4, sticky='we', columnspan=6)
        # self.lbl_image.grid(
        #     row=row, column=6, pady=5, padx=4, sticky='sw', rowspan=2)

        row = next(counter)
        self.answer_logs.grid(
            row=row, column=0, pady=5, padx=4, sticky='we', columnspan=6)

        self.update_window_size()

        # self.geometry(self.center_window(width=700, height=830))
        # self.resizable(False, False)

    def update_window_size(self, additional=0):
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        self.geometry(f"{width}x{height + additional}")

    def center_window(self, width, height):
        """Рассчет для центровки положения окна на экране"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        return '%dx%d+%d+%d' % (width, height, x, y)


def main():
    program = elv.Elvis()
    app = App(program)
    app.mainloop()


if __name__ == "__main__":
    main()
