import flet as ft

def main(page: ft.Page):
    # Настройка страницы
    page.title = "Кликер"
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # Счётчик кликов
    clicks = ft.Ref[ft.Text]()

    def increment_click(e):
        current_clicks = int(clicks.current.value.split(": ")[1])
        clicks.current.value = f"Клики: {current_clicks + 1}"
        page.update()

    # Создание интерфейса
    page.add(
        ft.Stack(
            [
                # Фон
                ft.Container(
                    content=ft.Image(
                        src=r"D:\Python\Clicker\Clicker\Icons\background.png",
                        width=800,
                        height=600,
                        fit=ft.ImageFit.FILL,
                    ),
                    width=800,
                    height=600,
                ),
                
                # Счётчик (верхний правый угол)
                ft.Container(
                    content=ft.Text(
                        ref=clicks,
                        value="Клики: 0",
                        size=30,
                        color="white",
                        weight=ft.FontWeight.BOLD
                    ),
                    top=20,
                    right=20,
                    padding=10,
                ),
                
                # Кликабельная картинка по центру (УВЕЛИЧЕННАЯ)
                ft.Container(
                    content=ft.Image(
                        src=r"D:\Python\Clicker\Clicker\Icons\MacanIcon.png",
                        width=300,  # Увеличено с 200 до 300
                        height=300, # Увеличено с 200 до 300
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    alignment=ft.alignment.center,
                    on_click=increment_click,
                    width=400,  # Увеличено с 300 до 400
                    height=400, # Увеличено с 300 до 400
                    top=100,    # Скорректировано положение
                    left=200,   # Скорректировано положение
                )
            ],
            width=800,
            height=600,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)