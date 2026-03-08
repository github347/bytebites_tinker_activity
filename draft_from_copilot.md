


classDiagram

    class Customer {
        +name: String
        +purchaseHistory: List~Transaction~
        +addTransaction(transaction: Transaction)
    }

    class Food {
        +name: String
        +price: double
        +category: String
        +popularityRating: int
    }

    class Collection {
        +items: List~Food~
        +addItem(food: Food)
        +filterByCategory(category: String): List~Food~
    }

    class Transaction {
        +selectedItems: List~Food~
        +totalCost: double
        +addItem(food: Food)
        +calculateTotal(): double
    }

    Customer --> Transaction : purchaseHistory
    Transaction --> Food : selectedItems
    Collection --> Food : items