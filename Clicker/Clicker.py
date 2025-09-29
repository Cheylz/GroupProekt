import flet as ft
import os

def main(page: ft.Page):
    # Настройка страницы
    page.title = "Кликер"
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # Получение абсолютного пути к папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(project_dir, "Icons")
    
    # Счётчик кликов
    clicks = ft.Ref[ft.Text]()
    # Референс для кликабельной картинки
    clickable_image = ft.Ref[ft.Image]()

    def increment_click(e):
        current_clicks = int(clicks.current.value.split(": ")[1])
        new_clicks = current_clicks + 1
        clicks.current.value = f"Клики: {new_clicks}"
        
        # Смена картинки при достижении 100 кликов
        if new_clicks == 100:
            new_image_path = os.path.join(icons_dir, "secondMakan.png")  # Замените на имя вашей новой картинки
            if os.path.exists(new_image_path):
                clickable_image.current.src = new_image_path
            else:
                # Если файл не найден, используем fallback
                fallback_path = os.path.join(icons_dir, "MacanIconUpgraded.png")
                clickable_image.current.src = fallback_path
        
        page.update()

    # Создание интерфейса
    page.add(
        ft.Stack(
            [
                # Фон
                ft.Container(
                    content=ft.Image(
                        src=os.path.join(icons_dir, "background.png"),
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
                        ref=clickable_image,
                        src=os.path.join(icons_dir, "MacanIcon.png"),
                        width=300,
                        height=300,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    alignment=ft.alignment.center,
                    on_click=increment_click,
                    width=400,
                    height=400,
                    top=100,
                    left=200,
                )
            ],
            width=800,
            height=600,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)