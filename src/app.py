import streamlit as st
import json
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.dataframe_explorer import dataframe_explorer
import os

# Configure page
st.set_page_config(
    page_title="Supermarket Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        color: white;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# File paths
PRODUCTS_FILE = 'data/products.json'
SALES_FILE = 'data/sales.json'

def init_files():
    """Initialize data files if they don't exist"""
    # Create data directory first
    os.makedirs(os.path.dirname(PRODUCTS_FILE), exist_ok=True)
    
    for file in [PRODUCTS_FILE, SALES_FILE]:
        try:
            with open(file, 'x') as f:
                json.dump([], f)
        except FileExistsError:
            pass

def load_data(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# ======================
# Custom Components
# ======================
def sidebar_menu():
    with st.sidebar:
        st.markdown("# 🛒 Supermarket Pro")
        st.markdown("---")
        
        menu_items = {
            "📦 Products": "products",
            "📈 Stock": "stock",
            "💰 Sales": "sales",
            "📊 Analytics": "analytics"
        }
        
        for item, key in menu_items.items():
            if st.button(item, use_container_width=True, key=key):
                st.session_state.current_page = key
        
        st.markdown("---")
        st.caption("v1.0 | Built with ❤️ by Rabby Md Golam")

# ======================
# Main Pages
# ======================
def products_page():
    st.header("📦 Product Management")
    
    with st.expander("➕ Add New Product", expanded=True):
        with st.form("add_product", clear_on_submit=True):
            cols = st.columns([1, 3])
            product_id = cols[0].text_input("Product ID*", help="Unique product identifier")
            product_name = cols[1].text_input("Product Name*")
            
            cols = st.columns(2)
            price = cols[0].number_input("Price*", min_value=0.0, step=0.1, format="%.2f")
            stock = cols[1].number_input("Initial Stock*", min_value=0, step=1)
            
            if st.form_submit_button("🚀 Add Product", use_container_width=True):
                if not all([product_id, product_name]):
                    st.error("Please fill all required fields!")
                else:
                    products = load_data(PRODUCTS_FILE)
                    if any(p['id'] == product_id for p in products):
                        st.error("Product ID already exists!")
                    else:
                        products.append({
                            'id': product_id,
                            'name': product_name,
                            'price': price,
                            'stock': stock
                        })
                        save_data(PRODUCTS_FILE, products)
                        st.success("Product added successfully!", icon="✅")

    st.subheader("Product Inventory")
    products = load_data(PRODUCTS_FILE)
    if products:
        filtered_df = dataframe_explorer(products, case=False)
        st.dataframe(
            filtered_df,
            column_config={
                "id": "Product ID",
                "name": "Product Name",
                "price": st.column_config.NumberColumn("Price", format="$%.2f"),
                "stock": "Current Stock"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No products found in inventory", icon="ℹ️")

def stock_page():
    st.header("📈 Stock Management")
    
    products = load_data(PRODUCTS_FILE)
    if not products:
        st.warning("No products available!", icon="⚠️")
        return
    
    selected_product = st.selectbox(
        "Select Product*",
        options=products,
        format_func=lambda x: f"{x['id']} - {x['name']}",
        placeholder="Search products...",
        index=None
    )
    
    if selected_product:
        cols = st.columns([2, 1, 1])
        cols[0].metric("Current Stock", selected_product['stock'])
        action = cols[1].radio(
            "Operation*",
            ["➕ Add Stock", "🔄 Set Stock"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if action == "➕ Add Stock":
            delta = cols[2].number_input(
                "Adjustment Amount*",
                min_value=-1000,
                max_value=1000,
                value=0,
                step=1
            )
            new_stock = selected_product['stock'] + delta
        else:
            new_stock = cols[2].number_input(
                "New Stock Quantity*",
                min_value=0,
                value=selected_product['stock'],
                step=1
            )
        
        if st.button("💾 Update Stock", use_container_width=True):
            if new_stock < 0:
                st.error("Stock cannot be negative!", icon="🚨")
            else:
                products = load_data(PRODUCTS_FILE)
                index = next(i for i, p in enumerate(products) if p['id'] == selected_product['id'])
                products[index]['stock'] = new_stock
                save_data(PRODUCTS_FILE, products)
                st.success(f"Stock updated to {new_stock}", icon="✅")

def sales_page():
    st.header("💰 Sales Management")
    
    products = load_data(PRODUCTS_FILE)
    if not products:
        st.warning("No products available for sale!", icon="⚠️")
        return
    
    cols = st.columns([3, 2])
    selected_product = cols[0].selectbox(
        "Select Product*",
        options=products,
        format_func=lambda x: f"{x['id']} - {x['name']}",
        placeholder="Search products..."
    )
    
    if selected_product:
        cols[1].metric("Available Stock", selected_product['stock'])
        quantity = cols[1].number_input(
            "Quantity to Sell*",
            min_value=1,
            max_value=selected_product['stock'],
            value=1,
            step=1
        )
        
        if st.button("💸 Record Sale", use_container_width=True, type="primary"):
            products = load_data(PRODUCTS_FILE)
            index = next(i for i, p in enumerate(products) if p['id'] == selected_product['id'])
            products[index]['stock'] -= quantity
            
            sale = {
                "product_id": selected_product['id'],
                "product_name": selected_product['name'],
                "quantity": quantity,
                "total": selected_product['price'] * quantity,
                "timestamp": datetime.now().isoformat()
            }
            
            save_data(PRODUCTS_FILE, products)
            sales = load_data(SALES_FILE)
            sales.append(sale)
            save_data(SALES_FILE, sales)
            st.success(f"Sale recorded: ${sale['total']:.2f}", icon="✅")

def analytics_page():
    st.header("📊 Business Analytics")
    
    tab1, tab2 = st.tabs(["📦 Inventory Analytics", "💰 Sales Analytics"])
    
    with tab1:
        products = load_data(PRODUCTS_FILE)
        if products:
            st.subheader("Inventory Overview")
            total_stock = sum(p['stock'] for p in products)
            total_value = sum(p['stock'] * p['price'] for p in products)
            
            cols = st.columns(2)
            cols[0].metric("Total Products", len(products))
            cols[1].metric("Total Inventory Value", f"${total_value:,.2f}")
            
            st.altair_chart(create_inventory_chart(products), use_container_width=True)
        else:
            st.info("No inventory data available", icon="ℹ️")
    
    with tab2:
        sales = load_data(SALES_FILE)
        if sales:
            total_sales = sum(s['total'] for s in sales)
            avg_sale = total_sales / len(sales)
            
            cols = st.columns(3)
            cols[0].metric("Total Sales", f"${total_sales:,.2f}")
            cols[1].metric("Total Transactions", len(sales))
            cols[2].metric("Average Sale Value", f"${avg_sale:,.2f}")
            
            st.altair_chart(create_sales_chart(sales), use_container_width=True)
        else:
            st.info("No sales records found", icon="ℹ️")
    
    style_metric_cards(border_left_color="#2c3e50")

def create_inventory_chart(products):
    import altair as alt
    data = [{"name": p['name'], "stock": p['stock']} for p in products]
    return alt.Chart(alt.Data(values=data)).mark_bar().encode(
        x='name:N',
        y='stock:Q',
        color=alt.Color('name:N', legend=None)
    ).properties(height=400)

def create_sales_chart(sales):
    import altair as alt
    from datetime import datetime
    data = [{
        "date": datetime.fromisoformat(s['timestamp']).strftime("%Y-%m-%d"),
        "total": s['total']
    } for s in sales]
    
    return alt.Chart(alt.Data(values=data)).mark_line().encode(
        x='date:T',
        y='total:Q'
    ).properties(height=400)

# ======================
# Main App Logic
# ======================
def main():
    init_files()
    
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "products"
    
    # Render sidebar
    sidebar_menu()
    
    # Show current page
    pages = {
        "products": products_page,
        "stock": stock_page,
        "sales": sales_page,
        "analytics": analytics_page
    }
    pages[st.session_state.current_page]()

if __name__ == "__main__":
    main()