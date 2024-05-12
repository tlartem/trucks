import reflex as rx


def navbar(add_customer, add_visible=True):
    if not add_visible:
        add_customer = lambda: rx.button("Добавить заявку")
    return rx.hstack(
        rx.image(src="/logo.png", width="7em"),
        rx.link("Таблица автомобилей", href="/"),
        rx.link("Обработка заявок", href="/requests"),
        rx.spacer(),
        add_customer(),

        position="fixed",
        top="0px",
        background_color="white",
        padding="1em",
        height="4em",
        width="100%",
        z_index="5",
        border_bottom="0.1em solid #F0F0F0",
        align="center",
        spacing="4"
    )
