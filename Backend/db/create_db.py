from database import engine, Base, SessionLocal, Customer, Order

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    customers = [
        Customer(customer_id=1, name="Alice Smith", email="alice@example.com"),
        Customer(customer_id=2, name="Bob Johnson", email="bob@example.com"),
        Customer(customer_id=3, name="Charlie Davis", email="charlie@example.com"),
        Customer(customer_id=4, name="Diana Prince", email="diana@example.com"),
        Customer(customer_id=5, name="Evan Wright", email="evan@example.com"),
        Customer(customer_id=6, name="Fiona Gallagher", email="fiona@example.com"),
        Customer(customer_id=7, name="George Martin", email="george@example.com"),
        Customer(customer_id=8, name="Hannah Abbott", email="hannah@example.com"),
        Customer(customer_id=9, name="Ian Malcolm", email="ian@example.com"),
        Customer(customer_id=10, name="Julia Roberts", email="julia@example.com"),
        Customer(customer_id=11, name="Kevin Hart", email="kevin@example.com"),
        Customer(customer_id=12, name="Laura Dern", email="laura@example.com"),
        Customer(customer_id=13, name="Michael Scott", email="michael@example.com"),
        Customer(customer_id=14, name="Nina Simone", email="nina@example.com"),
        Customer(customer_id=15, name="Oscar Isaac", email="oscar@example.com")
    ]
    db.add_all(customers)
    db.commit()

    orders = [
        Order(order_id="ORD-001", customer_id=1, item_name="Cotton T-Shirt", category="Apparel", purchase_date="2026-06-01", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-002", customer_id=2, item_name="Running Shoes", category="Footwear", purchase_date="2026-05-28", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-003", customer_id=3, item_name="Wireless Mouse", category="Electronics", purchase_date="2026-06-10", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-004", customer_id=4, item_name="Desk Lamp", category="Home", purchase_date="2026-06-05", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-005", customer_id=5, item_name="Yoga Mat", category="Fitness", purchase_date="2026-06-12", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-006", customer_id=6, item_name="Winter Coat", category="Apparel", purchase_date="2026-04-15", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-007", customer_id=7, item_name="Bluetooth Headphones", category="Electronics", purchase_date="2026-05-20", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-008", customer_id=8, item_name="Clearance Sunglasses", category="Accessories", purchase_date="2026-06-02", is_final_sale=True, status="Delivered"),
        Order(order_id="ORD-009", customer_id=9, item_name="Gaming Monitor", category="Electronics", purchase_date="2026-04-01", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-010", customer_id=10, item_name="Mystery Box", category="Novelty", purchase_date="2026-06-14", is_final_sale=True, status="Delivered"),
        Order(order_id="ORD-011", customer_id=11, item_name="Coffee Maker", category="Home", purchase_date="2026-05-10", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-012", customer_id=12, item_name="Graphic Novel", category="Books", purchase_date="2026-06-14", is_final_sale=False, status="In Transit"),
        Order(order_id="ORD-013", customer_id=13, item_name="Discounted Watch", category="Accessories", purchase_date="2026-06-08", is_final_sale=True, status="Delivered"),
        Order(order_id="ORD-014", customer_id=14, item_name="Office Chair", category="Furniture", purchase_date="2026-06-01", is_final_sale=False, status="Delivered"),
        Order(order_id="ORD-015", customer_id=15, item_name="Mechanical Keyboard", category="Electronics", purchase_date="2026-05-01", is_final_sale=False, status="Delivered")
    ]
    db.add_all(orders)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_database()
