
from datetime import date, timedelta

# =====================================================================
# 1. CONSTANTS & LIBRARY RULES
# =====================================================================

LOAN_DAYS = 14
FINE_PER_DAY = 2
MAX_BOOKS_PER_MEMBER = 3

# =====================================================================
# 2. IN-MEMORY DATA LISTS (Pure Python Dictionaries)
# =====================================================================

books = []
members = []
issued_books = []
reservations = []

# Book: {"id", "title", "author", "total_copies"}
# Member: {"id", "name", "phone"}
# Issue: {"issue_id", "book_id", "member_id",
#         "issue_date", "due_date", "return_date", "fine"}
# Reservation: {"book_id", "member_id", "date", "status"}

# =====================================================================
# 3. HELPER & VALIDATION FUNCTIONS
# =====================================================================

def today_date():
    return date.today()


def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)


def find_member(member_id):
    return next((m for m in members if m["id"] == member_id), None)


def get_available_copies(book_id):
    book = find_book(book_id)

    if book is None:
        return 0

    issued_count = sum(
        1 for i in issued_books
        if i["book_id"] == book_id
        and i["return_date"] is None
    )

    return book["total_copies"] - issued_count


def get_active_issues(member_id):
    return [
        i for i in issued_books
        if i["member_id"] == member_id
        and i["return_date"] is None
    ]


# =====================================================================
# 4. CORE FEATURE 1: ADD BOOKS
# =====================================================================

def add_book():

    print("\n===== ADD NEW BOOK =====")

    book_id = input("Enter Book ID: ").strip()

    if find_book(book_id):
        print("[!] Book ID already exists.")
        return

    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    try:
        copies = int(input("Enter Number of Copies: "))

        if copies <= 0:
            print("[!] Copies must be greater than zero.")
            return

    except ValueError:
        print("[!] Enter a valid number.")
        return

    books.append({
        "id": book_id,
        "title": title,
        "author": author,
        "total_copies": copies
    })

    print("[SUCCESS] Book added successfully!")


# =====================================================================
# 5. MEMBER REGISTRATION
# =====================================================================

def register_member():

    print("\n===== REGISTER MEMBER =====")

    member_id = input("Enter Member ID: ").strip()

    if find_member(member_id):
        print("[!] Member already exists.")
        return

    name = input("Enter Member Name: ").strip()
    phone = input("Enter Phone Number: ").strip()

    members.append({
        "id": member_id,
        "name": name,
        "phone": phone
    })

    print("[SUCCESS] Member registered successfully!")


# =====================================================================
# 6. CORE FEATURE 2: ISSUE A BOOK
# =====================================================================

def issue_book():

    print("\n===== ISSUE BOOK =====")

    book_id = input("Enter Book ID: ").strip()
    member_id = input("Enter Member ID: ").strip()

    book = find_book(book_id)
    member = find_member(member_id)

    if book is None:
        print("[!] Book not found.")
        return

    if member is None:
        print("[!] Member not found.")
        return

    active_issues = get_active_issues(member_id)

    if len(active_issues) >= MAX_BOOKS_PER_MEMBER:
        print("[!] Member has reached the borrowing limit.")
        return

    if get_available_copies(book_id) <= 0:
        print("[!] No copies available.")
        return

    issue_date = today_date()
    due_date = issue_date + timedelta(days=LOAN_DAYS)

    issue_id = f"I{len(issued_books) + 101}"

    issued_books.append({
        "issue_id": issue_id,
        "book_id": book_id,
        "member_id": member_id,
        "issue_date": issue_date,
        "due_date": due_date,
        "return_date": None,
        "fine": 0
    })

    print("\n[SUCCESS] Book issued successfully!")
    print("Book Title:", book["title"])
    print("Member:", member["name"])
    print("Issue Date:", issue_date)
    print("Due Date:", due_date)


# =====================================================================
# 7. CORE FEATURE 3: RETURN BOOK & CALCULATE FINE
# =====================================================================

