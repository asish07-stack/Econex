from flask import Flask, render_template, request, jsonify, session, redirect

app = Flask(__name__)

# ============================================================
# FLASK SESSION KEY
# ============================================================

app.secret_key = "econex-hackathon-secret-key"


# ============================================================
# WEEKLY MENU
# ============================================================

WEEKLY_MENU = {
    "Monday": [
        "Roti",
        "White Rice",
        "Tomato Dal",
        "Potato Deep Fry",
        "Andhra Pickle",
        "Butter Milk",
        "Rice Papad",
        "Onion",
        "Lemon"
    ],

    "Tuesday": [
        "Roti",
        "White Rice",
        "Sambhar",
        "Beans Curry",
        "Meal Maker Curry",
        "Andhra Pickle",
        "Butter Milk",
        "Onion",
        "Lemon"
    ],

    "Wednesday": [
        "Roti",
        "White Rice",
        "Tindora Chutney",
        "Oil Fry Sabji",
        "Dal",
        "Curd",
        "Andhra Pickle",
        "Lemon",
        "Onion"
    ],

    "Thursday": [
        "Roti",
        "White Rice",
        "Drumstick Curry",
        "Sambhar",
        "Butter Milk",
        "Andhra Pickle",
        "Lemon",
        "Onion"
    ],

    "Friday": [
        "Roti",
        "White Rice",
        "Sambhar",
        "Tomato Chutney",
        "Chole",
        "Puri",
        "Butter Milk",
        "Andhra Pickle",
        "Lemon",
        "Onion"
    ],

    "Saturday": [
        "Roti",
        "White Rice",
        "Leafy Dal",
        "Oil Fry Sabji",
        "Cauliflower-Tomato Curry",
        "Curd",
        "Andhra Pickle",
        "Lemon",
        "Onion"
    ],

    "Sunday": [
        "Roti",
        "Veg Dum Biryani",
        "Paneer Curry / Palak Paneer",
        "Raitha",
        "Andhra Pickle",
        "Vegetable Salad"
    ]
}

# ============================================================
# CANTEEN FOOD STORAGE ESTIMATES
# ============================================================
# These are approximate prototype values for the EcoNex
# screening model.
#
# IMPORTANT:
# These values are NOT entered by the user.
# The system uses them internally to estimate the overall
# storage tolerance of the COMPLETE menu for the selected day.
# ============================================================

CANTEEN_FOOD_STORAGE_ESTIMATES = {

    # -------------------------
    # Breads / Rice
    # -------------------------

    "Roti": 5,

    "White Rice": 3,

    "Puri": 4,

    "Veg Dum Biryani": 4,

    "Rice Papad": 8,


    # -------------------------
    # Dal / Sambar / Curries
    # -------------------------

    "Tomato Dal": 4,

    "Dal": 4,

    "Leafy Dal": 4,

    "Sambhar": 4,

    "Beans Curry": 5,

    "Meal Maker Curry": 4,

    "Potato Deep Fry": 5,

    "Oil Fry Sabji": 5,

    "Drumstick Curry": 5,

    "Chole": 5,

    "Cauliflower-Tomato Curry": 5,

    "Paneer Curry / Palak Paneer": 4,


    # -------------------------
    # Chutney / Pickle / Sides
    # -------------------------

    "Tindora Chutney": 4,

    "Tomato Chutney": 4,

    "Andhra Pickle": 8,

    "Vegetable Salad": 4,

    "Onion": 6,

    "Lemon": 8,


    # -------------------------
    # Dairy
    # -------------------------

    "Butter Milk": 3,

    "Curd": 3,

    "Raitha": 3
}


# ============================================================
# CALCULATE OVERALL MENU STORAGE ESTIMATE
# ============================================================
# The system looks at EVERY food item in the selected day's
# fixed menu and calculates one overall approximate value.
#
# Example:
#
# Rice       -> 3 hours
# Dal        -> 4 hours
# Curry      -> 5 hours
#
# Overall   -> (3 + 4 + 5) / 3
#            -> 4 hours
#
# The user only enters ONE storage time.
# ============================================================

def calculate_canteen_overall_storage(menu_items):

    if not menu_items:
        return 0

    storage_values = []

    for food in menu_items:

        estimated_hours = CANTEEN_FOOD_STORAGE_ESTIMATES.get(
            food
        )

        if estimated_hours is not None:

            storage_values.append(
                estimated_hours
            )

    if not storage_values:
        return 0

    overall_storage = sum(
        storage_values
    ) / len(
        storage_values
    )

    return round(
        overall_storage,
        1
    )





# ============================================================
# DEFAULT DATA
# ============================================================

DEFAULT_STUDENTS = 1000
DEFAULT_PREPARED = 1500

DEFAULT_DISTRIBUTION = {
    "zero": 50,
    "one": 430,
    "two": 450,
    "three": 70
}

DEFAULT_REQUIRED = 1540
DEFAULT_SURPLUS = 0


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_current_data():

    students = session.get(
        "students",
        DEFAULT_STUDENTS
    )

    prepared = session.get(
        "prepared_servings",
        DEFAULT_PREPARED
    )

    distribution = session.get(
        "distribution",
        DEFAULT_DISTRIBUTION
    )

    total_required = session.get(
        "total_required",
        DEFAULT_REQUIRED
    )

    surplus = session.get(
        "surplus",
        DEFAULT_SURPLUS
    )

    selected_day = session.get(
        "selected_day",
        "Monday"
    )

    food_status = session.get(
        "food_status",
        "READY"
    )

    quality_score = session.get(
        "quality_score",
        0
    )

    quality_status = session.get(
        "quality_status",
        "NOT CHECKED"
    )

    return {
        "students": students,
        "prepared": prepared,
        "distribution": distribution,
        "total_required": total_required,
        "surplus": surplus,
        "selected_day": selected_day,
        "food_status": food_status,
        "quality_score": quality_score,
        "quality_status": quality_status
    }


# ============================================================
# CATEGORY SELECTION
# ============================================================

@app.route("/")
def home():

    return render_template("category.html")


# ============================================================
# CANTEEN HOME
# ============================================================

@app.route("/canteen")
def canteen():

    return render_template(
        "index.html",
        menu=WEEKLY_MENU
    )

# ============================================================
# RESTAURANT HOME
# ============================================================

@app.route("/restaurant")
def restaurant():

    return render_template("restaurant_home.html")

# ============================================================
# RESTAURANT - ADD SURPLUS
# ============================================================

@app.route("/restaurant/add-surplus", methods=["GET", "POST"])
def restaurant_add_surplus():

    if "restaurant_surplus" not in session:
        session["restaurant_surplus"] = []

    if request.method == "POST":

        data = request.get_json()

        food_name = data.get("food_name", "").strip()
        quantity = data.get("quantity")
        unit = data.get("unit", "KG")

        if not food_name or quantity is None:
            return jsonify({
                "success": False,
                "message": "Please enter food name and quantity."
            })

        try:
            quantity = float(quantity)
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Please enter a valid quantity."
            })

        if quantity <= 0:
            return jsonify({
                "success": False,
                "message": "Quantity must be greater than zero."
            })

        item = {
            "name": food_name,
            "quantity": quantity,
            "unit": unit
        }

        surplus_items = session["restaurant_surplus"]
        surplus_items.append(item)

        session["restaurant_surplus"] = surplus_items
        session.modified = True

        return jsonify({
            "success": True,
            "message": f"{food_name} added successfully.",
            "item": item
        })

    return render_template(
        "restaurant_add_surplus.html"
    )

# ============================================================
# RESTAURANT FOOD STORAGE ESTIMATES
# ============================================================
# These are approximate prototype values used internally by
# EcoNex to estimate the storage tolerance of restaurant
# surplus food.
#
# IMPORTANT:
# These values are NOT entered by the user.
# The user only enters the ACTUAL storage time later.
#
# The system looks at the food items currently added to
# restaurant surplus and uses these internal estimates to
# calculate ONE overall approximate storage window.
#
# These are prototype screening values and are NOT official
# food-safety limits.
# ============================================================

