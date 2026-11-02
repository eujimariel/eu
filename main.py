# Author: Whole group (main.py)
"""Demo story: a lunch rush at the canteen. Only this file imports concrete classes."""
from contracts import CanteenError
from menu import Menu, MenuItem
from customer import StudentCustomer, StaffCustomer
from order import Order
from payment import Cash, EWallet
from kitchen import Kitchen


def main():
    menu = Menu([MenuItem("Adobo", 50, 3), MenuItem("Rice", 15, 20), MenuItem("Iced Tea", 25, 10)])
    kitchen = Kitchen(capacity=3)
    maria = StudentCustomer("Maria", balance=200)
    juan = StudentCustomer("Juan", balance=30)
    mr_cruz = StaffCustomer("Mr. Cruz", balance=0)

    print("=== Menu ===")
    for item in menu.items():
        print(" ", item)

    # 1) Maria pays with her e-wallet
    order1 = Order(1, maria)
    order1.add_item(menu.get_item("Adobo"), 2)
    order1.add_item(menu.get_item("Rice"), 2)
    order1.checkout(EWallet())
    kitchen.enqueue(order1)
    print(f"\n{order1}\n  Maria's balance now: P{maria.balance:.2f}")

    # 2) Mr. Cruz pays with cash and gets change
    order2 = Order(2, mr_cruz)
    order2.add_item(menu.get_item("Iced Tea"), 2)
    change = order2.checkout(Cash(100))
    kitchen.enqueue(order2)
    print(f"\n{order2}\n  Change: P{change:.2f}")

    # 3) RULE BROKEN: only 1 Adobo is left, Juan wants 2
    order3 = Order(3, juan)
    try:
        order3.add_item(menu.get_item("Adobo"), 2)
    except CanteenError as err:
        print(f"\n[Rule broken] {err}")

    # 4) RULE BROKEN: Juan cannot afford his order
    order3.add_item(menu.get_item("Adobo"), 1)
    order3.add_item(menu.get_item("Iced Tea"), 1)
    try:
        order3.checkout(EWallet())  # needs P75, has P30
    except CanteenError as err:
        print(f"[Rule broken] {err}")
    print(f"  Juan tops up P100 and tries again")
    juan.top_up(100)
    order3.checkout(EWallet())
    kitchen.enqueue(order3)

    # 5) Kitchen cooks in first-come-first-served order
    print(f"\n=== Kitchen: {kitchen} ===")
    while len(kitchen):
        done = kitchen.prepare_next()
        print(f"  Ready: {done}")


if __name__ == "__main__":
    main()
