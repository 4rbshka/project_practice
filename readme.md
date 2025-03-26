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

## 3. Запуск тестов

```sh
pytest test.py -v
```

## Требования

- **Docker и Docker Compose**
- **Python (совместимая версия)**
- **Playwright**
- **Установленные зависимости из `requirements.txt`**

После выполнения этих шагов проект будет готов к использованию.