RESTAURANT_FOOD_STORAGE_ESTIMATES = {

    # -------------------------
    # Rice / Grain Based Foods
    # -------------------------

    "Rice": 3,

    "White Rice": 3,

    "Jeera Rice": 3,

    "Fried Rice": 3,

    "Veg Fried Rice": 3,

    "Biryani": 4,

    "Veg Biryani": 4,

    "Chicken Biryani": 4,

    "Mutton Biryani": 4,


    # -------------------------
    # Indian Breads
    # -------------------------

    "Roti": 5,

    "Chapati": 5,

    "Naan": 5,

    "Puri": 4,

    "Paratha": 5,


    # -------------------------
    # Curries / Gravies
    # -------------------------

    "Dal": 4,

    "Sambar": 4,

    "Sambhar": 4,

    "Rasam": 4,

    "Paneer Curry": 4,

    "Paneer Butter Masala": 4,

    "Butter Chicken": 4,

    "Chicken Curry": 4,

    "Mutton Curry": 4,

    "Veg Curry": 5,

    "Mixed Veg Curry": 5,

    "Chole": 5,

    "Rajma": 4,


    # -------------------------
    # Fried / Dry Items
    # -------------------------

    "Potato Fry": 5,

    "French Fries": 3,

    "Gobi Fry": 5,

    "Chicken Fry": 4,

    "Fish Fry": 4,

    "Veg Fry": 5,


    # -------------------------
    # Dairy / Milk Based Foods
    # -------------------------

    "Curd": 3,

    "Yogurt": 3,

    "Raita": 3,

    "Raitha": 3,

    "Buttermilk": 3,

    "Butter Milk": 3,

    "Milk": 3,


    # -------------------------
    # Sweets / Desserts
    # -------------------------

    "Gulab Jamun": 5,

    "Rasgulla": 5,

    "Jalebi": 6,

    "Kheer": 3,

    "Payasam": 3,

    "Ice Cream": 2,

    "Icecream": 2,


    # -------------------------
    # Salads / Fresh Items
    # -------------------------

    "Salad": 4,

    "Vegetable Salad": 4,

    "Fruit Salad": 3,

    "Onion": 6,

    "Lemon": 8,


    # -------------------------
    # Chutneys / Pickles
    # -------------------------

    "Coconut Chutney": 3,

    "Tomato Chutney": 4,

    "Mint Chutney": 4,

    "Peanut Chutney": 4,

    "Pickle": 8,

    "Andhra Pickle": 8
}


# ============================================================
# CALCULATE RESTAURANT OVERALL STORAGE ESTIMATE
# ============================================================
#
# The restaurant can contain multiple surplus items with
# different quantities.
#
# Example:
#
# Rice          20 KG
# Biryani       25 KG
# Curd          10 KG
# Gulab Jamun   40 PIECES
#
# EcoNex finds the internal storage estimate for each item
# and calculates ONE overall approximate storage window.
#
# Quantity is considered so that larger quantities have a
# greater influence on the overall estimate.
# ============================================================

def calculate_restaurant_overall_storage(surplus_items):

    if not surplus_items:
        return 0


    weighted_total = 0

    total_weight = 0


    for item in surplus_items:

        food_name = str(
            item.get(
                "name",
                ""
            )
        ).strip()


        quantity = item.get(
            "quantity",
            0
        )


        try:

            quantity = float(
                quantity
            )

        except (
            TypeError,
            ValueError
        ):

            quantity = 0


        if quantity <= 0:
            continue


        estimated_hours = (
            RESTAURANT_FOOD_STORAGE_ESTIMATES.get(
                food_name
            )
        )


        # ----------------------------------------------------
        # If an exact food name is not available in the
        # prototype database, use a conservative generic
        # estimate rather than ignoring the item completely.
        # ----------------------------------------------------

        if estimated_hours is None:

            estimated_hours = 4


        weighted_total += (
            estimated_hours *
            quantity
        )


        total_weight += quantity


    if total_weight <= 0:
        return 0


    overall_storage = (
        weighted_total /
        total_weight
    )


    return round(
        overall_storage,
        1
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    data = get_current_data()

    return render_template(
        "dashboard.html",
        menu=WEEKLY_MENU,
        **data
    )


# ============================================================
# AI DEMAND PAGE
# ============================================================

@app.route("/demand")
def demand():

    data = get_current_data()

    return render_template(
        "demand.html",
        menu=WEEKLY_MENU,
        **data
    )


# ============================================================
# AI PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # READ JSON DATA FROM DEMAND PAGE
        # ----------------------------------------------------

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "error": "No data was received by the EcoNex AI engine."
            }), 400


        # ----------------------------------------------------
        # GET VALUES
        # ----------------------------------------------------

        day = str(
            data.get("day", "Monday")
        )

        students = int(
            data.get("students", 0)
        )

        prepared = int(
            data.get("prepared_servings", 0)
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if students <= 0:

            return jsonify({
                "success": False,
                "error": "Please enter a student count greater than 0."
            }), 400


        if prepared <= 0:

            return jsonify({
                "success": False,
                "error": "Please enter available food greater than 0."
            }), 400


        if day not in WEEKLY_MENU:

            day = "Monday"


        # ====================================================
        # CLEAR OLD RESULT FIRST
        # ====================================================

        session["selected_day"] = day

        session["students"] = students

        session["prepared_servings"] = prepared

        session["distribution"] = {
            "zero": 0,
            "one": 0,
            "two": 0,
            "three": 0
        }

        session["total_required"] = 0

        session["surplus"] = 0


        # ====================================================
        # HARD FOOD AVAILABILITY CHECK
        # ====================================================
        #
        # If the number of persons is greater than the
        # available prepared meals, food cannot be
        # distributed.
        #
        # IMPORTANT:
        # The previous result is already cleared above.
        #
        # ====================================================

        if students > prepared:

            session["food_status"] = "INSUFFICIENT FOOD"

            return jsonify({

                "success": True,

                "food_status": "INSUFFICIENT FOOD",

                "clear_previous": True,

                "error": (
                    "Food cannot be distributed because "
                    "the number of persons is greater than "
                    "the available prepared meals."
                ),

                "students": students,

                "prepared": prepared,

                "zero": 0,

                "one": 0,

                "two": 0,

                "three": 0,

                "total_required": 0,

                "surplus": 0

            }), 200


        # ====================================================
        # AI CONSUMPTION TARGET
        # ====================================================
        #
        # The AI does NOT assume:
        #
        # 1 person = 1 meal
        #
        # Instead, it estimates how many people consume
        # 0, 1, 2 or 3 meals.
        #
        # The target consumption is intentionally below
        # the prepared amount so potential surplus can exist.
        #
        # ====================================================

        meals_per_student = prepared / students


        if meals_per_student >= 1.5:

            consumption_ratio = 0.88

        elif meals_per_student >= 1.2:

            consumption_ratio = 0.90

        else:

            consumption_ratio = 0.95


        target_consumption = int(
            prepared * consumption_ratio
        )


        # Never allow the target to exceed prepared food.

        target_consumption = min(
            target_consumption,
            prepared
        )


        # ====================================================
        # AI STUDENT DISTRIBUTION
        # ====================================================
        #
        # We distribute PERSONS into:
        #
        # 0 meals
        # 1 meal
        # 2 meals
        # 3 meals
        #
        # Then:
        #
        # total consumption =
        #     0-persons × 0
        #   + 1-persons × 1
        #   + 2-persons × 2
        #   + 3-persons × 3
        #
        # ====================================================


        if students >= 10:

            # Approximately 5% consume no meal.

            zero_meals = max(
                1,
                round(students * 0.05)
            )

            active_students = (
                students - zero_meals
            )


            # ------------------------------------------------
            # Make sure the target can be represented by the
            # remaining students.
            # ------------------------------------------------

            minimum_active = max(
                3,
                (target_consumption + 2) // 3
            )

            maximum_active = min(
                active_students,
                target_consumption - 3
            )


            if minimum_active <= maximum_active:

                active_students = maximum_active

                zero_meals = (
                    students - active_students
                )


            else:

                active_students = (
                    students - zero_meals
                )


            # ------------------------------------------------
            # Meals above the first meal
            # ------------------------------------------------

            extra_meals = (
                target_consumption
                - active_students
            )


            # ------------------------------------------------
            # Give approximately 15% of active students
            # a third meal where possible.
            # ------------------------------------------------

            preferred_three = max(
                1,
                round(active_students * 0.15)
            )


            max_three = (
                extra_meals // 2
            )


            three_meals = min(
                preferred_three,
                max_three
            )


            # Always try to keep a 3-meal category.

            if (
                three_meals <= 0
                and extra_meals >= 2
            ):

                three_meals = 1


            # ------------------------------------------------
            # Remaining extra meals become second meals.
            # ------------------------------------------------

            remaining_extra = (
                extra_meals
                - (three_meals * 2)
            )


            two_meals = max(
                0,
                remaining_extra
            )


            # ------------------------------------------------
            # Ensure the number of people in categories
            # never exceeds active students.
            # ------------------------------------------------

            if (
                two_meals
                + three_meals
                > active_students
            ):

                two_meals = max(
                    0,
                    active_students
                    - three_meals
                )


            one_meal = (
                active_students
                - two_meals
                - three_meals
            )


            # ------------------------------------------------
            # If there is a rounding mismatch, correct it.
            # ------------------------------------------------

            total_people = (
                zero_meals
                + one_meal
                + two_meals
                + three_meals
            )


            difference = (
                students
                - total_people
            )


            one_meal += difference


        else:

            # For very small numbers it is mathematically
            # impossible to guarantee all four categories.

            zero_meals = 0

            one_meal = students

            two_meals = 0

            three_meals = 0


        # ====================================================
        # FINAL CALCULATED CONSUMPTION
        # ====================================================

        total_required = (

            (zero_meals * 0)

            + (one_meal * 1)

            + (two_meals * 2)

            + (three_meals * 3)

        )


        # ====================================================
        # FINAL SAFETY CORRECTION
        # ====================================================
        #
        # Consumption MUST NEVER exceed prepared food.
        #
        # If it somehow does because of rounding, reduce
        # higher-meal categories.
        #
        # ====================================================

        while total_required > prepared:

            if three_meals > 1:

                three_meals -= 1

                one_meal += 1

            elif two_meals > 0:

                two_meals -= 1

                one_meal += 1

            elif one_meal > 0:

                one_meal -= 1

                zero_meals += 1

            else:

                break


            total_required = (

                (zero_meals * 0)

                + (one_meal * 1)

                + (two_meals * 2)

                + (three_meals * 3)

            )


        # ====================================================
        # FINAL PERSON COUNT CHECK
        # ====================================================

        total_people = (

            zero_meals
            + one_meal
            + two_meals
            + three_meals

        )


        if total_people != students:

            difference = (
                students
                - total_people
            )

            one_meal += difference


        # ====================================================
        # FINAL CONSUMPTION CALCULATION
        # ====================================================

        total_required = (

            (zero_meals * 0)

            + (one_meal * 1)

            + (two_meals * 2)

            + (three_meals * 3)

        )


        # ====================================================
        # ABSOLUTE SAFETY CHECK
        # ====================================================

        if total_required > prepared:

            return jsonify({

                "success": False,

                "clear_previous": True,

                "error": (
                    "The AI calculation exceeded the "
                    "available prepared food. "
                    "Please try again."
                )

            }), 500


        # ====================================================
        # SURPLUS
        # ====================================================

        surplus = (
            prepared
            - total_required
        )


        # ====================================================
        # FOOD STATUS
        # ====================================================

        if surplus > 0:

            food_status = "SURPLUS AVAILABLE"

        else:

            food_status = "FULLY UTILIZED"


        # ====================================================
        # DISTRIBUTION
        # ====================================================

        distribution = {

            "zero": zero_meals,

            "one": one_meal,

            "two": two_meals,

            "three": three_meals

        }


        # ====================================================
        # SAVE EVERYTHING
        # ====================================================

        session["selected_day"] = day

        session["students"] = students

        session["prepared_servings"] = prepared

        session["distribution"] = distribution

        session["total_required"] = total_required

        session["surplus"] = surplus

        session["food_status"] = food_status


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return jsonify({

            "success": True,

            "clear_previous": True,

            "day": day,

            "students": students,

            "prepared": prepared,

            "zero": zero_meals,

            "one": one_meal,

            "two": two_meals,

            "three": three_meals,

            "total_required": total_required,

            "surplus": surplus,

            "food_status": food_status,

            "message": (
                f"EcoNex AI estimates approximately "
                f"{total_required} meals will be consumed "
                f"by {students} persons. "
                f"{surplus} meals may remain available "
                f"for redistribution."
            )

        }), 200


    # ========================================================
    # ERROR PROTECTION
    # ========================================================

    except Exception as error:

        print(
            "PREDICT ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "clear_previous": True,

            "error": (
                "EcoNex AI could not process the request. "
                "Please check the entered values."
            )

        }), 500


