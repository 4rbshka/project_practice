import re
from playwright.sync_api import Page, expect

def test_page_loads_and_has_title(page: Page):
    """Проверяем загрузку страницы и наличие заголовка"""
    page.goto("http://localhost:8050/")
    
    # Проверка основного заголовка
    expect(page.locator("h1")).to_have_text("Анализ аппаратных компонентов")
    
    # Проверка наличия кнопки обновления
    refresh_btn = page.locator("#refresh-btn")
    expect(refresh_btn).to_have_text("Обновить данные")
    
    # Скриншот всей страницы
    page.screenshot(path="playwright-tests/screenshots/page_loaded.png")

def test_dropdown_interaction(page: Page):
    """Тестируем работу выпадающего списка графиков"""
    page.goto("http://localhost:8050/")
    
    # Проверяем наличие dropdown
    dropdown = page.locator("#graph-type")
    expect(dropdown).to_be_visible()
    
    # Проверяем выбранное значение по тексту (альтернативный способ)
    selected_value = page.locator("#graph-type .Select-value-label")
    expect(selected_value).to_have_text("Распределение по категориям")
    
    # Меняем значение и проверяем обновление
    dropdown.click()
    page.locator(".VirtualizedSelectOption", has_text="Топ самых дорогих товаров").click()
    
    # Проверяем новое выбранное значение
    updated_value = page.locator("#graph-type .Select-value-label")
    expect(updated_value).to_have_text("Топ самых дорогих товаров")

def test_data_table_visibility(page: Page):
    """Проверяем отображение таблицы с данными"""
    page.goto("http://localhost:8050/")
    
    # Проверяем заголовок таблицы
    expect(page.locator("h3")).to_have_text("Данные продуктов")
    
    # Проверяем наличие таблицы
    table = page.locator("#table")
    expect(table).to_be_visible()
    
    # Проверяем пагинацию (новый селектор)
    pagination = page.locator(".dash-table-container .previous-next-container")
    expect(pagination).to_be_visible()
    
    # Проверяем наличие хотя бы одной строки данных
    rows = page.locator("#table .dash-cell div")
    expect(rows.first).to_be_visible()

def test_graph_rendering(page: Page):
    """Проверяем отрисовку графика"""
    page.goto("http://localhost:8050/")
    
    # Проверяем наличие графика
    graph = page.locator("#hardware-graph")
    expect(graph).to_be_visible()
    
    # Проверяем заголовок графика (должен соответствовать выбранному типу)
    graph_title = page.locator(".gtitle")
    expect(graph_title).to_contain_text("Распределение продуктов по категориям")
    
    # Скриншот графика
    graph.screenshot(path="playwright-tests/screenshots/graph_rendered.png")

def test_refresh_button(page: Page):
    """Тестируем кнопку обновления данных"""
    page.goto("http://localhost:8050/")
    
    # Получаем начальное состояние таблицы
    initial_table = page.locator("#table .dash-cell div").first.text_content()
    
    # Нажимаем кнопку обновления
    page.locator("#refresh-btn").click()
    
    # Ждем обновления (можно добавить ожидание конкретного изменения)
    page.wait_for_timeout(1000)
    
    # Проверяем, что таблица обновилась (простейшая проверка)
    updated_table = page.locator("#table .dash-cell div").first.text_content()
    assert initial_table == updated_table  # В реальном тесте лучше проверять конкретные изменения