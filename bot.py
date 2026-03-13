import json
import os
from datetime import datetime


DATA_FILE = "finance_data.json"

def load_data():
    """Завантажує дані з JSON файлу. Якщо файлу немає, створює порожню структуру."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"budget": 0.0, "expenses": []}

def save_data(data):
    """Зберігає поточні дані у JSON файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def print_help():
    """Виводить список доступних команд."""
    print("\n--- Доступні команди ---")
    print("допомога - показати це меню")
    print("встановити бюджет - задати загальну суму бюджету")
    print("додати витрату - внести нову витрату")
    print("показати витрати - переглянути всі витрати (з можливістю фільтрації)")
    print("залишок - переглянути залишок коштів")
    print("звіт за категоріями - показати загальну суму витрат по кожній категорії")
    print("вийти - завершити роботу програми")
    print("------------------------\n")

def set_budget(data):
    """Встановлює загальний бюджет користувача."""
    try:
        amount = float(input("Введіть суму бюджету: "))
        if amount < 0:
            print("Бюджет не може бути від'ємним!")
            return
        data["budget"] = amount
        save_data(data)
        print(f"Бюджет успішно встановлено: {amount} грн.")
    except ValueError:
        print("Помилка: введіть числове значення.")

def get_total_expenses(data):
    """Допоміжна функція для підрахунку загальної суми витрат."""
    return sum(item["amount"] for item in data["expenses"])

def add_expense(data):
    """Додає нову витрату та перевіряє ліміт бюджету."""
    try:
        amount = float(input("Введіть суму витрати: "))
        if amount <= 0:
            print("Сума має бути більшою за нуль.")
            return
            
        category = input("Введіть категорію (наприклад, Їжа, Транспорт): ").strip().capitalize()
        date_str = input("Введіть дату (у форматі ДД.ММ.РРРР) або натисніть Enter для сьогоднішньої: ").strip()
        
        if not date_str:
            date_str = datetime.now().strftime("%d.%m.%Y")
        else:
            # Перевірка правильності формату дати
            datetime.strptime(date_str, "%d.%m.%Y")
            
        comment = input("Додайте короткий коментар (необов'язково): ").strip()
        
        expense = {
            "amount": amount,
            "category": category,
            "date": date_str,
            "comment": comment
        }
        
        data["expenses"].append(expense)
        save_data(data)
        print("Витрату успішно додано!")
        
        # Перевірка перевищення бюджету
        total_expenses = get_total_expenses(data)
        if total_expenses > data["budget"]:
            print(f"⚠️ УВАГА: Ви перевищили свій бюджет! Загальні витрати ({total_expenses} грн) більші за бюджет ({data['budget']} грн).")
            
    except ValueError:
        print("Помилка: некоректне введення суми або дати.")

def print_expenses_list(expenses_list):
    """Допоміжна функція для красивого виведення списку витрат."""
    if not expenses_list:
        print("Список витрат порожній.")
        return
        
    for i, exp in enumerate(expenses_list, 1):
        comment_str = f" ({exp['comment']})" if exp['comment'] else ""
        print(f"{i}. Дата: {exp['date']} | Категорія: {exp['category']} | Сума: {exp['amount']} грн{comment_str}")

def show_expenses(data):
    """Виводить список витрат з можливістю застосування фільтрів."""
    print("Оберіть режим перегляду:")
    print("1 - Всі витрати")
    print("2 - За конкретну дату")
    print("3 - За категорією")
    print("4 - За період (між двома датами)")
    
    choice = input("Ваш вибір (1/2/3/4): ").strip()
    
    if choice == '1':
        print("\n--- Всі витрати ---")
        print_expenses_list(data["expenses"])
        
    elif choice == '2':
        target_date = input("Введіть дату (ДД.ММ.РРРР): ").strip()
        filtered = [e for e in data["expenses"] if e["date"] == target_date]
        print(f"\n--- Витрати за {target_date} ---")
        print_expenses_list(filtered)
        
    elif choice == '3':
        target_category = input("Введіть категорію: ").strip().capitalize()
        filtered = [e for e in data["expenses"] if e["category"] == target_category]
        print(f"\n--- Витрати у категорії '{target_category}' ---")
        print_expenses_list(filtered)
        
    elif choice == '4':
        try:
            start_str = input("Введіть початкову дату (ДД.ММ.РРРР): ").strip()
            end_str = input("Введіть кінцеву дату (ДД.ММ.РРРР): ").strip()
            
            start_date = datetime.strptime(start_str, "%d.%m.%Y")
            end_date = datetime.strptime(end_str, "%d.%m.%Y")
            
            filtered = []
            for e in data["expenses"]:
                exp_date = datetime.strptime(e["date"], "%d.%m.%Y")
                if start_date <= exp_date <= end_date:
                    filtered.append(e)
                    
            print(f"\n--- Витрати з {start_str} по {end_str} ---")
            print_expenses_list(filtered)
            
        except ValueError:
            print("Помилка: неправильний формат дати.")
    else:
        print("Невідомий вибір.")

def show_balance(data):
    """Обчислює та виводить залишок бюджету."""
    total_expenses = get_total_expenses(data)
    balance = data["budget"] - total_expenses
    
    print(f"\nЗагальний бюджет: {data['budget']} грн")
    print(f"Сума всіх витрат: {total_expenses} грн")
    print(f"Залишок коштів: {balance} грн\n")

def category_report(data):
    """Формує та виводить звіт про сумарні витрати за кожною категорією."""
    report = {}
    for exp in data["expenses"]:
        cat = exp["category"]
        report[cat] = report.get(cat, 0) + exp["amount"]
        
    print("\n--- Звіт за категоріями ---")
    if not report:
        print("Витрат ще немає.")
    else:
        for cat, total in report.items():
            print(f"{cat}: {total} грн")
    print("---------------------------\n")

def main():
    """Головна функція програми (точка входу)."""
    print("========================================")
    print("Привіт! Я твій бот 'Фінансовий трекер'.")
    print("Допоможу тобі контролювати бюджет та витрати.")
    print("========================================")
    
    
    data = load_data()
    print_help()
    
    while True:
        command = input("\nВведіть команду: ").strip().lower()
        
        if command == "допомога":
            print_help()
        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт за категоріями":
            category_report(data)
        elif command == "вийти":
            print("Дані збережено. До зустрічі!")
            break
        else:
            print("Невідома команда. Введіть 'допомога' для списку команд.")

if __name__ == "__main__":
    main()