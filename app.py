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
    with solara.Card("Starters"):
        #solara.Head("starters")
        # Iterate over the food items fetched from Firebase
        with solara.Columns([7,5,7]):
            solara.Text("Food item")
            solara.Text("Price")
            solara.Text("Add to cart")
        for name, details in food_items_docs.items():
            if details['availability']:  # Only display items that are available
                with solara.Columns([7,5,7]):
                    solara.Text(name)
                    solara.Text(str(details['price']))
                    # Update the cart_items state when the button is clicked
                    solara.Button(icon_name="mdi-cart", on_click=(lambda item_name=name, item_price=details['price']: cart_items.set(cart_items.get() + [(item_name, item_price)])))

@solara.component
def Cart():
    with solara.Card("Cart"):
        #solara.Markdown("Cart")
        # Display the items in the cart
        for item, price in cart_items.get():
            solara.Text(f"{item}: {price}")

routes = [
    solara.Route(path="/", component=Menu, label="Menu"),
    solara.Route(path="Cart", component=Cart, label="Cart"),
]
