```mermaid
C4Context
title Система анализа и визуализации данных о компьютерных компонентах

Person(Admin, "Администратор", "Управляет системой")
Person(Analyst, "Аналитик", "Анализирует данные")

Boundary(WebLayer, "Веб-уровень") {
  System(DjangoAdmin, "Админ-панель", "[Django Admin]")
  System(DashApp, "Дашборды", "[Plotly Dash]")
}

Boundary(AppLayer, "Бизнес-логика") {
  System(DjangoCore, "Ядро приложения", "[Django ORM, Views]")
  System(DataService, "Сервис данных", "[Pandas, NumPy]")
  SystemDb(Database, "Хранилище", "[SQLite, PostgreSQL]")
}

Boundary(TestLayer, "Тестирование") {
  System(E2ETests, "End-to-end тесты", "[Playwright]")
  System(LoadTests, "Нагрузочные тесты", "[Locust]")
}

Boundary(Infra, "Инфраструктура") {
  System(Container, "Контейнеризация", "[Docker]")
  System(Env, "Виртуальное окружение", "[venv]")
}

Rel(Admin, DjangoAdmin, "Управление данными", "HTTP")
Rel(Analyst, DashApp, "Просмотр аналитики", "HTTP")
Rel(DjangoAdmin, DjangoCore, "CRUD операции", "Internal")
Rel(DashApp, DataService, "Запросы данных", "API")
Rel(DjangoCore, Database, "ORM запросы", "SQL")
Rel(DataService, Database, "Сырые запросы", "SQL")

Rel(E2ETests, DashApp, "Тестирование UI", "Playwright")
Rel(LoadTests, DjangoCore, "Нагрузка", "HTTP")
Rel(Container, Env, "Запускает", "Dockerfile")

UpdateRelStyle(Admin, DjangoAdmin, $offsetY="-60")
UpdateRelStyle(Analyst, DashApp, $offsetY="-40")
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

---

# Запуск проекта

## 1. Запуск контейнеров

```sh
cd /workspaces/codespaces-blank/project_practice
docker-compose up
```

## 2. Настройка окружения для Playwright

```sh
cd /workspaces/codespaces-blank/project_practice/playwright/
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
playwright install
playwright install-deps
```

## 3. Запуск тестов Playwright

```sh
pytest test.py -v
```

## 4. Настройка окружения для Locust

```sh
cd /workspaces/codespaces-blank/project_practice/locust/
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Запуск тестов Locust

```sh
locust -f locustfile.py
```

## Требования

- **Docker и Docker Compose**
- **Python (совместимая версия)**
- **Playwright**
- **Locust**
- **Установленные зависимости из `requirements.txt`**

После выполнения этих шагов проект будет готов к использованию.