# ============================================================
# SURPLUS PAGE
# ============================================================

@app.route("/surplus")
def surplus():

    data = get_current_data()

    return render_template(
        "surplus.html",
        **data
    )

# ============================================================
# RESTAURANT - SURPLUS INVENTORY
# ============================================================

@app.route("/restaurant/inventory")
def restaurant_inventory():

    items = session.get("restaurant_surplus", [])

    total_kg = 0
    total_litres = 0

    for item in items:

        unit = item.get("unit", "").upper()

        quantity = float(item.get("quantity", 0))

        if unit == "KG":
            total_kg += quantity

        elif unit == "L":
            total_litres += quantity

    return render_template(
        "restaurant_inventory.html",
        items=items,
        total_kg=total_kg,
        total_litres=total_litres
    )

# ============================================================
# RESTAURANT - FOOD QUALITY
# ============================================================

@app.route("/restaurant/quality")
def restaurant_quality():

    # --------------------------------------------------------
    # Get the currently added Restaurant surplus items.
    #
    # This is completely separate from Canteen and Caterer.
    # --------------------------------------------------------

    items = session.get(
        "restaurant_surplus",
        []
    )


    # --------------------------------------------------------
    # Calculate ONE overall approximate storage window
    # for all currently added surplus items.
    # --------------------------------------------------------

    overall_storage_estimate = (
        calculate_restaurant_overall_storage(
            items
        )
    )


    # --------------------------------------------------------
    # Get the previously entered actual storage time.
    #
    # 0 means the user has not entered a value yet.
    # --------------------------------------------------------

    storage_time = session.get(
        "restaurant_storage_time",
        0
    )


    # --------------------------------------------------------
    # Existing Restaurant quality information.
    # --------------------------------------------------------

    quality_score = session.get(
        "restaurant_quality_score",
        0
    )

    quality_status = session.get(
        "restaurant_quality_status",
        "NOT CHECKED"
    )


    return render_template(

        "restaurant_quality.html",

        items=items,

        storage_time=storage_time,

        overall_storage_estimate=(
            overall_storage_estimate
        ),

        quality_score=quality_score,

        quality_status=quality_status

    )


# ============================================================
# RESTAURANT - CHECK FOOD QUALITY
# ============================================================

