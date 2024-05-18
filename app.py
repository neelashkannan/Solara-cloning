import solara
import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    cred = credentials.Certificate("testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://snack-jack-e004a-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Fetch food items from Firebase
food_items_ref = db.reference('Starters')
food_items_docs = food_items_ref.get()

# Create a state for the cart
cart_items = solara.reactive([])

solara.Title("Snack Jack")

@solara.component
def Menu():
    solara.AppBarTitle("Snack Jack")
    with solara.Column():
        solara.Head("starters")
        # Iterate over the food items fetched from Firebase
        for name, price in food_items_docs.items():
            with solara.Columns([7,5,7]):
                solara.Text(name)
                solara.Text(str(price))
                # Update the cart_items state when the button is clicked
                solara.Button(icon_name="mdi-cart", on_click=lambda: cart_items.set(cart_items.get() + [(name, price)]))

@solara.component
def Cart():
    with solara.Column():
        solara.Markdown("Cart")
        # Display the items in the cart
        for item, price in cart_items.get():
            solara.Text(f"{item}: {price}")

routes = [
    solara.Route(path="/", component=Menu, label="Menu"),
    solara.Route(path="/cart", component=Cart, label="Cart"),
]
