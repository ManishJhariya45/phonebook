import sqlite3

# Connect to the database
conn = sqlite3.connect('phonebook.db')

# Create a table to store contacts
conn.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        name TEXT PRIMARY KEY,
        phone TEXT
    )
''')

def display_contact():
    cursor = conn.execute("SELECT name, phone FROM contacts")
    print("Name\t\tContact Number")
    for row in cursor:
        print("{}\t\t{}".format(row[0], row[1]))

while True:
    Choice = int(input("1. Add Contact\n2. Search Contact\n3. Display Contact\n4. Update Contact\n5. Delete Contact\n6. Exit\nEnter your Operation: "))
    if Choice == 1:
        name = input("Enter Contact Name: ")
        phone = input("Enter the Phone Number: ")
        if len(phone) == 10:
            conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
            print("Contact added:", name, phone)
        else:
            print("Invalid phone number. Phone number should be 10 digits.")
    elif Choice == 2:
        search_name = input("Enter the Contact Name: ")
        cursor = conn.execute("SELECT phone FROM contacts WHERE name = ?", (search_name,))
        row = cursor.fetchone()
        if row:
            print(search_name, "contact number is", row[0])
        else:
            print("Name is not found")
    elif Choice == 3:
        cursor = conn.execute("SELECT COUNT(*) FROM contacts")
        count = cursor.fetchone()[0]
        if count == 0:
            print("Empty contact book")
        else:
            display_contact()
    elif Choice == 4:
        update_contact = input("Enter the Contact to be updated: ")
        cursor = conn.execute("SELECT phone FROM contacts WHERE name = ?", (update_contact,))
        row = cursor.fetchone()
        if row:
            phone = input("Enter Mobile Number: ")
            if len(phone) == 10:
                conn.execute("UPDATE contacts SET phone = ? WHERE name = ?", (phone, update_contact))
                conn.commit()
                print("Contact updated")
                display_contact()
            else:
                print("Invalid phone number. Phone number should be 10 digits.")
        else:
            print("Name is not found")
    elif Choice == 5:
        del_contact = input("Enter the Contact to be deleted: ")
        cursor = conn.execute("SELECT name FROM contacts WHERE name = ?", (del_contact,))
        row = cursor.fetchone()
        if row:
            confirm = input("Are you sure you want to delete this contact? (y/n): ")
            if confirm == 'y' or confirm == 'Y':
                conn.execute("DELETE FROM contacts WHERE name = ?", (del_contact,))
                conn.commit()
                display_contact()
        else:
            print("Name is not found")
    elif Choice == 6:
        break
    else:
        print("Phone Book is closed")

# Close the database connection
conn.close()