@app.route(
    "/restaurant/check-quality",
    methods=["POST"]
)
def restaurant_check_quality():

    # --------------------------------------------------------
    # Read storage time entered by the user.
    # --------------------------------------------------------

    data = request.get_json(
        silent=True
    ) or {}

    storage_time = data.get(
        "storage_time"
    )


    # --------------------------------------------------------
    # Validate storage time.
    # --------------------------------------------------------

    try:

        storage_time = float(
            storage_time
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({

            "success": False,

            "message":
                "Please enter a valid storage time."

        })


    if storage_time < 0:

        return jsonify({

            "success": False,

            "message":
                "Storage time cannot be negative."

        })


    # --------------------------------------------------------
    # Get current Restaurant surplus.
    # --------------------------------------------------------

    items = session.get(
        "restaurant_surplus",
        []
    )


    # --------------------------------------------------------
    # Calculate the AI estimated storage window for
    # the COMPLETE Restaurant surplus.
    # --------------------------------------------------------

    overall_storage_estimate = (
        calculate_restaurant_overall_storage(
            items
        )
    )


    # --------------------------------------------------------
    # No surplus protection.
    #
    # Food Quality cannot calculate an AI estimate if
    # there are no Restaurant surplus items.
    # --------------------------------------------------------

    if overall_storage_estimate <= 0:

        return jsonify({

            "success": False,

            "message":
                "Please add surplus food items before checking food quality."

        })


    # ========================================================
    # CONTINUOUS STORAGE-BASED QUALITY SCORE
    # ========================================================
    #
    # Exact match with the AI estimate = 100.
    #
    # The score changes gradually instead of using large
    # fixed percentage buckets.
    #
    # IMPORTANT:
    # This is an EcoNex prototype screening score and is
    # NOT an official food-safety limit.
    # ========================================================


    if storage_time <= overall_storage_estimate:

        # ----------------------------------------------------
        # Actual storage is at or below the AI estimate.
        #
        # The score moves gradually from 80 → 100.
        #
        # Exact match:
        #
        # 4.2 / 4.2 = 100
        # ----------------------------------------------------

        storage_fraction = (
            storage_time /
            overall_storage_estimate
        )

        score = round(

            80 +
            (
                storage_fraction *
                20
            )

        )

    else:

        # ----------------------------------------------------
        # Actual storage has exceeded the AI estimate.
        #
        # Score decreases continuously according to how much
        # the estimated storage window has been exceeded.
        # ----------------------------------------------------

        excess_ratio = (

            storage_time -
            overall_storage_estimate

        ) / overall_storage_estimate


        score = round(

            100 -
            (
                excess_ratio *
                100
            )

        )


    # --------------------------------------------------------
    # Keep score inside 0–100.
    # --------------------------------------------------------

    score = max(
        0,
        min(
            score,
            100
        )
    )


    # --------------------------------------------------------
    # Determine status.
    # --------------------------------------------------------

    if score >= 80:

        status = "SAFE"

    elif score >= 60:

        status = "CHECK REQUIRED"

    else:

        status = "UNSAFE"


    # --------------------------------------------------------
    # Save Restaurant-only quality information.
    # --------------------------------------------------------

    session[
        "restaurant_storage_time"
    ] = storage_time


    session[
        "restaurant_quality_score"
    ] = score


    session[
        "restaurant_quality_status"
    ] = status


    session[
        "restaurant_overall_storage_estimate"
    ] = overall_storage_estimate


    session.modified = True


    # --------------------------------------------------------
    # Return result to Restaurant Food Quality page.
    # --------------------------------------------------------

    return jsonify({

        "success": True,

        "score": score,

        "status": status,

        "storage_time": storage_time,

        "overall_storage_estimate":
            overall_storage_estimate,

        "items": items

    })


# ============================================================
# RESTAURANT - REMOVE SURPLUS ITEM
# ============================================================

@app.route("/restaurant/remove-surplus/<int:item_index>", methods=["POST"])
def restaurant_remove_surplus(item_index):

    items = session.get("restaurant_surplus", [])

    if 0 <= item_index < len(items):

        removed_item = items.pop(item_index)

        session["restaurant_surplus"] = items
        session.modified = True

    return redirect("/restaurant/inventory")

# ============================================================
# RESTAURANT - DASHBOARD
# ============================================================

@app.route("/restaurant/dashboard")
def restaurant_dashboard():

    items = session.get("restaurant_surplus", [])

    total_kg = 0
    total_litres = 0

    for item in items:

        unit = item.get("unit", "").upper()
        quantity = float(item.get("quantity", 0))

        if unit == "KG":
            total_kg += quantity

        elif unit == "L":
            total_litres += quantity

    quantities = [
        float(item.get("quantity", 0))
        for item in items
    ]

    max_quantity = max(quantities) if quantities else 0

    return render_template(
        "restaurant_dashboard.html",
        items=items,
        total_kg=total_kg,
        total_litres=total_litres,
        max_quantity=max_quantity
    )

# ============================================================
# RESTAURANT - SMART REDISTRIBUTION
# ============================================================

@app.route("/restaurant/redistribution")
def restaurant_redistribution():

    # --------------------------------------------------------
    # GET RESTAURANT-SPECIFIC DATA
    # --------------------------------------------------------

    restaurant_items = session.get(
        "restaurant_surplus",
        []
    )

    # --------------------------------------------------------
    # GET LATEST RESTAURANT FOOD QUALITY RESULT
    # --------------------------------------------------------

    quality_score = session.get(
        "restaurant_quality_score",
        0
    )

    quality_status = session.get(
        "restaurant_quality_status",
        "NOT CHECKED"
    )

    # --------------------------------------------------------
    # ALWAYS DERIVE STATUS FROM THE LATEST SCORE
    # --------------------------------------------------------

    try:

        quality_score = float(
            quality_score
        )

    except (
        TypeError,
        ValueError
    ):

        quality_score = 0


    if quality_score > 0:

        if quality_score >= 80:

            quality_status = "SAFE"

        elif quality_score >= 60:

            quality_status = "CHECK REQUIRED"

        else:

            quality_status = "UNSAFE"

    else:

        quality_status = "NOT CHECKED"

    # --------------------------------------------------------
    # CALCULATE RESTAURANT SURPLUS
    # --------------------------------------------------------

    total_items = len(
        restaurant_items
    )

    total_kg = 0
    total_litres = 0

    for item in restaurant_items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        quantity = float(
            item.get(
                "quantity",
                0
            )
        )

        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    # --------------------------------------------------------
    # AI RECIPIENT MATCHING
    # --------------------------------------------------------
    #
    # Restaurant-specific recipient analysis.
    #
    # Factors:
    # 1. Surplus quantity
    # 2. Recipient capacity
    # 3. Distance
    # 4. Food quality
    # 5. Pickup readiness
    #
    # --------------------------------------------------------

    recipients = [

        {
            "name": "Hope Community Shelter",
            "capacity": 120,
            "distance": 2.4,
            "pickup_ready": 100
        },

        {
            "name": "City Community Kitchen",
            "capacity": 100,
            "distance": 3.1,
            "pickup_ready": 95
        },

        {
            "name": "Helping Hands NGO",
            "capacity": 80,
            "distance": 4.7,
            "pickup_ready": 90
        }

    ]

    recipient_analysis = []

    recipient_scores = []

    # --------------------------------------------------------
    # USE SOLID SURPLUS AS PRIMARY MATCHING QUANTITY
    # --------------------------------------------------------

    surplus_quantity = total_kg

    if surplus_quantity <= 0:

        surplus_quantity = total_litres

    # --------------------------------------------------------
    # CALCULATE MATCH SCORES
    # --------------------------------------------------------

    if (
        restaurant_items
        and quality_status != "UNSAFE"
    ):

        for recipient in recipients:

            capacity = recipient[
                "capacity"
            ]

            distance = recipient[
                "distance"
            ]

            pickup_ready = recipient[
                "pickup_ready"
            ]

            # -----------------------------------------------
            # QUANTITY / CAPACITY FIT
            # -----------------------------------------------

            if surplus_quantity <= 0:

                quantity_score = 0

            elif surplus_quantity <= capacity:

                quantity_score = 100

            else:

                quantity_score = max(
                    0,
                    round(
                        (
                            capacity
                            / surplus_quantity
                        ) * 100
                    )
                )

            # -----------------------------------------------
            # DISTANCE SCORE
            # -----------------------------------------------

            if distance <= 2:

                distance_score = 100

            elif distance <= 3:

                distance_score = 95

            elif distance <= 5:

                distance_score = 85

            elif distance <= 8:

                distance_score = 70

            else:

                distance_score = 50

            # -----------------------------------------------
            # QUALITY SCORE
            # -----------------------------------------------

            if quality_status == "SAFE":

                quality_factor = quality_score

            elif quality_status == "CHECK REQUIRED":

                quality_factor = min(
                    quality_score,
                    70
                )

            else:

                quality_factor = 0

            # -----------------------------------------------
            # FINAL AI MATCH
            # -----------------------------------------------

            match_score = round(

                (quantity_score * 0.35)

                + (distance_score * 0.20)

                + (quality_factor * 0.25)

                + (pickup_ready * 0.20)

            )

            match_score = max(
                0,
                min(
                    100,
                    match_score
                )
            )

            # -----------------------------------------------
            # MATCH LEVEL
            # -----------------------------------------------

            if match_score >= 85:

                match_level = "HIGH"

            elif match_score >= 70:

                match_level = "GOOD"

            else:

                match_level = "MEDIUM"

            recipient_scores.append(
                match_score
            )

            recipient_analysis.append({

                "name":
                    recipient["name"],

                "capacity":
                    capacity,

                "distance":
                    distance,

                "pickup_ready":
                    pickup_ready,

                "match_score":
                    match_score,

                "match_level":
                    match_level

            })

    # --------------------------------------------------------
    # OVERALL AI MATCH
    # --------------------------------------------------------

    if recipient_scores:

        recipient_match = round(

            sum(recipient_scores)
            / len(recipient_scores)

        )

    else:

        recipient_match = 0

    # --------------------------------------------------------
    # SORT RECIPIENTS BY AI MATCH
    # --------------------------------------------------------

    recipient_analysis.sort(

        key=lambda x:
        x["match_score"],

        reverse=True

    )

    # --------------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------------

    if recipient_analysis:

        best_match = (
            recipient_analysis[0]
        )

    else:

        best_match = {

            "name":
                "No recipient available",

            "distance":
                0,

            "match_score":
                0,

            "match_level":
                "PENDING"

        }

    # --------------------------------------------------------
    # SAVE RESTAURANT MATCH DATA
    # --------------------------------------------------------

    session[
        "restaurant_recipient_match"
    ] = recipient_match

    session[
        "restaurant_recipient_analysis"
    ] = recipient_analysis

    session.modified = True

    # --------------------------------------------------------
    # RENDER RESTAURANT REDISTRIBUTION
    # --------------------------------------------------------

    return render_template(

        "restaurant_redistribution.html",

        items=restaurant_items,

        total_items=total_items,

        total_kg=total_kg,

        total_litres=total_litres,

        quality_score=quality_score,

        quality_status=quality_status,

        recipient_match=recipient_match,

        recipient_analysis=recipient_analysis,

        best_match=best_match

    )
# ============================================================
# RESTAURANT - IMPACT ANALYTICS
# ============================================================

@app.route("/restaurant/impact")
def restaurant_impact():

    restaurant_items = session.get(
        "restaurant_surplus",
        []
    )

    restaurant_quality = session.get(
        "restaurant_quality",
        {}
    )

    recipient_match = session.get(
        "restaurant_recipient_match",
        0
    )

    recipient_analysis = session.get(
        "restaurant_recipient_analysis",
        []
    )

    quality_score = restaurant_quality.get(
        "score",
        0
    )

    quality_status = restaurant_quality.get(
        "status",
        "NOT CHECKED"
    )

    total_items = len(
        restaurant_items
    )

    total_kg = 0
    total_litres = 0
    total_pieces = 0

    for item in restaurant_items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        quantity = float(
            item.get(
                "quantity",
                0
            )
        )

        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

        elif unit == "PIECES":

            total_pieces += quantity

    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    total_pieces = round(
        total_pieces,
        1
    )

    if total_kg > 0:

        food_rescued = total_kg

    elif total_litres > 0:

        food_rescued = total_litres

    else:

        food_rescued = total_pieces

    food_rescued = round(
        food_rescued,
        1
    )

    waste_prevented = round(
        food_rescued * 0.25,
        1
    )

    co2_avoided = round(
        food_rescued * 0.39,
        1
    )

    people_served = round(
        food_rescued
    )

    impact_score = 70

    if food_rescued >= 50:

        impact_score += 10

    if food_rescued >= 100:

        impact_score += 10

    if recipient_match >= 80:

        impact_score += 10

    if quality_status == "SAFE":

        impact_score += 5

    impact_score = min(
        impact_score,
        100
    )

    if recipient_analysis:

        best_recipient = (
            recipient_analysis[0]
        )

    else:

        best_recipient = {

            "name":
                "No recipient matched",

            "match_score":
                0,

            "distance":
                0,

            "capacity":
                0,

            "pickup_ready":
                0

        }

    return render_template(

        "restaurant_impact.html",

        restaurant_items=restaurant_items,

        total_items=total_items,

        total_kg=total_kg,

        total_litres=total_litres,

        total_pieces=total_pieces,

        food_rescued=food_rescued,

        waste_prevented=waste_prevented,

        co2_avoided=co2_avoided,

        people_served=people_served,

        quality_score=quality_score,

        quality_status=quality_status,

        recipient_match=recipient_match,

        recipient_analysis=recipient_analysis,

        best_recipient=best_recipient,

        impact_score=impact_score

    )


# ============================================================
# FOOD QUALITY PAGE
# ============================================================

@app.route("/quality")
def quality():

    data = get_current_data()

    # --------------------------------------------------------
    # SELECTED CANTEEN DAY
    # --------------------------------------------------------

    selected_day = data.get(
        "selected_day",
        "Monday"
    )

    # Make sure the selected day exists
    # in the fixed weekly menu.
    if selected_day not in WEEKLY_MENU:

        selected_day = "Monday"

        # Keep the data dictionary synchronized
        data["selected_day"] = selected_day


    # --------------------------------------------------------
    # GET THE COMPLETE MENU FOR THAT DAY
    # --------------------------------------------------------

    daily_menu = WEEKLY_MENU.get(
        selected_day,
        []
    )


    # --------------------------------------------------------
    # CALCULATE OVERALL STORAGE ESTIMATE
    # --------------------------------------------------------

    overall_storage_estimate = (
        calculate_canteen_overall_storage(
            daily_menu
        )
    )


    # --------------------------------------------------------
    # PREVIOUSLY ENTERED STORAGE TIME
    # --------------------------------------------------------

    storage_time = session.get(
        "storage_time",
        0
    )


    # --------------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------------

    return render_template(

        "quality.html",

        daily_menu=daily_menu,

        overall_storage_estimate=overall_storage_estimate,

        storage_time=storage_time,

        **data
    )


# ============================================================
# FOOD QUALITY CHECK
# ============================================================

@app.route("/check-quality", methods=["POST"])
def check_quality():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "error": (
                    "No quality data was received."
                )

            }), 400


        # ----------------------------------------------------
        # GET STORAGE TIME
        # ----------------------------------------------------

        storage_time = float(
            data.get(
                "storage_time",
                0
            )
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if storage_time < 0:

            return jsonify({

                "success": False,

                "error": (
                    "Storage time cannot be negative."
                )

            }), 400


        # ----------------------------------------------------
        # GET SELECTED DAY
        # ----------------------------------------------------

        selected_day = session.get(
            "selected_day",
            "Monday"
        )

        if selected_day not in WEEKLY_MENU:

            selected_day = "Monday"


        # ----------------------------------------------------
        # GET COMPLETE MENU FOR THE DAY
        # ----------------------------------------------------

        daily_menu = WEEKLY_MENU.get(
            selected_day,
            []
        )


        # ----------------------------------------------------
        # CALCULATE OVERALL MENU STORAGE ESTIMATE
        # ----------------------------------------------------

        overall_storage_estimate = (
            calculate_canteen_overall_storage(
                daily_menu
            )
        )


        # ----------------------------------------------------
        # QUALITY SCORE
        # ----------------------------------------------------
        #
        # The score is now based ONLY on:
        #
        # 1. Actual storage time entered by the user
        # 2. Overall storage estimate calculated from
        #    the complete menu for the selected day
        #
        # Temperature and humidity are NOT used.
        # ----------------------------------------------------

        if overall_storage_estimate <= 0:

            return jsonify({

                "success": False,

                "error": (
                    "Unable to calculate the storage "
                    "profile for the selected day's menu."
                )

            }), 400


        storage_ratio = (
            storage_time /
            overall_storage_estimate
        )


                # ----------------------------------------------------
        # CONTINUOUS STORAGE-BASED QUALITY SCORE
        # ----------------------------------------------------
        #
        # The AI-estimated menu storage window represents
        # the reference point for the selected day's menu.
        #
        # Exactly matching the estimated window = 100.
        #
        # If the actual storage time is LOWER than the
        # estimate, the food remains in the safe screening
        # direction, but the score changes gradually so the
        # result reflects how closely the actual time aligns
        # with the estimated window.
        #
        # If the actual storage time EXCEEDS the estimate,
        # the score decreases more strongly.
        #
        # This is a prototype screening score and NOT an
        # official food-safety limit.
        # ----------------------------------------------------

        if storage_time <= overall_storage_estimate:

            # Lower storage time remains in the safer
            # screening direction.
            #
            # Score ranges from 80 to 100.
            #
            # Example with 5.6 hour estimate:
            #
            # 5.6 hrs -> 100
            # 4.0 hrs -> about 94
            # 2.0 hrs -> about 87
            # 0.0 hrs -> 80

            storage_fraction = (
                storage_time /
                overall_storage_estimate
            )

            score = round(
                80 +
                (
                    storage_fraction * 20
                )
            )

        else:

            # Once the actual storage time exceeds the
            # AI-estimated window, reduce the score
            # progressively according to the excess time.

            excess_ratio = (
                storage_time -
                overall_storage_estimate
            ) / overall_storage_estimate

            score = round(
                100 -
                (
                    excess_ratio * 100
                )
            )


        score = max(
            0,
            min(
                score,
                100
            )
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if score >= 80:

            status = "SAFE"

        elif score >= 60:

            status = "CHECK REQUIRED"

        else:

            status = "UNSAFE"


        # ----------------------------------------------------
        # SAVE CANTEEN QUALITY RESULT
        # ----------------------------------------------------

        session["storage_time"] = storage_time

        session["quality_score"] = score

        session["quality_status"] = status

        session["quality_day"] = selected_day

        session["overall_storage_estimate"] = (
            overall_storage_estimate
        )

        session.modified = True


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "score": score,

            "status": status,

            "storage_time": storage_time,

            "selected_day": selected_day,

            "daily_menu": daily_menu,

            "overall_storage_estimate": (
                overall_storage_estimate
            )

        }), 200


    except (TypeError, ValueError):

        return jsonify({

            "success": False,

            "error": (
                "Please enter a valid storage time."
            )

        }), 400


    except Exception as error:

        print(
            "QUALITY ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error": (
                "Unable to complete food quality analysis."
            )

        }), 500


