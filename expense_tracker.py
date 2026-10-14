"""Expense tracker with JSON storage and CSV/JSON export."""
import csv, json
from datetime import date
from pathlib import Path
DATA = Path(__file__).with_name("expenses.json")
FIELDS = ["id", "date", "category", "description", "amount"]
def load():
    try:
        x = json.loads(DATA.read_text(encoding="utf-8")); return x if isinstance(x, list) else []
    except (OSError, json.JSONDecodeError): return []
def save(items): DATA.write_text(json.dumps(items, indent=2), encoding="utf-8")
def show(items):
    if not items: print("No expenses yet."); return
    print("ID | Date       | Category     | Amount | Description")
    for x in items: print(f"{x['id']} | {x['date']} | {x['category']} | {x['amount']:.2f} | {x['description']}")
    print(f"Total: {sum(x['amount'] for x in items):.2f}")
def main():
    items = load()
    while True:
        print("\nEXPENSE TRACKER\n1 Add expense\n2 View expenses\n3 Delete expense\n4 Export CSV\n5 Export JSON\n6 Exit")
        c = input("Choose: ").strip()
        if c == "1":
            try: amount = round(float(input("Amount: ")), 2); assert amount > 0
            except (ValueError, AssertionError): print("Enter a positive amount."); continue
            items.append({"id": max([x["id"] for x in items], default=0)+1, "date": input(f"Date [{date.today()}]: ").strip() or date.today().isoformat(), "category": input("Category: ").strip() or "Other", "description": input("Description: ").strip() or "No description", "amount": amount})
            save(items); print("Expense saved.")
        elif c == "2": show(items)
        elif c == "3":
            show(items)
            try: wanted = int(input("ID to delete: "))
            except ValueError: print("Invalid ID."); continue
            new = [x for x in items if x["id"] != wanted]
            if len(new) == len(items): print("ID not found.")
            else: items = new; save(items); print("Deleted.")
        elif c in ("4", "5"):
            ext = "csv" if c == "4" else "json"; name = input(f"Filename [expenses_export.{ext}]: ").strip() or f"expenses_export.{ext}"
            if not name.lower().endswith("."+ext): name += "."+ext
            if ext == "csv":
                with open(name, "w", newline="", encoding="utf-8") as f: w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(items)
            else: Path(name).write_text(json.dumps(items, indent=2), encoding="utf-8")
            print("Exported to", Path(name).resolve())
        elif c == "6": break
        else: print("Choose 1-6.")
if __name__ == "__main__": main()
