import os
import timeit


# Реалізація алгоритму Кнута-Морріса-Пратта
# Створення lps-таблиці
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

# KMP алгоритм
def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# Реалізація алгоритму Боєра-Мура
# Створення таблиці зсувів
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

# Алгоритм Боєра-Мура
def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1



# Реалізація алгоритму Рабіна-Карпа
# Функція поліноміального хешу рядка s    
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

# Алгоритм Рабіна-Карпа
def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1



# Функція для вимірювання часу виконання алгоритму
def measure_time(algorithm, text, pattern):
    stmt = f"{algorithm}({text!r}, {pattern!r})"
    setup = f"from __main__ import {algorithm}"
    time_taken = timeit.timeit(stmt, setup, number=1000)
    return time_taken


# Завантаження текстових файлів та підрядків
# Вказати шлях до директорії:
directory = "C:\\Users\\vasyl\\Downloads"

# Скласти повний шлях до кожного файлу
file_one_path = os.path.join(directory, "text_one.txt")
file_two_path = os.path.join(directory, "text_two.txt")

# Перевірити наявність файлів
if os.path.exists(file_one_path) and os.path.exists(file_two_path):
    # Завантажити текстові файли
    with open(file_one_path, 'r') as file:
        text_one = file.read()
    with open(file_two_path, 'r') as file:
        text_two = file.read()
else:
    print("Не вдалося знайти один або обидва текстові файли")


# Підрядки для пошуку
existing_pattern = "https"
non_existing_pattern = "верес"



def main():
    # Вимірюємо час виконання для кожного алгоритму та кожного тексту
    algorithms = ['boyer_moore_search', 'kmp_search', 'rabin_karp_search']
    
    for algorithm in algorithms:
        # Для існуючого підрядка
        time_taken_text_one_existing = measure_time(algorithm, text_one, existing_pattern)
        time_taken_text_two_existing = measure_time(algorithm, text_two, existing_pattern)
        
        # Для вигаданого підрядка
        time_taken_text_one_non_existing = measure_time(algorithm, text_one, non_existing_pattern)
        time_taken_text_two_non_existing = measure_time(algorithm, text_two, non_existing_pattern)
    
        print(f"Час виконання алгоритму '{algorithm}' для тексту 1 (існуючий підрядок): {time_taken_text_one_existing: .5F} секунд")
        print(f"Час виконання алгоритму '{algorithm}' для тексту 1 (вигаданий підрядок): {time_taken_text_one_non_existing: .5F} секунд")
        print(f"Час виконання алгоритму '{algorithm}' для тексту 2 (існуючий підрядок): {time_taken_text_two_existing: .5F} секунд")
        print(f"Час виконання алгоритму '{algorithm}' для тексту 2 (вигаданий підрядок): {time_taken_text_two_non_existing: .5F} секунд")





if __name__ == "__main__":
    main()