# ============================================================
# REDISTRIBUTION
# ============================================================

@app.route("/redistribution")
def redistribution():

    data = get_current_data()

    return render_template(

        "redistribution.html",

        **data
    )


# ============================================================
# IMPACT
# ============================================================

@app.route("/impact")
def impact():

    surplus = session.get(
        "surplus",
        DEFAULT_SURPLUS
    )

    quality_score = session.get(
        "quality_score",
        0
    )

    quality_status = session.get(
        "quality_status",
        "NOT VERIFIED"
    )

    # ========================================================
    # AI RECIPIENT MATCH ANALYSIS
    # ========================================================
    #
    # EcoNex evaluates:
    #
    # 1. Surplus quantity
    # 2. Recipient capacity
    # 3. Distance from kitchen
    # 4. Food quality
    # 5. Pickup readiness
    #
    # ========================================================

    recipients = [

        {
            "name": "Hope Community Shelter",
            "capacity": 120,
            "distance": 2.4,
            "pickup_ready": 100
        },

        {
            "name": "City Community Kitchen",
            "capacity": 100,
            "distance": 3.1,
            "pickup_ready": 95
        },

        {
            "name": "Helping Hands NGO",
            "capacity": 80,
            "distance": 4.7,
            "pickup_ready": 90
        }

    ]

    recipient_scores = []

    recipient_analysis = []


    # ========================================================
    # CALCULATE MATCH FOR EACH RECIPIENT
    # ========================================================

    if surplus > 0:

        for recipient in recipients:

            capacity = recipient["capacity"]

            distance = recipient["distance"]

            pickup_ready = recipient["pickup_ready"]


            # ------------------------------------------------
            # SURPLUS / CAPACITY FIT
            # ------------------------------------------------

            if surplus <= capacity:

                quantity_score = 100

            else:

                quantity_score = max(
                    0,
                    round(
                        (capacity / surplus) * 100
                    )
                )


            # ------------------------------------------------
            # DISTANCE SCORE
            # ------------------------------------------------

            if distance <= 2:

                distance_score = 100

            elif distance <= 3:

                distance_score = 95

            elif distance <= 5:

                distance_score = 85

            elif distance <= 8:

                distance_score = 70

            else:

                distance_score = 50


            # ------------------------------------------------
            # FOOD QUALITY
            # ------------------------------------------------

            if quality_status == "SAFE":

                quality_factor = quality_score

            elif quality_status == "CHECK REQUIRED":

                quality_factor = min(
                    quality_score,
                    70
                )

            elif quality_status == "UNSAFE":

                quality_factor = 0

            else:

                quality_factor = 60


            # ------------------------------------------------
            # FINAL MATCH SCORE
            # ------------------------------------------------

            match_score = round(

                (quantity_score * 0.35)

                + (distance_score * 0.20)

                + (quality_factor * 0.25)

                + (pickup_ready * 0.20)

            )


            recipient_scores.append(
                match_score
            )


            # ------------------------------------------------
            # MATCH LEVEL
            # ------------------------------------------------

            if match_score >= 85:

                match_level = "HIGH"

            elif match_score >= 70:

                match_level = "GOOD"

            else:

                match_level = "MEDIUM"


            recipient_analysis.append({

                "name": recipient["name"],

                "capacity": capacity,

                "distance": distance,

                "match_score": match_score,

                "match_level": match_level

            })


        # ----------------------------------------------------
        # OVERALL AI RECIPIENT MATCH
        # ----------------------------------------------------

        recipient_match = round(

            sum(recipient_scores)
            / len(recipient_scores)

        )

        recipient_match = max(
            0,
            min(
                100,
                recipient_match
            )
        )

    else:

        recipient_match = 0

        recipient_analysis = []


    # ========================================================
    # CO2 AVOIDED
    # ========================================================

    co2_avoided = round(
        surplus * 0.39,
        1
    )


    # ========================================================
    # FOOD WASTE PREVENTED
    # ========================================================

    food_waste = round(
        surplus * 0.25,
        1
    )


    # ========================================================
    # IMPACT SCORE
    # ========================================================

    impact_score = 80


    if surplus >= 100:

        impact_score += 5


    if surplus >= 200:

        impact_score += 5


    impact_score = min(
        impact_score,
        100
    )


    # ========================================================
    # SEND DATA TO IMPACT PAGE
    # ========================================================

    return render_template(

        "impact.html",

        surplus=surplus,

        recipient_match=recipient_match,

        recipient_analysis=recipient_analysis,

        food_waste=food_waste,

        co2_avoided=co2_avoided,

        impact_score=impact_score

    )


