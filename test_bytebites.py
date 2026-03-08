from decimal import Decimal

import models


def test_order_totals():
	# two items sum correctly
	f1 = models.Food(id=1, name="Spicy Burger", price=5.50, category="Entree")
	f2 = models.Food(id=2, name="Large Soda", price=1.25, category="Drinks")

	tx = models.Transaction()
	tx.addItem(f1)
	tx.addItem(f2)

	assert tx.total() == Decimal("6.75")


def test_empty_totals():
	tx = models.Transaction()
	assert tx.total() == Decimal("0.00")


def test_filter_by_category():
	c = models.Collection()
	a = models.Food(id=1, name="Cola", price=1.00, category="Drinks")
	b = models.Food(id=2, name="Iced Tea", price=1.50, category="drinks")
	d = models.Food(id=3, name="Cake", price=3.00, category="Desserts")

	c.addItem(a)
	c.addItem(b)
	c.addItem(d)

	drinks = c.filterByCategory("Drinks")
	# both drink items should be returned (case-insensitive match)
	assert len(drinks) == 2
	names = {f.name for f in drinks}
	assert names == {"Cola", "Iced Tea"}


