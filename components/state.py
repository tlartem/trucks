import reflex as rx
from sqlmodel import select


class Car(rx.Model, table=True):
    car_number: str
    car_type: str
    payload: float
    length: float
    width: float
    height: float


def get_english_from_sort_string(russian_string):
    term_start = len("Сортировка: ")
    russian_term = russian_string[term_start:].strip()
    translations_reverse = {
        "грузоподъемность": "payload",
        "длина": "length",
        "ширина": "width",
        "высота": "height"
    }
    english_term = translations_reverse.get(russian_term, "unknown")
    return english_term


class State(rx.State):
    id: int
    car_number: str = ""
    car_type: str = ""
    payload: float
    length: float
    width: float
    height: float
    cars: list[Car] = []
    sort_value: float
    num_cars: int

    def load_entries(self) -> list[Car]:
        with rx.session() as session:
            self.cars = session.exec(select(Car)).all()
            self.num_cars = len(self.cars)

            if self.sort_value:
                self.cars = sorted(
                    self.cars, key=lambda car: getattr(car, get_english_from_sort_string(self.sort_value)),
                    reverse=True
                )

    def sort_values(self, sort_value):
        self.sort_value = sort_value
        self.load_entries()

    def set_car_vars(self, car: Car):
        print(car)
        self.id = car["id"]
        self.car_number = car["car_number"]
        self.car_type = car["car_type"]
        self.payload = car["payload"]
        self.width = car["width"]
        self.length = car["length"]
        self.height = car["height"]

    def add_car(self):
        with rx.session() as session:
            if session.exec(
                select(Car).where(Car.car_number == self.car_number)
            ).first():
                return rx.window_alert("Car already exists")
            session.add(
                Car(
                    car_number=self.car_number,
                    car_type=self.car_type,
                    payload=self.payload,
                    length=self.length,
                    width=self.width,
                    height=self.height
                )
            )
            session.commit()
        self.load_entries()
        return rx.window_alert(f"Car {self.car_number} has been added.")

    def update_car(self):
        with rx.session() as session:
            car = session.exec(
                select(Car).where(Car.id == self.id)
            ).first()
            car.car_number = self.car_number
            car.car_type = self.car_type
            car.payload = self.payload
            car.length = self.length
            car.width = self.width
            car.height = self.height
            print(car)
            session.add(car)
            session.commit()
        self.load_entries()

    def delete_car(self, car_number: str):
        with rx.session() as session:
            car = session.exec(
                select(Car).where(Car.car_number == car_number)
            ).first()
            session.delete(car)
            session.commit()
        self.load_entries()

    def on_load(self):
        self.load_entries()


def show_car(car: Car):
    return rx.table.row(
        rx.table.cell(rx.text.kbd(car.car_number, size="5")),
        rx.table.cell(car.car_type),
        rx.table.cell(car.payload),
        rx.table.cell(car.length),
        rx.table.cell(car.width),
        rx.table.cell(car.height),
        rx.table.cell(
            update_car(car),
        ),
        rx.table.cell(
            rx.button(
                "Delete",
                on_click=lambda: State.delete_car(car.car_number),
                bg="red",
                color="white",
            ),
        ),
    )


def add_car():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                    "Добавить машину",
                    rx.icon(tag="plus", width=24, height=24),
                    spacing="3",
                    size="2"
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Данные автомобиля"),
            rx.dialog.description(
                "Укажите необходимые данные для добавления автомобиля в базу данных.",
                size="2",
                mb="4",
                padding_bottom="1em",
            ),
            rx.flex(
                rx.text(
                    "Номер",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Номер машины", on_blur=State.set_car_number),
                rx.text(
                    "Тип",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Тип машины (например: фура, газель)", on_blur=State.set_car_type),
                rx.text(
                    "Грузоподъемность, тонн",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Грузоподъемность в тоннах", on_blur=State.set_payload),
                rx.text(
                    "Длина, м",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Длина в метрах", on_blur=State.set_length),
                rx.text(
                    "Ширина, м",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Ширина в метрах", on_blur=State.set_width),
                rx.text(
                    "Высота, м",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Высота в метрах", on_blur=State.set_height),
                direction="column",
                spacing="3",

            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Отмена",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Добавить",
                        on_click=State.add_car,
                        variant="solid",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="4px",
        ),
    )


def update_car(car):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square_pen", width=24, height=24),
                bg="red",
                color="white",
                on_click=lambda: State.set_car_vars(car),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Customer Details"),
            rx.dialog.description(
                "Update your customer profile details.",
                size="2",
                mb="4",
                padding_bottom="1em",
            ),
            rx.flex(
                rx.text(
                    "Name",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    placeholder=car.car_number,
                    default_value=car.car_number,
                    on_blur=State.set_car_number,
                ),
                rx.text(
                    "Email",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    placeholder=car.car_type,
                    default_value=car.car_type,
                    on_blur=State.set_car_type,
                ),
                rx.text(
                    "Customer Phone",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    on_blur=State.set_payload,
                ),
                rx.text(
                    "Customer Address",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    on_blur=State.set_length,
                ),
                rx.text(
                    "Car width",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    on_blur=State.set_width,
                ),
                rx.text(
                    "Car height",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(
                    on_blur=State.set_height,
                ),
                direction="column",
                spacing="3",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Submit Customer",
                        on_click=State.update_car,
                        variant="solid",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="4px",
        ),
    )

