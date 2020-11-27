import numpy as np

FILE_WITH_TEST_NAME = "test_long_msg_collisions.txt"
TACT_TIME = 51.2e-6

full_log = []


class Message(object):
    """
          Класс с информацией о кадре. Было решено, что для симуляции и выяснения времен отправок сообщений,
        не обязательно формировать кадр в виде преамбула-адреса-тип-данные-наполнитель-CRC. Поэтому по факту 
        в виде сообщения используется просто класс с нужными полями. 
          :param text: это текст, а вернее данные кадра
          :param time: это время, в которое кадр готов к отправке. При этом ожидание экспоненциальное тоже
            учитывается
          :param send_time: это время, необходимое для того, чтобы отправить этот кадр
          :param attempt: это номер попытки отправки кадра
    """
    def __init__(self,
                 message_text,
                 message_time,
                 message_sending_time):
        self.text = message_text
        self.time = message_time
        self.send_time = message_sending_time
        self.attempt = 0
        full_log.append((message_time, "Got message", message_text))

    def get_text(self):
        return self.text

    def get_time(self):
        return self.time

    def make_pause(self):
        """
              Изменить время до следующей отправки сообщения с учётом метода экспоненциальной задержки.
            Возвращает False, если было слишком много попыток и нужно отклонить попытки. 
        """
        if self.attempt == 15:
            full_log.append((self.time, "Rejected message", self.text))
            return False
        self.attempt += 1
        pause_size = np.random.randint(2 ** (min(10, self.attempt)))
        self.time += pause_size * TACT_TIME
        return True

    def send_message(self, time_start):
        """
              Этот метод добавляет в лог сообщение о том, что сообщение отправляется и возвращает момент
            времени окончания отправки
        """
        final_time = self.send_time + time_start
        full_log.append((time_start, "Send message start", self.text))
        return final_time

    def __le__(self, other):
        return self.time <= other.time

    def __lt__(self, other):
        return self.time < other.time


def work_with_times_data(station_num):
    """
          Считывает файлик с данными и возвращает все данные о сообщениях от конкретной станции
    """
    f = open(FILE_WITH_TEST_NAME)
    msges = []
    while (s := f.readline().rstrip()):
        from_adress, to_adress, time_msg_tact, sending_tacts = s.split()
        from_adress = int(from_adress)
        to_adress = int(to_adress)
        time_msg = float(time_msg_tact) * TACT_TIME
        sending_time = float(sending_tacts) * TACT_TIME
        if from_adress == station_num:
            msges.append(
                Message(f"{from_adress} --> {to_adress}",
                        time_msg,
                        sending_time))
    f.close()
    return sorted(msges)
    
    
class Station(object):
    """
          Класс с информацией на станции. Было решено не добавлять информацию о сообщениях, пришедших
        на станцию, поскольку они не нужны для решения конкретной задачи. 
        :param station_number: это номер станции. Все станции пронумерованы в порядке 0...n - 1
        :param messages: это список сообщений в порядке возрастания времени, а значит в порядке их
          отправки со станции
    """
    def __init__(self, station_number):
        self.station_number = station_number
        self.messages = work_with_times_data(station_number)

    def has_messages_to_send(self):
        """
            Возвращает bool, есть ли ещё сообщения, которые будет отправлять эта станция
        """
        return len(self.messages) > 0

    def remove_message(self):
        """
            Удаление сообщения из списка сообщений со станции.
        """
        self.messages = self.messages[1:]

    def get_top_msg(self):
        """
            Получение следующего отправляемого станцией сообщения
        """
        return self.messages[0]


def have_msg_to_send(stations):
    """
        Возвращает bool, есть ли ещё сообщения, которые будет отправлять хотя бы одна станция
    """
    for station_num in range(len(stations)):
        if stations[station_num].has_messages_to_send():
            return True
    return False


n = int(input())
stations = []
for station_number in range(n):
    stations.append(Station(station_number))
tact_start_time = 0
sending_msg_end_time = None
waiting_candidates = set()

while have_msg_to_send(stations):
    tact_end_time = tact_start_time + TACT_TIME
    if sending_msg_end_time is None:
        # Ни одного сообщения не передаётся и шина свободна
        if len(waiting_candidates) > 1:
            # Происходит коллизия в данный момент, а значит всем надо отложить отправку экспоненциально
            for station_num in waiting_candidates:
                if not stations[station_num].get_top_msg().make_pause():
                    stations[station_num].remove_message()
        if len(waiting_candidates) == 1:
            # Начинает отправку сообщения через шину, как единственный кандидат при свободной шине
            station_num = waiting_candidates.pop()
            sending_msg_end_time = stations[station_num].get_top_msg().send_message(tact_start_time)
            stations[station_num].remove_message()
        waiting_candidates = set()
    if (sending_msg_end_time is not None and tact_end_time > sending_msg_end_time):
        # Если отправка текущего сообщения заканчивается на этом такте, то говорим, что шина освободилась
        sending_msg_end_time = None
    # Обновляем список кандидатов на отправку сообщения через шину в следующий такт
    for station_num in range(len(stations)):
        if stations[station_num].has_messages_to_send():
            msg = stations[station_num].get_top_msg()
            if tact_end_time >= msg.get_time():
                waiting_candidates.add(station_num)
    tact_start_time = tact_end_time
full_log.sort()

for t, type_of_msg, msg in full_log:
    print(f"{np.round(t, 8)}: {type_of_msg} '{msg}'")