def return_book():

    print("\n===== RETURN BOOK =====")

    issue_id = input("Enter Issue ID: ").strip()

    issue = next(
        (i for i in issued_books
         if i["issue_id"] == issue_id
         and i["return_date"] is None),
        None
    )

    if issue is None:
        print("[!] Active issue record not found.")
        return

    return_date = today_date()

    overdue_days = max(
        0, (return_date - issue["due_date"]).days
    )

    fine = overdue_days * FINE_PER_DAY

    issue["return_date"] = return_date
    issue["fine"] = fine

    print("\n[SUCCESS] Book returned successfully!")
    print("Overdue Days:", overdue_days)
    print("Fine Amount: Rs.", fine)

    # Notify first waiting reservation
    notify_first_reserver(issue["book_id"])


# =====================================================================
# 8. CORE FEATURE 4: SEARCH BOOKS BY TITLE OR AUTHOR
# =====================================================================

def search_books():

    print("\n===== SEARCH BOOKS =====")

    keyword = input("Enter Book Title or Author: ").strip().lower()

    results = [
        b for b in books
        if keyword in b["title"].lower()
        or keyword in b["author"].lower()
    ]

    if not results:
        print("[!] No books found.")
        return

    print("\nID       TITLE                AUTHOR          AVAILABLE")

    for b in results:
        available = get_available_copies(b["id"])

        print(
            f"{b['id']:<8} "
            f"{b['title']:<20} "
            f"{b['author']:<15} "
            f"{available}"
        )


# =====================================================================
# 9. CORE FEATURE 5: OVERDUE BOOK REPORT
# =====================================================================

def overdue_report():

    print("\n===== OVERDUE BOOK REPORT =====")

    today = today_date()
    found = False

    for issue in issued_books:

        if issue["return_date"] is not None:
            continue

        if today > issue["due_date"]:

            book = find_book(issue["book_id"])
            member = find_member(issue["member_id"])

            overdue_days = (today - issue["due_date"]).days

            estimated_fine = overdue_days * FINE_PER_DAY

            print("\nBook:", book["title"])
            print("Member:", member["name"])
            print("Member ID:", member["id"])
            print("Phone:", member["phone"])
            print("Due Date:", issue["due_date"])
            print("Overdue Days:", overdue_days)
            print("Current Fine: Rs.", estimated_fine)

            found = True

    if not found:
        print("No overdue books found.")


# =====================================================================
# 10. STRETCH FEATURE 1: BOOK RESERVATION
# =====================================================================

def reserve_book():

    print("\n===== RESERVE BOOK =====")

    book_id = input("Enter Book ID: ").strip()
    member_id = input("Enter Member ID: ").strip()

    book = find_book(book_id)
    member = find_member(member_id)

    if book is None or member is None:
        print("[!] Invalid Book ID or Member ID.")
        return

    if get_available_copies(book_id) > 0:
        print("[!] A copy is already available. Issue it instead.")
        return

    reservations.append({
        "book_id": book_id,
        "member_id": member_id,
        "date": today_date(),
        "status": "WAITING"
    })

    print("[SUCCESS] Reservation added to waiting list.")


def notify_first_reserver(book_id):

    for reservation in reservations:

        if (reservation["book_id"] == book_id
                and reservation["status"] == "WAITING"):

            member = find_member(reservation["member_id"])

            reservation["status"] = "NOTIFIED"

            print("\n[NOTIFICATION]")
            print("Book is now available for:", member["name"])
            print("Member ID:", member["id"])

            return

# =====================================================================
# 11. MAIN MENU
# =====================================================================

def print_menu():

    print("\n" + "=" * 65)
    print("       CP-035 SHELFWISE: LIBRARY MANAGEMENT SYSTEM")
    print("=" * 65)

    print(" 1. Add New Book")
    print(" 2. Register Member")
    print(" 3. Issue Book")
    print(" 4. Return Book")
    print(" 5. Search Books")
    print(" 6. Overdue Book Report")
    print(" 7. Reserve Book")
    print(" 0. Exit Application")

    print("=" * 65)


# =====================================================================
# 12. MAIN FUNCTION & MENU LOOP
# =====================================================================

def main():

    while True:

        print_menu()

        choice = input("Select an option (0-7): ").strip()

        if choice == "1":
            add_book()

        elif choice == "2":
            register_member()

        elif choice == "3":
            issue_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            search_books()

        elif choice == "6":
            overdue_report()

        elif choice == "7":
            reserve_book()

        elif choice == "0":
            print("Thank you for using ShelfWise!")
            break

        else:
            print("[!] Invalid choice. Enter 0-7.")


if __name__ == "__main__":
    main()
