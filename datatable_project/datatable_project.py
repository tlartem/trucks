from rxconfig import config
from components.navbar import navbar
import reflex as rx
from components.state import *

filename = f"{config.app_name}/{config.app_name}.py"


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
                rx.select(
                    ["Сортировка: грузоподъемность", "Сортировка: длина", "Сортировка: ширина", "Сортировка: высота"],
                    default_value="Сортировка: грузоподъемность",
                    size="3",
                    on_change=lambda sort_value: State.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="2em",
                padding_bottom="1em",
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


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, accent_color="blue",
        stylesheets=["https://fonts.googleapis.com/css?family=Inter"],
    )
)
app.add_page(index, on_load=State.on_load, title="Машины")
