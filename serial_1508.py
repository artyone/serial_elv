import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import elvis as elv
import sys
import serial


class App(tk.Tk):
    """Интерфейс программы"""

    def __init__(self, program):
        super().__init__()
        self.program = program
        self.ports_list = program.get_ports()
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        s = ttk.Style()
        s.theme_use('vista')
        self.title("Управление микросхемой 1.0")
        frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        frame.pack()

        self.lbl_com = ttk.Label(
            frame,
            text="COM-порт:"
        )
        self.lb_com = ttk.Combobox(
            frame,
            width=70,
            values=list(map(lambda x: x.description, self.ports_list)),
            state="readonly")

        self.lbl_fclk = ttk.Label(
            frame,
            text='Fclk'
        )
        self.ent_fclk = ttk.Entry(
            frame
        )
        self.ent_fclk.insert(0, '1000')
        self.ent_fclk.config(state='readonly')
        self.lbl_fclk_mghz = ttk.Label(
            frame,
            text='МГц'
        )
        self.btn_fclk_edit = ttk.Button(
            frame,
            text='Изменить',
            command=self.edit_processor_frequency
        )
        self.lbl_fout1 = ttk.Label(
            frame,
            text='Fout1'
        )
        self.fout1_stringvar = tk.StringVar()
        self.fout1_stringvar.trace('w', self.check_button)
        self.ent_fout1 = ttk.Entry(
            frame,
            textvariable=self.fout1_stringvar
        )
        self.lbl_fout1_mghz = ttk.Label(
            frame,
            text='МГц'
        )
        self.lb_fout1 = ttk.Combobox(
            frame,
            width=3,
            values=list(['0', '1', '2']),
            state="readonly")
        self.lb_fout1.current(0)
        self.btn_fout1_set = ttk.Button(
            frame,
            text='Установить',
            state='disabled',
            command=lambda: self.set_fout(1)
        )
        self.btn_fout1_on = ttk.Button(
            frame,
            text='Включить',
            command=self.change_CH1_state
        )
        self.lbl_fout2 = ttk.Label(
            frame,
            text='Fout2'
        )
        self.fout2_stringvar = tk.StringVar()
        self.fout2_stringvar.trace('w', self.check_button)
        self.ent_fout2 = ttk.Entry(
            frame,
            textvariable=self.fout2_stringvar
        )
        self.lbl_fout2_mghz = ttk.Label(
            frame,
            text='МГц'
        )
        self.lb_fout2 = ttk.Combobox(
            frame,
            width=3,
            values=list(['0', '1', '2']),
            state="readonly")
        self.lb_fout2.current(0)
        self.btn_fout2_set = ttk.Button(
            frame,
            text='Установить',
            state='disabled',
            command=lambda: self.set_fout(2)
        )
        self.btn_fout2_on = ttk.Button(
            frame,
            text='Включить',
            command=self.change_CH2_state
        )
        self.txt_logs = tk.Text(
            frame,
            width=55,
            height=5,
            state='disabled'
        )
        logo_64 = "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"
        image = tk.PhotoImage(data=logo_64, width=100, height=60)
        self.lbl_image = tk.Label(
            frame,
            image=image
        )
        self.lbl_image.image_ref = image  # type: ignore
        self.__grid_interface()

        try:
            self.lb_com.current(0)
        except:
            mb.showinfo('Предупреждение', 'Не найдено устройство')
            sys.exit()

    def log(self, message):
        """Поле вывода сообщений"""
        self.txt_logs.config(state='normal')
        self.txt_logs.insert(1.0, str(message) + '\n')
        self.txt_logs.config(state='disabled')

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
            profile_index = self.lb_fout1.current()
        else:
            frequency = self.ent_fout2.get()
            profile_index = self.lb_fout2.current()

        if not frequency.isdigit():
            return self.log('Неверно введена частота Fout' + str(channel_number))
        if int(frequency) >= self.program.processor_frequency:
            return self.log('Частота процессора должна быть больше Fout' + str(channel_number))

        try:
            self.program.set_fout(
                int(frequency), self.lb_com.current(), channel_number, profile_index)
            return self.log('Команда успешно выполнена')
        except ValueError as e:
            return self.log(e)
        except IndexError:
            return self.log('Устройство было отключено после запуска программы. Необходимо перезапустить программу')
        except serial.SerialException as e:
            return self.log(e)
        except Exception as e:
            return self.log(e)

    def change_CH1_state(self):
        """Изменить статус 1 канала"""
        message = ''
        try:
            if self.program.switch_CH1_state(self.lb_com.current()):
                if self.program.state_CH1:
                    message += 'FOUT1 ON - '
                else:
                    message += 'FOUT1 OFF - '
                if self.program.state_CH2:
                    message += 'FOUT2 ON'
                else:
                    message += 'FOUT2 OFF'
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except ValueError as e:
            message = e
        except serial.SerialException as e:
            message = e
        except Exception as e:
            message = e
        if self.program.state_CH1:
            self.btn_fout1_on.config(text='Выключить')
        else:
            self.btn_fout1_on.config(text='Включить')

        return self.log(message)

    def change_CH2_state(self):
        """Изменить статус 2 канала"""
        message = ''
        try:
            if self.program.switch_CH2_state(self.lb_com.current()):
                if self.program.state_CH1:
                    message += 'FOUT1 ON - '
                else:
                    message += 'FOUT1 OFF - '
                if self.program.state_CH2:
                    message += 'FOUT2 ON'
                else:
                    message += 'FOUT2 OFF'
            else:
                message = 'Статус каналов не определен'
        except IndexError:
            message = 'Устройство было отключено после запуска программы. Необходимо перезапустить программу'
        except ValueError as e:
            message = e
        # except serial.SerialException as e:
        #     message = e
        # except Exception as e:
        #     message = e
        if self.program.state_CH2:
            self.btn_fout2_on.config(text='Выключить')
        else:
            self.btn_fout2_on.config(text='Включить')

        return self.log(message)

    def check_button(self, *args):
        """Функция контроля кнопки установить частоту"""
        data_fout1 = self.fout1_stringvar.get()
        if data_fout1.isdigit():
            self.btn_fout1_set.config(state='normal')
        else:
            self.btn_fout1_set.config(state='disabled')
        data_fout2 = self.fout2_stringvar.get()
        if data_fout2.isdigit():
            self.btn_fout2_set.config(state='normal')
        else:
            self.btn_fout2_set.config(state='disabled')

    def __grid_interface(self):
        """Отрисовать интерфейс"""
        self.lbl_com.grid(row=0, column=0, pady=5, padx=4, sticky='w')
        self.lb_com.grid(row=0, column=1, pady=5, padx=4,
                         sticky='w', columnspan=5)
        self.lbl_fclk.grid(row=1, column=0, pady=5, padx=4, sticky='e')
        self.ent_fclk.grid(row=1, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fclk_mghz.grid(row=1, column=2, pady=5, padx=4, sticky='w')
        self.btn_fclk_edit.grid(row=1, column=5, pady=5, padx=4, sticky='we')
        self.lbl_fout1.grid(row=2, column=0, pady=5, padx=4, sticky='e')
        self.ent_fout1.grid(row=2, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fout1_mghz.grid(row=2, column=2, pady=5, padx=4, sticky='w')
        self.lb_fout1.grid(row=2, column=3, pady=5, padx=4, sticky='we')
        self.btn_fout1_set.grid(row=2, column=4, pady=5, padx=4, sticky='we')
        self.btn_fout1_on.grid(row=2, column=5, pady=5, padx=4, sticky='we')
        self.lbl_fout2.grid(row=3, column=0, pady=5, padx=4, sticky='e')
        self.ent_fout2.grid(row=3, column=1, pady=5, padx=4, sticky='we')
        self.lbl_fout2_mghz.grid(row=3, column=2, pady=5, padx=4, sticky='w')
        self.lb_fout2.grid(row=3, column=3, pady=5, padx=4, sticky='we')
        self.btn_fout2_set.grid(row=3, column=4, pady=5, padx=4, sticky='we')
        self.btn_fout2_on.grid(row=3, column=5, pady=5, padx=4, sticky='we')
        self.lbl_image.grid(row=0, column=6, pady=5,
                            padx=4, rowspan=5, sticky='S')
        self.txt_logs.grid(row=4, column=1, pady=5, padx=4,
                           sticky='w', columnspan=5)
        self.geometry(self.center_window(width=650, height=270))
        self.resizable(False, False)

    def center_window(self, width, height):
        """Рассчет для центровки положения окна на экране"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        return '%dx%d+%d+%d' % (width, height, x, y)


def main():
    program = elv.Elvis()
    app = App(program)
    app.mainloop()


if __name__ == "__main__":
    main()
