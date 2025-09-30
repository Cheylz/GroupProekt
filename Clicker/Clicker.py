import flet as ft
import os
import sys
import json

def main(page: ft.Page):
    # Настройка страницы
    page.title = "MakanForever"
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.padding = 0

    # Получение абсолютного пути к папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(project_dir, "Icons")
    save_path_json = os.path.join(os.path.dirname(sys.executable), "save.json")
    save_path_txt = os.path.join(os.path.dirname(sys.executable), "save.txt")
    
    # Переменные состояния
    current_clicks = 0
    clicks_per_click = 1
    upgrade_level = 0
    hundred_reached = False

    # Загрузка сохранения
    try:
        if os.path.exists(save_path_json):
            with open(save_path_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_clicks = data.get("counter", 0)
        elif os.path.exists(save_path_txt):
            with open(save_path_txt, "r", encoding="utf-8") as f:
                current_clicks = int(f.read())
    except Exception as err:
        print("Ошибка при загрузке сохранения:", err)
        current_clicks = 0
    
    # Стоимости улучшений
    upgrade_costs = [50, 150, 300, 450, 600]
    
    # Создаем элементы интерфейса
    clicks_text = ft.Text(value=f"Клики: {current_clicks}", size=30, color="white", weight="bold")
    upgrade_text = ft.Text(value="Улучшение +1\n(50 кликов)\nУр. 1", size=16, color="black", weight="bold", text_align="center")
    
    # Основное изображение для кликов
    main_image = ft.Image(
        src=os.path.join(icons_dir, "MacanIcon.png"),
        width=300,
        height=300,
        fit="contain",
    )
    
    # Контейнер для кнопки улучшения
    upgrade_container = ft.Container(
        content=ft.Column(
            [
                upgrade_text
            ],
            horizontal_alignment="center",
            spacing=5,
            alignment="center"
        ),
        padding=10,
        border=ft.border.all(2, "black"),
        border_radius=10,
        bgcolor="gray",
        width=140,
        height=140,
    )
    
    def update_counter():
        clicks_text.value = f"Клики: {current_clicks}"
        
        # Обновляем текст кнопки улучшения
        if upgrade_level < len(upgrade_costs):
            cost = upgrade_costs[upgrade_level]
            upgrade_text.value = f"Улучшение +2\n({cost} кликов)\nУр. {upgrade_level + 1}"
            
            # Меняем цвет кнопки в зависимости от доступности
            upgrade_container.bgcolor = "green" if current_clicks >= cost else "gray"
        else:
            upgrade_text.value = "Макс. уровень"
            upgrade_container.bgcolor = "blue"
            
        page.update()

    def increment_click(e):
        nonlocal current_clicks, hundred_reached
        current_clicks += clicks_per_click
        update_counter()
        
        # Смена картинки при достижении 100 кликов
        if current_clicks >= 100 and not hundred_reached:
            hundred_reached = True
            new_image_path = os.path.join(icons_dir, "secondMakan.png")
            if os.path.exists(new_image_path):
                main_image.src = new_image_path
            else:
                fallback_path = os.path.join(icons_dir, "MacanIconUpgraded.png")
                main_image.src = fallback_path
            page.update()

    def buy_upgrade(e):
        nonlocal current_clicks, clicks_per_click, upgrade_level
        if upgrade_level < len(upgrade_costs):
            cost = upgrade_costs[upgrade_level]
            if current_clicks >= cost:
                current_clicks -= cost
                clicks_per_click += 2
                upgrade_level += 1
                update_counter()
    
    # Назначаем обработчики событий
    upgrade_container.on_click = buy_upgrade
    
    main_image_container = ft.Container(
        content=main_image,
        alignment=ft.alignment.center,
        on_click=increment_click,
        width=400,
        height=400,
    )

    # Создание интерфейса
    background_image = ft.Image(
        src=os.path.join(icons_dir, "background.png"),
        width=800,
        height=600,
        fit="fill",
    )

    def change_background(e):
        if background_image.src.endswith("background.png"):
            background_image.src = os.path.join(icons_dir, "mskcity.jpg")
        else:
            background_image.src = os.path.join(icons_dir, "background.png")
        page.update()

    change_bg_button = ft.TextButton(
        text="Сменить фон",
        on_click=change_background,
        style=ft.ButtonStyle(
            bgcolor="white",
            color="black",
            padding=10,
        )
    )
    def open_menu(e):
        page.go("/menu")
    
    menu_button = ft.TextButton(
    text="Меню",
    on_click=open_menu,
    style=ft.ButtonStyle(
        bgcolor="white",
        color="black",
        padding=10,
    )
)


    page.add(
        ft.Stack(
            [
                ft.Container(
                    content=background_image,
                    width=800,
                    height=600,
                ),
                
                ft.Container(
                    content=clicks_text,
                    top=450,
                    left=310,
                    padding=10,
                ),
                
                ft.Container(
                    content=upgrade_container,
                    top=230,
                    left=30,
                ),
                
                ft.Container(
                    content=main_image_container,
                    top=100,
                    left=200,
                ),
                ft.Container(
                    content=change_bg_button,
                    top=20,
                    left=20,
                ),
                ft.Container(
                    content=menu_button,
                    top=20,
                    right=20,
                ),
            ],
            width=800,
            height=600,
        )
    )
    
    def route_change(e):
        if page.route == "/menu":
            page.views.clear()

            menu_background = ft.Container(
                bgcolor="#1e1e1e",
                width=800,
                height=600,
            )

            menu_title = ft.Text(
                "Пауза",
                size=40,
                weight="bold",
                color="white",
                text_align="center"
            )

            def close_app(e):
                try:
                    with open(save_path_json, "w", encoding="utf-8") as f:
                        json.dump({"counter": current_clicks}, f)
                    with open(save_path_txt, "w", encoding="utf-8") as f:
                        f.write(str(current_clicks))
                except Exception as err:
                    print("Ошибка при сохранении:", err)
                page.window.close()

            resume_button = ft.ElevatedButton(
                text="Продолжить",
                style=ft.ButtonStyle(bgcolor="#08960c", color="white"),
                on_click=lambda e: page.go("/")
            )

            exit_button = ft.ElevatedButton(
                text="Выход",
                style=ft.ButtonStyle(bgcolor="#971910", color="white"),
                on_click=close_app
            )
            def reset_save(e):
                nonlocal current_clicks, clicks_per_click, upgrade_level, hundred_reached
                try:
                    if os.path.exists(save_path_json):
                        os.remove(save_path_json)
                    if os.path.exists(save_path_txt):
                        os.remove(save_path_txt)
                except Exception as err:
                    print("Ошибка при удалении сохранений:", err)
                current_clicks = 0
                clicks_per_click = 1
                upgrade_level = 0
                hundred_reached = False
                update_counter()
                page.go("/") 
            
            reset_button = ft.ElevatedButton(
                text="Сбросить сохранения",
                style=ft.ButtonStyle(bgcolor="#555555", color="white"),
                on_click=reset_save
            )
        

            menu_layout = ft.Column(
                [
                    menu_title,
                    ft.Divider(thickness=2, color="white"),
                    resume_button,
                    reset_button,
                    exit_button
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=25
            )

            page.views.append(
                ft.View(
                    "/menu",
                    controls=[
                        ft.Stack([
                            menu_background,
                            ft.Container(content=menu_layout, alignment=ft.alignment.center)
                        ])
                    ]
                )
            )

        elif page.route == "/":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    controls=[page.controls[0]]
                )
            )
        page.update()

    def on_close(e):
        try:
            with open(save_path_json, "w", encoding="utf-8") as f:
                json.dump({"counter": current_clicks}, f)
            with open(save_path_txt, "w", encoding="utf-8") as f:
                f.write(str(current_clicks))
        except Exception as err:
            print("Ошибка при сохранении:", err)

    page.on_window_event = lambda e: on_close(e) if e.data == "close" else None
    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
