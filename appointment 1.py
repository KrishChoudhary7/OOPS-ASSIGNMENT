import math

class Appointment:
    def __init__(self, day_of_week, start_time_hour, client_name="", client_phone="", appt_type=0):
        self.__client_name = client_name
        self.__client_phone = client_phone
        self.__appt_type = appt_type
        self.__day_of_week = day_of_week
        self.__start_time_hour = start_time_hour

    def get_client_name(self):
        return self.__client_name

    def get_client_phone(self):
        return self.__client_phone

    def get_appt_type(self):
        return self.__appt_type

    def get_day_of_week(self):
        return self.__day_of_week

    def get_start_time_hour(self):
        return self.__start_time_hour

    def get_appt_type_desc(self):
        appt_types = ["Available", "Mens Cut", "Ladies Cut", "Mens Colouring", "Ladies Colouring"]
        return appt_types[self.__appt_type]

    def get_end_time_hour(self):
        return self.__start_time_hour + 1

    def set_client_name(self, name):
        self.__client_name = name

    def set_client_phone(self, phone):
        self.__client_phone = phone

    def set_appt_type(self, appt_type):
        self.__appt_type = appt_type

    def schedule(self, client_name, client_phone, appt_type):
        self.__client_name = client_name
        self.__client_phone = client_phone
        self.__appt_type = appt_type

    def cancel(self):
        self.__client_name = ""
        self.__client_phone = ""
        self.__appt_type = 0

    def format_record(self):
        return f"{self.__client_name},{self.__client_phone},{self.__appt_type},{self.__day_of_week},{self.__start_time_hour}"

    def __str__(self):
        return f"Client: {self.__client_name}, Phone: {self.__client_phone}, Type: {self.get_appt_type_desc()}, Day: {self.__day_of_week}, Time: {self.__start_time_hour}-{self.get_end_time_hour()}"

class SalonCalendar:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.hours = range(9, 17)  # 9 AM to 4 PM (last appointment is 4-5 PM)
        self.appointments = {day: [Appointment(day, hour) for hour in self.hours] for day in self.days}

    def load_appointments(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    client_name, client_phone, appt_type, day_of_week, start_time_hour = line.strip().split(',')
                    appt_type = int(appt_type)
                    start_time_hour = int(start_time_hour)
                    self.schedule_appointment(day_of_week, start_time_hour, client_name, client_phone, appt_type)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty calendar.")

    def save_appointments(self, filename):
        with open(filename, 'w') as file:
            for day in self.days:
                for appt in self.appointments[day]:
                    if appt.get_appt_type() != 0:
                        file.write(appt.format_record() + "\n")

    def schedule_appointment(self, day, hour, client_name, client_phone, appt_type):
        for appt in self.appointments[day]:
            if appt.get_start_time_hour() == hour:
                appt.schedule(client_name, client_phone, appt_type)
                break

    def print_day_calendar(self, day):
        for appt in self.appointments[day]:
            print(appt)

  

    def change_appointment(self, old_day, old_hour, new_day, new_hour, client_name, client_phone, appt_type):
        self.cancel_appointment(old_day, old_hour)
        self.schedule_appointment(new_day, new_hour, client_name, client_phone, appt_type)


def main():
    salon_calendar = SalonCalendar()

    while True:
        print("Menu:")
        print("1) Schedule an appointment")
        print("2) Find appointment by name")
        print("3) Print calendar for a specific day")
        print("4) Cancel an appointment")
        print("5) Change an appointment")
        print("6) Calculate total fees for a day")
        print("7) Calculate total weekly fees")
        print("9) Exit the system")
        choice = input("Enter your choice: ")

        if choice == "1":
            day = input("Enter the day of the week: ")
            hour = int(input("Enter the start time (e.g. 9 for 9 AM): "))
            client_name = input("Enter the client's name: ")
            client_phone = input("Enter the client's phone number: ")
            appt_type = int(input("Enter the type of appointment (1-4): "))
            salon_calendar.schedule_appointment(day, hour, client_name, client_phone, appt_type)
        elif choice == "2":
            client_name = input("Enter the client's name: ")
            appt = salon_calendar.find_appointment_by_name(client_name)
            if appt:
                print(appt)
            else:
                print("Appointment not found.")
        elif choice == "3":
            day = input("Enter the day of the week: ")
            salon_calendar.print_day_calendar(day)
        elif choice == "4":
            day = input("Enter the day of the week: ")
            hour = int(input("Enter the start time (e.g. 9 for 9 AM): "))
            salon_calendar.cancel_appointment(day, hour)
        elif choice == "5":
            old_day = input("Enter the current day of the appointment: ")
            old_hour = int(input("Enter the current start time (e.g. 9 for 9 AM): "))
            new_day = input("Enter the new day for the appointment: ")
            new_hour = int(input("Enter the new start time (e.g. 9 for 9 AM): "))
            client_name = input("Enter the client's name: ")
            client_phone = input("Enter the client's phone number: ")
            appt_type = int(input("Enter the new type of appointment (1-4): "))
            salon_calendar.change_appointment(old_day, old_hour, new_day, new_hour, client_name, client_phone, appt_type)
        elif choice == "6":
            day = input("Enter the day of the week: ")
            total_fees = salon_calendar.calculate_total_fees_for_day(day)
            print(f"Total fees for {day}: ${total_fees}")
        elif choice == "7":
            total_fees = salon_calendar.calculate_total_weekly_fees()
            print(f"Total weekly fees: ${total_fees}")
        elif choice == "9":
            filename = input("Enter the filename to save appointments: ")
            salon_calendar.save_appointments(filename)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
