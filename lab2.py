import csv 
import random
import xml.etree.ElementTree as ET
# We open the file and use delimiter=';' because the CSV data is separated by semicolons
with open('books-en.csv', 'r', encoding='windows-1252') as file:
    reader = csv.reader(file, delimiter=';')
    
    # This skips the first row (the headers like ISBN, Book-Title, etc.)
    next(reader)
    
    count = 0
    
    # We loop through every row in the file
    for row in reader:
        title = row[1]  # row[1] is the Book-Title column
        
        # Check if the length of the title is greater than 30
        if len(title) > 30:
            count += 1
            
    # Print the final result
    print(f"Number of records with a title longer than 30 characters: {count}")
    print("\n--- Поиск книг по автору (Вариант 2: только 1991 и 1996 годы) ---")

# Ask the user for the author's name and convert to lowercase for easier matching
search_author = input("Введите имя автора (например, King, Rowling): ").lower()
found = False

# Open the file again to search
with open('books-en.csv', 'r', encoding='windows-1252') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader) # Skip headers
    
    for row in reader:
        author = row[2].lower() # Column 2 is Author
        year = row[3]           # Column 3 is Year
        
        # Check if the author name matches AND the year is 1991 or 1996 (Variant 2)
        if search_author in author and year in ['1991', '1996']:
            # row[1] is title, row[2] is original author name
            print(f"Найдено: {row[1]} | Автор: {row[2]} | Год: {year}")
            found = True

if not found:
    print("Книги этого автора (1991 или 1996 года) не найдены.")
    print("\n--- Генерация 20 библиографических ссылок ---")

all_books = []
with open('books-en.csv', 'r', encoding='windows-1252') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)
    for row in reader:
        all_books.append(row)

# Pick 20 random books from the list
random_books = random.sample(all_books, 20)

# Open a new text file to write the results
with open('result.txt', 'w', encoding='utf-8') as out_file:
    # Loop through the 20 books, using 'enumerate' to get a line number (1, 2, 3...)
    for i, book in enumerate(random_books, start=1):
        author = book[2]
        title = book[1]
        year = book[3]
        
        # Format: <author>. <title> - <year>
        reference = f"{author}. {title} - {year}"
        
        # Write to the file with the line number
        out_file.write(f"{i}. {reference}\n")
        
        # Also print it to the screen so we can see it
        print(f"{i}. {reference}")

print("\nSuccess! Check the 'result.txt' file in your left sidebar.")
print("\n--- Парсинг currency.xml (Вариант 2: Два списка Name и Value) ---")

# Parse the XML file
tree = ET.parse('currency.xml')
root = tree.getroot()

# Create two empty lists for Name and Value
names_list = []
values_list = []

# Loop through every <Valute> tag in the XML
for valute in root.findall('Valute'):
    # Find the <Name> and <Value> tags inside the <Valute> tag
    name_tag = valute.find('Name')
    value_tag = valute.find('Value')
    
    # Extract the text inside the tags
    if name_tag is not None and value_tag is not None:
        name = name_tag.text
        value_str = value_tag.text
        
        # Type conversion: The XML uses commas for decimals (e.g., 59,8944). 
        # We need to replace the comma with a dot so Python can convert it to a float.
        value_float = float(value_str.replace(',', '.'))
        
        # Add them to our lists
        names_list.append(name)
        values_list.append(value_float)

# Print the results
print(f"Количество валют: {len(names_list)}")
print("\nСписок Name:")
print(names_list)
print("\nСписок Value:")
print(values_list)
print("\n--- Допзадание 1: Уникальные издательства ---")

# We use a 'set' because sets automatically remove duplicates
unique_publishers = set()

with open('books-en.csv', 'r', encoding='windows-1252') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)
    for row in reader:
        # row[4] is the Publisher column
        if len(row) > 4: 
            unique_publishers.add(row[4])

print(f"Всего уникальных издательств: {len(unique_publishers)}")
print("Список издательств:")
for publisher in unique_publishers:
    print(f"- {publisher}")


print("\n--- Допзадание 2: 20 самых популярных книг (по скачиваниям) ---")

# We will use the 'all_books' list we created earlier in Step 3.
# We need to sort it by the Downloads column (row[5]).
# We use a 'try/except' just in case a row has empty or broken data.
def get_downloads(book):
    try:
        return int(book[5])
    except (ValueError, IndexError):
        return 0

# Sort the list from highest to lowest (reverse=True)
sorted_books = sorted(all_books, key=get_downloads, reverse=True)

# Print the top 20
for i in range(20):
    if i < len(sorted_books):
        book = sorted_books[i]
        # row[1] = Title, row[2] = Author, row[5] = Downloads
        print(f"{i+1}. {book[1]} | Автор: {book[2]} | Скачиваний: {book[5]}")