# ============================================================
# CATERER HOME
# ============================================================

@app.route("/caterer")
def caterer():

    # Caterer data is intentionally isolated from
    # both Canteen and Restaurant data.
    if "caterer_event" not in session:
        session["caterer_event"] = {
            "event_name": "Wedding Reception",
            "expected_guests": 450,
            "menu_items": 18
        }

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    event = session.get("caterer_event", {})

    return render_template(
        "caterer_home.html",
        event=event,
        surplus_items=session.get("caterer_surplus", [])
    )

# ============================================================
# CATERER - EVENT DASHBOARD
# ============================================================

@app.route("/caterer/dashboard")
def caterer_dashboard():

    # --------------------------------------------------------
    # GET CATERER-SPECIFIC EVENT DATA
    # --------------------------------------------------------

    if "caterer_event" not in session:
        session["caterer_event"] = {
            "event_name": "Wedding Reception",
            "expected_guests": 450,
            "menu_items": 18
        }

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    event = session.get(
        "caterer_event",
        {}
    )

    surplus_items = session.get(
        "caterer_surplus",
        []
    )


    # --------------------------------------------------------
    # CALCULATE SURPLUS QUANTITY
    # --------------------------------------------------------

    total_kg = 0
    total_litres = 0
    total_pieces = 0

    for item in surplus_items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        quantity = float(
            item.get(
                "quantity",
                0
            )
        )

        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

        elif unit == "PIECES":

            total_pieces += quantity


    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    total_pieces = round(
        total_pieces,
        1
    )


    # --------------------------------------------------------
    # TOTAL TRACKED SURPLUS
    # --------------------------------------------------------
    #
    # KG, litres and pieces are kept separate because they
    # represent different physical units.
    #
    # --------------------------------------------------------

    total_surplus_items = len(
        surplus_items
    )


    # --------------------------------------------------------
    # EVENT SURPLUS STATUS
    # --------------------------------------------------------

    if total_surplus_items == 0:

        event_status = "EVENT READY"

        status_description = (
            "No surplus food has been registered yet."
        )

    elif total_kg >= 100:

        event_status = "HIGH SURPLUS"

        status_description = (
            "Significant surplus detected. "
            "Consider quality verification and redistribution."
        )

    elif total_kg >= 50:

        event_status = "MODERATE SURPLUS"

        status_description = (
            "Surplus is being monitored. "
            "Redistribution can be prepared."
        )

    else:

        event_status = "LOW SURPLUS"

        status_description = (
            "Surplus levels are currently manageable."
        )


    # --------------------------------------------------------
    # EVENT READINESS
    # --------------------------------------------------------

    readiness_score = 60

    if event.get(
        "expected_guests",
        0
    ) > 0:

        readiness_score += 15

    if event.get(
        "menu_items",
        0
    ) > 0:

        readiness_score += 10

    if total_surplus_items > 0:

        readiness_score += 10

    if total_surplus_items >= 3:

        readiness_score += 5

    readiness_score = min(
        readiness_score,
        100
    )


    # --------------------------------------------------------
    # SEND DATA TO DASHBOARD
    # --------------------------------------------------------

    return render_template(

        "caterer_dashboard.html",

        event=event,

        surplus_items=surplus_items,

        total_kg=total_kg,

        total_litres=total_litres,

        total_pieces=total_pieces,

        total_surplus_items=total_surplus_items,

        event_status=event_status,

        status_description=status_description,

        readiness_score=readiness_score

    )

