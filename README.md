# Canteen Ordering System (EXAMPLE)

**Scenario.** Students and staff order food at a school canteen. The menu keeps
prices and limited stock. Customers hold an e-wallet balance. An order is a cart
that is paid with cash or e-wallet, then goes to the kitchen queue and is cooked
first-come-first-served. Rules such as running out of stock, not having enough
money, or a full kitchen raise `CanteenError`.

| Module | Owner | Contract ABC it implements |
|---|---|---|
| menu | Student 1 | IMenuItem, IMenu |
| customer | Student 2 | ICustomer |
| order | Student 3 | IOrder |
| payment | Student 4 | IPayment |
| kitchen | Student 5 | IKitchen |

## How to run
```
python main.py
python -m unittest discover tests
```

## AI tools / references used
- Claude (AI) generated this whole example to show the structure. A real group
  must write its own code and list how AI was used here.

## Contract change log
- (none yet)
