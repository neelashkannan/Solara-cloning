import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from functools import partial
import solara

# Use a service account
if not firebase_admin._apps:
    cred = credentials.Certificate("testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://snack-jack-e004a-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Reference to food items in Firebase
food_items_ref = db.reference('Starters')

# Fetch all food items from Firebase
def fetch_food_items():
    return food_items_ref.get()

# Update the availability of a food item
def update_availability(food_item, value):
    food_items_ref.child(food_item).update({'availability': value})

# Delete a food item
def delete_food_item(food_item):
    food_items_ref.child(food_item).delete()

# Create a state for the new food item and price
new_food_item = solara.reactive("")
new_price = solara.reactive("")
availability = solara.reactive("")

solara.Title("Add Food Items")

def add_food_item():
    # Add the new food item to Firebase
    food_items_ref.update({
        new_food_item.get(): {
            'price': int(new_price.get()),
            'availability': availability.get()
        }
    })
    # Clear the input fields
    new_food_item.set("")
    new_price.set("")
    availability.set("")

@solara.component
def FoodItemsPage():
    with solara.AppBarTitle():
        solara.Text("Snack Jack")
    with solara.Column(align="stretch"):
        with solara.Card("Starters", margin=10):
            food_items_docs = food_items_ref.get()  # Fetch the food items every time the component is rendered
            with solara.Columns([7,5,7,5]):
                solara.Text("Food item")
                solara.Text("Price")
                solara.Text("Availability")
                solara.Text("Delete")
            for name, details in food_items_docs.items():
                if 'price' in details:  # Only display items that have a price
                    price = details['price']
                    item_availability = details['availability']
                    with solara.Columns([10,5,7,9]):
                        solara.Text(name)
                        solara.Text(str(details['price']))
                        solara.Switch(value=item_availability, on_value=partial(update_availability, name))
                        solara.Button(icon_name="mdi-delete", on_click=partial(delete_food_item, name))
            with solara.Row(gap="10px", justify="space-around"):
                solara.Text("Food Item")
                solara.Text("Price")
                solara.Text("Availability")
                solara.Text("Add to Menu")
            with solara.Row(gap="30px", justify="space-around"):
                solara.InputText("Enter food item name", value=new_food_item)              
                solara.InputText("Enter price", value=new_price)
                solara.Switch(label=" ", value=availability.get())
                solara.Button(icon_name="mdi-book-plus", on_click=add_food_item)

routes = [
    solara.Route(path="/", component=FoodItemsPage, label="Food Items Page"),
]