# ============================================================
# CATERER - ADD EVENT SURPLUS
# ============================================================

@app.route("/caterer/add-surplus", methods=["GET", "POST"])
def caterer_add_surplus():

    # --------------------------------------------------------
    # INITIALIZE CATERER-ONLY SURPLUS STORAGE
    # --------------------------------------------------------

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []


    # --------------------------------------------------------
    # ADD SURPLUS ITEM
    # --------------------------------------------------------

    if request.method == "POST":

        data = request.get_json()

        food_name = data.get(
            "food_name",
            ""
        ).strip()

        quantity = data.get(
            "quantity"
        )

        unit = data.get(
            "unit",
            "KG"
        ).upper()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not food_name:

            return jsonify({
                "success": False,
                "message": "Please enter a food item."
            })


        if quantity is None:

            return jsonify({
                "success": False,
                "message": "Please enter a quantity."
            })


        try:

            quantity = float(quantity)

        except (TypeError, ValueError):

            return jsonify({
                "success": False,
                "message": "Please enter a valid quantity."
            })


        if quantity <= 0:

            return jsonify({
                "success": False,
                "message": "Quantity must be greater than zero."
            })


        # ----------------------------------------------------
        # ALLOWED UNITS
        # ----------------------------------------------------

        allowed_units = [
            "KG",
            "L",
            "PIECES"
        ]

        if unit not in allowed_units:

            unit = "KG"


        # ----------------------------------------------------
        # CREATE ITEM
        # ----------------------------------------------------

        item = {

            "name": food_name,

            "quantity": quantity,

            "unit": unit

        }


        # ----------------------------------------------------
        # SAVE ONLY TO CATERER SURPLUS
        # ----------------------------------------------------

        surplus_items = session.get(
            "caterer_surplus",
            []
        )

        surplus_items.append(item)

        session["caterer_surplus"] = surplus_items

        session.modified = True


        return jsonify({

            "success": True,

            "message":
                f"{food_name} added successfully.",

            "item": item

        })


    # --------------------------------------------------------
    # DISPLAY PAGE
    # --------------------------------------------------------

    return render_template(

        "caterer_add_surplus.html",

        surplus_items=session.get(
            "caterer_surplus",
            []
        )

    )

# ============================================================
# CATERER - SURPLUS INVENTORY
# ============================================================

@app.route("/caterer/inventory")
def caterer_inventory():

    # --------------------------------------------------------
    # CATERER-ONLY DATA
    # --------------------------------------------------------

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    items = session.get(
        "caterer_surplus",
        []
    )


    # --------------------------------------------------------
    # CALCULATE INVENTORY TOTALS
    # --------------------------------------------------------

    total_kg = 0
    total_litres = 0
    total_pieces = 0

    for item in items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        try:
            quantity = float(
                item.get(
                    "quantity",
                    0
                )
            )
        except (TypeError, ValueError):
            quantity = 0

        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

        elif unit == "PIECES":

            total_pieces += quantity


    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    total_pieces = round(
        total_pieces,
        1
    )


    # --------------------------------------------------------
    # INVENTORY STATUS
    # --------------------------------------------------------

    item_count = len(items)

    if item_count == 0:

        inventory_status = "NO SURPLUS"

        inventory_message = (
            "No event surplus has been registered yet."
        )

    elif item_count <= 3:

        inventory_status = "LOW INVENTORY"

        inventory_message = (
            "A small amount of event surplus is currently "
            "being tracked."
        )

    elif item_count <= 7:

        inventory_status = "ACTIVE INVENTORY"

        inventory_message = (
            "Multiple surplus items are being monitored "
            "for the event."
        )

    else:

        inventory_status = "HIGH INVENTORY"

        inventory_message = (
            "A large variety of surplus items is currently "
            "being tracked."
        )


    return render_template(

        "caterer_inventory.html",

        items=items,

        total_kg=total_kg,

        total_litres=total_litres,

        total_pieces=total_pieces,

        item_count=item_count,

        inventory_status=inventory_status,

        inventory_message=inventory_message

    )


# ============================================================
# CATERER - REMOVE SURPLUS ITEM
# ============================================================

@app.route(
    "/caterer/remove-surplus/<int:item_index>",
    methods=["POST"]
)
def caterer_remove_surplus(item_index):

    items = session.get(
        "caterer_surplus",
        []
    )


    if 0 <= item_index < len(items):

        items.pop(item_index)

        session["caterer_surplus"] = items

        session.modified = True


    return redirect("/caterer/inventory")

# ============================================================
# CATERER FOOD QUALITY
# ============================================================

@app.route("/caterer/quality", methods=["GET"])
def caterer_quality():

    # Caterer data is completely isolated
    # from Canteen and Restaurant data.
    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    caterer_items = session.get("caterer_surplus", [])
    caterer_quality_data = session.get("caterer_quality", {})

    return render_template(
        "caterer_quality.html",
        caterer_items=caterer_items,
        quality=caterer_quality_data
    )


@app.route("/caterer/check-quality", methods=["POST"])
def caterer_check_quality():

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    data = request.get_json()

    food_name = data.get("food_name", "").strip()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    storage_hours = data.get("storage_hours")

    if not food_name:
        return jsonify({
            "success": False,
            "message": "Please select a food item."
        })

    try:
        temperature = float(temperature)
        humidity = float(humidity)
        storage_hours = float(storage_hours)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Please enter valid values."
        })

    if storage_hours < 0:
        return jsonify({
            "success": False,
            "message": "Storage time cannot be negative."
        })

    # --------------------------------------------------------
    # ECOnex rule-based food quality screening
    # --------------------------------------------------------

    score = 100

    # Temperature assessment
    if temperature <= 5:
        temperature_score = 100
    elif temperature <= 10:
        temperature_score = 85
    elif temperature <= 20:
        temperature_score = 65
    elif temperature <= 30:
        temperature_score = 40
    else:
        temperature_score = 20

    # Humidity assessment
    if humidity <= 60:
        humidity_score = 100
    elif humidity <= 70:
        humidity_score = 85
    elif humidity <= 80:
        humidity_score = 65
    elif humidity <= 90:
        humidity_score = 40
    else:
        humidity_score = 20

    # Storage-time assessment
    if storage_hours <= 2:
        storage_score = 100
    elif storage_hours <= 4:
        storage_score = 90
    elif storage_hours <= 6:
        storage_score = 75
    elif storage_hours <= 8:
        storage_score = 55
    else:
        storage_score = 30

    # Weighted quality score
    score = round(
        (temperature_score * 0.45) +
        (humidity_score * 0.20) +
        (storage_score * 0.35)
    )

    # Final screening status
    if score >= 80:
        status = "SAFE"
        status_description = (
            "The current storage conditions are within "
            "the EcoNex screening range for redistribution."
        )
    elif score >= 60:
        status = "CHECK REQUIRED"
        status_description = (
            "Some conditions require additional verification "
            "before redistribution."
        )
    else:
        status = "UNSAFE"
        status_description = (
            "The current conditions indicate that the food "
            "should not proceed to redistribution without "
            "further safety assessment."
        )

    quality_data = {
        "food_name": food_name,
        "temperature": temperature,
        "humidity": humidity,
        "storage_hours": storage_hours,
        "temperature_score": temperature_score,
        "humidity_score": humidity_score,
        "storage_score": storage_score,
        "score": score,
        "status": status,
        "status_description": status_description
    }

    session["caterer_quality"] = quality_data
    session.modified = True

    return jsonify({
        "success": True,
        "message": "Food quality screening completed.",
        "quality": quality_data
    })

# ============================================================
# CATERER SMART REDISTRIBUTION
# ============================================================

