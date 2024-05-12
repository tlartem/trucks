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
                rx.flex(
                    rx.switch(default_checked=False, checked=~State.switchBusyStatus, on_change=lambda v: State.switch_busy(~v)),
                    rx.text("Свободные"),
                    spacing="2",
                ),
                rx.flex(
                    rx.switch(default_checked=False, checked=~State.switchFreeStatus, on_change=lambda v: State.switch_free(~v)),
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
    return rx.form(
        rx.flex(
            rx.input(
                placeholder="Text to translate",
                debounce_timeout=300,
                size="3",
                name="text",
            ),
            rx.select(
                placeholder="Select a language",
                margin_top="1rem",
                size="3",
                items=['fruit', 'apple', 'banana']
            ),
            rx.button(
                "Post",
                size="3",
            ),
            direction="column",
            spacing="4",
            width="100%",
            align="center"
        )
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