# - Customers, Food,  Collection, Transaction
"""ByteBites domain models.

Implements in-memory domain classes for the ByteBites tinker activity:
- `Customer`, `Food`, `Collection`, `Transaction`.

Assumptions:
- In-memory models (no persistence layer).
- `id` fields are optional ints (can be None until persisted).
- `price` uses `Decimal` for currency accuracy.
- `createdAt` is a UTC-aware datetime set at creation.
- `isVerified()` is a simple rule: non-empty name and >=1 purchase.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
import datetime
from typing import List, Optional


def _to_decimal(value) -> Decimal:
	if isinstance(value, Decimal):
		return value
	try:
		# convert float/int/str to Decimal safely via str
		return Decimal(str(value))
	except Exception:
		raise ValueError("Invalid monetary value")


@dataclass
class Food:
	id: Optional[int] = None
	name: str = ""
	price: Decimal = Decimal("0.00")
	category: str = ""
	popularity: int = 0

	def __post_init__(self) -> None:
		self.price = _to_decimal(self.price)
		if self.price < 0:
			raise ValueError("price must be non-negative")
		if not isinstance(self.popularity, int):
			try:
				self.popularity = int(self.popularity)
			except Exception:
				raise ValueError("popularity must be an integer")

	def updatePopularity(self, delta: int) -> None:
		"""Adjust popularity by `delta`. Popularity is clamped at 0."""
		if not isinstance(delta, int):
			raise ValueError("delta must be an int")
		self.popularity = max(0, self.popularity + delta)


@dataclass
class Transaction:
	id: Optional[int] = None
	customer: Optional[Customer] = None
	items: List[Food] = field(default_factory=list)
	createdAt: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

	def addItem(self, f: Food) -> None:
		if not isinstance(f, Food):
			raise ValueError("addItem expects a Food instance")
		self.items.append(f)

	def removeItem(self, foodId: int) -> bool:
		"""Remove the first item with matching `id`. Returns True if removed."""
		for i, item in enumerate(self.items):
			if item.id == foodId:
				del self.items[i]
				return True
		return False

	def total(self) -> Decimal:
		"""Return total cost as a Decimal (sum of item prices)."""
		total = Decimal("0.00")
		for item in self.items:
			total += item.price
		return total


@dataclass
class Customer:
	id: Optional[int] = None
	name: str = ""
	purchaseHistory: List[Transaction] = field(default_factory=list)

	def addPurchase(self, tx: Transaction) -> None:
		if not isinstance(tx, Transaction):
			raise ValueError("addPurchase expects a Transaction instance")
		self.purchaseHistory.append(tx)

	def isVerified(self) -> bool:
		"""Default verification rule: non-empty name and at least one past purchase."""
		return bool(self.name and len(self.purchaseHistory) >= 1)


@dataclass
class Collection:
	items: List[Food] = field(default_factory=list)

	def addItem(self, f: Food) -> None:
		if not isinstance(f, Food):
			raise ValueError("addItem expects a Food instance")
		self.items.append(f)

	def removeItem(self, foodId: int) -> bool:
		for i, item in enumerate(self.items):
			if item.id == foodId:
				del self.items[i]
				return True
		return False

	def filterByCategory(self, cat: str) -> List[Food]:
		return [f for f in self.items if (f.category or "").lower() == (cat or "").lower()]

	def findByName(self, name: str) -> Optional[Food]:
		name_lower = (name or "").lower()
		for f in self.items:
			if f.name and f.name.lower() == name_lower:
				return f
		return None


# TODO: add repository / persistence layer and unit tests.

if __name__ == "__main__":
	# Example usage
    food1 = Food(id=1, name="Burger", price="5.99", category="Main")
    food2 = Food(id=2, name="Fries", price="2.49", category="Sides")
    collection = Collection(items=[food1, food2])
    customer = Customer(id=1, name="Alice")
    tx = Transaction(customer=customer)
    tx.addItem(food1)
    tx.addItem(food2)
    customer.addPurchase(tx)

    print(f"Customer: {customer.name}, Verified: {customer.isVerified()}")
    print(f"Transaction items: {[item.name for item in tx.items]}")
    print(f"Transaction total: ${tx.total():.2f}")