@app.route("/caterer/redistribution")
def caterer_redistribution():

    # --------------------------------------------------------
    # Caterer-only data
    # --------------------------------------------------------

    if "caterer_surplus" not in session:
        session["caterer_surplus"] = []

    caterer_items = session.get("caterer_surplus", [])

    caterer_quality = session.get(
        "caterer_quality",
        {}
    )

    # --------------------------------------------------------
    # Calculate caterer inventory totals
    # --------------------------------------------------------

    total_kg = 0
    total_litres = 0
    total_pieces = 0

    for item in caterer_items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        try:
            quantity = float(
                item.get(
                    "quantity",
                    0
                )
            )
        except (TypeError, ValueError):
            quantity = 0

        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

        elif unit == "PIECES":

            total_pieces += quantity


    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    total_pieces = round(
        total_pieces,
        1
    )

    # --------------------------------------------------------
    # Quality information
    # --------------------------------------------------------

    quality_score = caterer_quality.get(
        "score",
        0
    )

    quality_status = caterer_quality.get(
        "status",
        "NOT CHECKED"
    )

    # --------------------------------------------------------
    # Event-specific recipient network
    # --------------------------------------------------------

    recipients = [

        {
            "name": "Hope Community Shelter",
            "capacity": 180,
            "distance": 2.4,
            "pickup_ready": 100
        },

        {
            "name": "City Community Kitchen",
            "capacity": 150,
            "distance": 3.1,
            "pickup_ready": 95
        },

        {
            "name": "Helping Hands NGO",
            "capacity": 100,
            "distance": 4.7,
            "pickup_ready": 90
        }

    ]

    recipient_analysis = []

    # --------------------------------------------------------
    # AI-style recipient compatibility calculation
    #
    # Factors:
    # 35% Capacity fit
    # 20% Distance
    # 25% Food quality
    # 20% Pickup readiness
    # --------------------------------------------------------

    for recipient in recipients:

        capacity = recipient["capacity"]

        distance = recipient["distance"]

        pickup_ready = recipient["pickup_ready"]


        # Capacity fit

        if total_pieces > 0:

            available_quantity = total_pieces

        elif total_kg > 0:

            available_quantity = total_kg

        else:

            available_quantity = total_litres


        if available_quantity <= 0:

            quantity_score = 0

        elif available_quantity <= capacity:

            quantity_score = 100

        else:

            quantity_score = max(
                0,
                round(
                    (capacity /
                     available_quantity) * 100
                )
            )


        # Distance score

        if distance <= 2:

            distance_score = 100

        elif distance <= 3:

            distance_score = 95

        elif distance <= 5:

            distance_score = 85

        elif distance <= 8:

            distance_score = 70

        else:

            distance_score = 50


        # Quality score

        if quality_status == "SAFE":

            quality_factor = quality_score

        elif quality_status == "CHECK REQUIRED":

            quality_factor = min(
                quality_score,
                70
            )

        elif quality_status == "UNSAFE":

            quality_factor = 0

        else:

            quality_factor = 60


        # Final compatibility score

        match_score = round(

            (quantity_score * 0.35) +

            (distance_score * 0.20) +

            (quality_factor * 0.25) +

            (pickup_ready * 0.20)

        )


        if match_score >= 85:

            match_level = "EXCELLENT MATCH"

        elif match_score >= 70:

            match_level = "GOOD MATCH"

        elif match_score >= 55:

            match_level = "MODERATE MATCH"

        else:

            match_level = "LOW MATCH"


        recipient_analysis.append({

            "name": recipient["name"],

            "capacity": capacity,

            "distance": distance,

            "pickup_ready": pickup_ready,

            "quantity_score": quantity_score,

            "distance_score": distance_score,

            "quality_factor": quality_factor,

            "match_score": match_score,

            "match_level": match_level

        })


    # --------------------------------------------------------
    # Sort highest compatibility first
    # --------------------------------------------------------

    recipient_analysis.sort(

        key=lambda x:
        x["match_score"],

        reverse=True

    )


    if recipient_analysis:

        best_match = recipient_analysis[0]

    else:

        best_match = {

            "name": "No recipient available",

            "match_score": 0,

            "capacity": 0,

            "distance": 0,

            "pickup_ready": 0,

            "match_level": "NO MATCH"

        }


    # --------------------------------------------------------
    # Save caterer-only matching data
    # --------------------------------------------------------

    session[
        "caterer_recipient_match"
    ] = best_match["match_score"]

    session[
        "caterer_recipient_analysis"
    ] = recipient_analysis

    session.modified = True


    return render_template(

        "caterer_redistribution.html",

        caterer_items=caterer_items,

        total_kg=total_kg,

        total_litres=total_litres,

        total_pieces=total_pieces,

        quality_score=quality_score,

        quality_status=quality_status,

        recipient_analysis=recipient_analysis,

        best_match=best_match

    )

# ============================================================
# CATERER IMPACT & ANALYTICS
# ============================================================

@app.route("/caterer/impact")
def caterer_impact():

    # --------------------------------------------------------
    # Caterer data only
    # --------------------------------------------------------

    caterer_items = session.get(
        "caterer_surplus",
        []
    )

    caterer_quality = session.get(
        "caterer_quality",
        {}
    )

    recipient_match = session.get(
        "caterer_recipient_match",
        0
    )

    recipient_analysis = session.get(
        "caterer_recipient_analysis",
        []
    )


    # --------------------------------------------------------
    # Calculate Caterer inventory totals
    # --------------------------------------------------------

    total_kg = 0
    total_litres = 0
    total_pieces = 0


    for item in caterer_items:

        unit = item.get(
            "unit",
            ""
        ).upper()

        try:

            quantity = float(
                item.get(
                    "quantity",
                    0
                )
            )

        except (TypeError, ValueError):

            quantity = 0


        if unit == "KG":

            total_kg += quantity

        elif unit == "L":

            total_litres += quantity

        elif unit == "PIECES":

            total_pieces += quantity


    total_kg = round(
        total_kg,
        1
    )

    total_litres = round(
        total_litres,
        1
    )

    total_pieces = round(
        total_pieces,
        1
    )


    # --------------------------------------------------------
    # Quality information
    # --------------------------------------------------------

    quality_score = caterer_quality.get(
        "score",
        0
    )

    quality_status = caterer_quality.get(
        "status",
        "NOT CHECKED"
    )


    # --------------------------------------------------------
    # Impact calculations
    #
    # Keep different units separate rather than pretending
    # KG, litres and pieces are directly interchangeable.
    # --------------------------------------------------------

    food_items_registered = len(
        caterer_items
    )


    # Food rescue indicator
    #
    # KG is used as the primary measurable solid-food
    # sustainability quantity.
    #

    food_rescued_kg = round(
        total_kg,
        1
    )


    # Estimated waste prevention based on the registered
    # solid-food quantity.

    waste_prevented_kg = round(
        food_rescued_kg * 0.25,
        1
    )


    # Estimated CO2e avoidance factor used by the
    # EcoNex prototype.

    co2_avoided = round(
        food_rescued_kg * 0.39,
        1
    )


    # --------------------------------------------------------
    # Event impact score
    # --------------------------------------------------------

    impact_score = 50


    if food_rescued_kg > 0:

        impact_score += 15


    if total_litres > 0:

        impact_score += 5


    if total_pieces > 0:

        impact_score += 5


    if quality_status == "SAFE":

        impact_score += 10

    elif quality_status == "CHECK REQUIRED":

        impact_score += 5


    if recipient_match >= 85:

        impact_score += 15

    elif recipient_match >= 70:

        impact_score += 10

    elif recipient_match >= 55:

        impact_score += 5


    impact_score = min(
        impact_score,
        100
    )


    # --------------------------------------------------------
    # Impact status
    # --------------------------------------------------------

    if impact_score >= 90:

        impact_level = "EXCELLENT IMPACT"

    elif impact_score >= 75:

        impact_level = "STRONG IMPACT"

    elif impact_score >= 60:

        impact_level = "POSITIVE IMPACT"

    else:

        impact_level = "DEVELOPING IMPACT"


    # --------------------------------------------------------
    # Best recipient
    # --------------------------------------------------------

    if recipient_analysis:

        best_recipient = recipient_analysis[0]

    else:

        best_recipient = {

            "name":
                "No recipient matched",

            "match_score":
                0,

            "distance":
                0,

            "capacity":
                0,

            "pickup_ready":
                0

        }


    # --------------------------------------------------------
    # Render page
    # --------------------------------------------------------

    return render_template(

        "caterer_impact.html",

        caterer_items=caterer_items,

        food_items_registered=
            food_items_registered,

        total_kg=
            total_kg,

        total_litres=
            total_litres,

        total_pieces=
            total_pieces,

        food_rescued_kg=
            food_rescued_kg,

        waste_prevented_kg=
            waste_prevented_kg,

        co2_avoided=
            co2_avoided,

        quality_score=
            quality_score,

        quality_status=
            quality_status,

        recipient_match=
            recipient_match,

        best_recipient=
            best_recipient,

        impact_score=
            impact_score,

        impact_level=
            impact_level

    )


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000
        
    )