from langchain_core.tools import tool
from db.database import SessionLocal, Order

@tool
def get_order_details(order_id: str) -> str:
    """
    Fetches the details of a customer's order by Order ID.
    Always use this tool first to gather facts before making a refund decision.
    """
    db = SessionLocal()
    clean_order_id = order_id.strip().upper()
    try:
        order = db.query(Order).filter(Order.order_id == clean_order_id).first()
        
        if order:
            final_sale_str = "Yes" if order.is_final_sale else "No"
            return (f"Customer: {order.customer.name} | Item: {order.item_name} | "
                    f"Category: {order.category} | Purchase Date: {order.purchase_date} | "
                    f"Final Sale: {final_sale_str} | Status: {order.status}")
        else:
            return f"Order {order_id} not found in the database."
    except Exception as e:
        return f"Database error: {str(e)}"
    finally:
        db.close()

@tool
def process_refund(order_id: str, action: str, reason: str) -> str:
    """
    Executes the final refund decision.
    'action' must be strictly either "APPROVE" or "DENY".
    'reason' must be a short explanation based on the policy.
    """
    if action == "APPROVE":
        return f"SUCCESS: Refund approved for {order_id}. Reason: {reason}"
    elif action == "DENY":
        return f"DENIED: Refund rejected for {order_id}. Reason: {reason}"
    else:
        return "ERROR: Invalid action. Must be APPROVE or DENY."

agent_tools = [get_order_details, process_refund]
