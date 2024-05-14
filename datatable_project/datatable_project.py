from rxconfig import config
from components.navbar import navbar
import reflex as rx
from components.state import *

filename = f"{config.app_name}/{config.app_name}.py"


def convert_values_to_float(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, (int, float)):
            new_dict[key] = float(value)
        elif isinstance(value, str):
            try:
                new_dict[key] = float(value)
            except ValueError:
                raise ValueError()
        else:
            raise TypeError()
    return new_dict


class FormState(rx.State):
    form_data: dict = {}
    cars: list = []
    car: str = ''

    def handle_submit(self, form_data: dict):
        is_done = False
        try:
            convert_values_to_float(form_data)
            id = None
            with rx.session() as session:
                self.cars = session.exec(select(Car).where(Car.payload >= form_data['payload'],
                                                           Car.width >= form_data['width'],
                                                           Car.height >= form_data['height'],
                                                           Car.length >= form_data['length'])).first()
                if self.cars and self.cars.status != "Занята":
                    self.car = self.cars.car_number + ' - вы успешно заняли машину под данным номером.'
                    id = self.cars.id
                    is_done = True
                else:
                    self.car = 'Нет доступных машин для перевозки заданного груза'
        except ValueError:
            self.car = 'Введены неверные значения для габаритов'
        if is_done:
            with rx.session() as session:
                car = session.exec(
                    select(Car).where(Car.id == id)
                ).first()
                car.status = "Занята"
                session.status = car.status
                session.commit()
                State.load_entries()


def content():
    return rx.fragment(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    f"Всего машин: {State.num_cars}",
                    size="5",
                    font_family="Inter",
                ),
                rx.spacer(),
                rx.flex(
                    rx.switch(default_checked=False, checked=~State.switchBusyStatus,
                              on_change=lambda v: State.switch_busy(~v)),
                    rx.text("Свободные"),
                    spacing="2",
                ),
                rx.flex(
                    rx.switch(default_checked=False, checked=~State.switchFreeStatus,
                              on_change=lambda v: State.switch_free(~v)),
                    rx.text("Занятые"),
                    spacing="2",
                ),
                rx.select(
                    ["Сортировка: грузоподъемность", "Сортировка: длина", "Сортировка: ширина", "Сортировка: высота"],
                    default_value="Сортировка: грузоподъемность",
                    size="3",
                    on_change=lambda sort_value: State.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="2em",
                align="center",
                # padding_bottom="1em",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Номер"),
                        rx.table.column_header_cell("Тип"),
                        rx.table.column_header_cell("Грузоподъемность, тонн"),
                        rx.table.column_header_cell("Длина, м"),
                        rx.table.column_header_cell("Ширина, м"),
                        rx.table.column_header_cell("Высота"),
                        rx.table.column_header_cell("Статус"),
                        rx.table.column_header_cell("Занять"),
                        rx.table.column_header_cell("Редактировать"),
                        rx.table.column_header_cell("Удалить"),
                    ),
                ),
                rx.table.body(rx.foreach(State.cars, show_car)),
                size="3",
                width="100%",
            ),
        ),
    )


def req() -> rx.Component:
    return rx.vstack(
        rx.heading('Создание заявки'),
        rx.text('Для создания новой заявки укажите все характеристики груза.'),
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Вес, тонны",
                    name="payload",
                ),
                rx.input(
                    placeholder="Длина, м",
                    name="length",
                ),
                rx.input(
                    placeholder="Ширина, м",
                    name="width",
                ),
                rx.input(
                    placeholder="Высота, м",
                    name="height",
                ),
                rx.dialog.root(
                    rx.dialog.trigger(rx.button("Подтвердить", type="submit")),
                    rx.dialog.content(
                        rx.dialog.title("Результаты заявки"),
                        rx.dialog.description(
                            FormState.car,
                        ),
                        rx.dialog.close(
                            rx.button("Закрыть", size="2"),
                        ),
                    ),
                ),
                align='center'
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        align='center'
    )


def index() -> rx.Component:
    return rx.fragment(
        navbar(add_car),
        rx.box(
            content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family="Tahoma"
    )


def requests() -> rx.Component:
    return rx.fragment(
        navbar(add_car, add_visible=False),
        rx.box(
            req(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family="Tahoma",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, accent_color="blue",
        stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
    )
)
app.add_page(index, on_load=State.on_load, title="Машины")
app.add_page(requests, route='/requests', title="Составить заявку")
