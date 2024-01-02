from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import db
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# DATABASE_USER = 'patrick' # Username the database was created with
# DATABASE_PASSWORD = 'patrick' # Password for the database
# DATABASE_CONNECT_STRING = 'localhost:1521/XEPDB1' # Using home computer to host and the Oracle SQL database

DATABASE_USER = 'trading' # Username for MySQL
DATABASE_PASSWORD = 'csc496' # Password for MySQL
DATABASE_HOST = 'cscmysql.lemoyne.edu' # MySQL Host
DATABASE_NAME = 'csc496_23' # Database name in MySQL
DATABASE_PORT = 3306 # Default MySQL Port

#Connent to the database
#db_connection = oracledb.connect(user = DATABASE_USER, password = DATABASE_PASSWORD, dsn = DATABASE_CONNECT_STRING)
db_connection = mysql.connector.connect(host = DATABASE_HOST, user = DATABASE_USER, password = DATABASE_PASSWORD, database = DATABASE_NAME, port = DATABASE_PORT)

app = Flask(__name__)

app.secret_key = "secret_key" #super secret key to encrypt the information

#API link
API_ENDPOINT = "https://api.pokemontcg.io/v2/cards/"

#Allows users to register for the website
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username') #grabs the username entered
        password = request.form.get('password') #grabs the password entered
        
        #Checks to see if the user already is registered
        user = db.db_get_user_count(db_connection, username)
        print (user)
        if user > 0:
            flash('Username has already been used. Please choose another name.')
            return redirect(url_for('register'))
                        
        #hashes the users entered password with sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        #Enters the users name, and password into the database
        db.db_create_user(db_connection, username, hashed_password)             

        flash('Registration was successful! You can now login.')
        return redirect(url_for('login'))
    #Bring the user back to register page
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Gets the username typed in
        username = request.form.get('username')
        #Gets the password
        password = request.form.get('password')
        
        #Gets the information from the database to check the users information
        user = db.db_get_user(db_connection, username)
        
        #checks if the information is correct then logs the user in and starts a session
        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            session['userid'] = user[0]
            flash('Login was successful!')
            return redirect(url_for('index'))
                
        #let user know something was wrong
        else:
            flash('Invalid credentials.', 'danger')
            
    #Bring user to the home page
    return render_template('login.html')

@app.route('/index')
def index():
    if 'userid' in session:
        user_id = session['userid']
        #grabs the users cards they have stored in their collection
        card_ids = db.db_get_collection(db_connection, user_id)
            
        
        # Fetch card details from the API for each card ID
        cards = []
        for card_tuple in card_ids:
            card_id = card_tuple[0]  # Extract the card ID from the tuple
            collection_id = card_tuple[1] #extract the collection id
            #make an API call to get all the card information
            api_response = requests.get(f"{API_ENDPOINT}{card_id}")
            if api_response.status_code == 200:
                data = api_response.json()["data"]

                # Check for normal and holofoil prices
                prices = data.get("tcgplayer", {}).get("prices", {})
                market_value = prices.get("normal", {}).get("market")
                if market_value is None:
                    market_value = prices.get("holofoil", {}).get("market", "N/A")

                #Info being displayed
                card_info = {
                    "collection_id":collection_id,
                    "api_id": card_id,
                    "name": data["name"],
                    "rarity": data["rarity"],
                    "market_value": market_value,
                    "image_url": data["images"]["large"]
                }
                cards.append(card_info)
        #brings up the home page with the users collection
        return render_template('index.html', cards=cards, card_ids=card_ids)
    else:
        return redirect(url_for('login'))

@app.route('/wishlist')
def wishlist():
    if 'userid' in session:
        user_id = session['userid']
        #grabs the cards from the users wishlist
        wishlist_card_ids = db.db_get_wishlist_card_ids(db_connection, user_id)

        #displays the users cards they want
        cards = []
        for card_tuple in wishlist_card_ids:
            card_id = card_tuple[0] #extract the card_id
            wl_id = card_tuple[1] #extract the wl_id
            #makes an API call to grab the card info
            api_response = requests.get(f"{API_ENDPOINT}{card_id}")
            if api_response.status_code == 200:
                data = api_response.json()["data"]

                # Check for normal and holofoil prices from tcg player
                prices = data.get("tcgplayer", {}).get("prices", {})
                market_value = prices.get("normal", {}).get("market")
                if market_value is None:
                    market_value = prices.get("holofoil", {}).get("market", "N/A")

                #display the info
                card_info = {
                    "wl_id":wl_id,
                    "api_id": card_id,
                    "name": data["name"],
                    "rarity": data["rarity"],
                    "market_value": market_value,
                    "image_url": data["images"]["large"]
                }
                cards.append(card_info)

        return render_template('wishlist.html', cards=cards)
    else:
        return redirect(url_for('login'))

@app.route('/trade_binder')
def trade_binder():
    if 'userid' in session:
        user_id = session['userid']
        card_ids = db.db_get_trade_binder_ids(db_connection, user_id)

        # Fetch card details from the API for each card ID
        cards = []
        for card_tuple in card_ids:
            card_id = card_tuple[0]  # Extract the card ID from the tuple
            collection_id = card_tuple[1] #extract the collection id
            #make the API call for card info
            api_response = requests.get(f"{API_ENDPOINT}{card_id}")
            if api_response.status_code == 200:
                data = api_response.json()["data"]

                # Check for normal and holofoil prices
                prices = data.get("tcgplayer", {}).get("prices", {})
                market_value = prices.get("normal", {}).get("market")
                if market_value is None:
                    market_value = prices.get("holofoil", {}).get("market", "N/A")

                #display the info
                card_info = {
                    "collection_id":collection_id,
                    "api_id": card_id,
                    "name": data["name"],
                    "rarity": data["rarity"],
                    "market_value": market_value,
                    "image_url": data["images"]["large"]
                }
                cards.append(card_info)

        return render_template('trade_binder.html', cards=cards)
    else:
        return redirect(url_for('login'))

@app.route('/search', methods=['GET'])
def search():
    series_options = ['swsh']  # list of series
    set_options = ['7']  # list of sets
    card_number_options = [str(i) for i in range(1, 238)]  # list of card numbers
    return render_template('search.html', series_options=series_options, 
                           set_number_options=set_options, card_number_options=card_number_options)

@app.route('/search_card', methods=['POST'])
def search_card():
    #gets Card information the user picked
    series = request.form.get('series')
    set_number = request.form.get('set')
    card_number = request.form.get('card_number')
    #creates the card id to be entered into the api
    card_id = f"{series}{set_number}-{card_number}"
    #send the user to the results page with the card they wanted to see
    return redirect(url_for('results', card_id=card_id))

@app.route('/results', methods=['GET'])
def results():
    if 'userid' in session:
        user_id = session['userid']
        
    #just in case the user makes it here without selecting a card
    card_id = request.args.get('card_id')             
    if not card_id:
        return "No card specified.", 400

    #sents the info to the api to get the card info
    api_endpoint = f"https://api.pokemontcg.io/v2/cards/{card_id}"
    response = requests.get(api_endpoint)
    data = response.json()

    #No card was found
    if 'data' not in data:
        return "No card found.", 404

    #Gets the information from the API dictionary
    card_data = data["data"]
    image_url = data["data"]["images"]["large"]
    card_name = card_data.get("name", "Unknown Card")
    return render_template('results.html', image_url=image_url, card_id=card_id, user_id=user_id, card_name=card_name)

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    #gets the info from the card selected
    card_id = request.form.get('card_id')
    user_id = session.get('userid') 
    card_name = request.form.get('card_name')

    # Logic to add the card to the user's wishlist
    db.db_add_to_wishlist(db_connection, user_id, card_id, card_name)

    # Redirect to a confirmation page or back to the results
    return redirect(url_for('wishlist'))

@app.route('/remove_from_collection', methods=['POST'])
def remove_from_collection():
    user_id = session.get('userid')
    collection_id = request.form.get('card_id')
    card_id = db.db_get_card_id(db_connection, collection_id)
    
    # Check if the card is part of any pending trade offers
    if db.db_is_card_in_pending_trade(db_connection, user_id, card_id):
        flash("Cannot remove the card. It is part of a pending trade offer.", "warning")
        return redirect(url_for('index'))
    
    # Logic to remove the card from the user's collection
    db.db_remove_card_from_collection(db_connection, user_id, collection_id)

    return redirect(url_for('index'))

@app.route('/remove_from_trade_binder', methods=['POST'])
def remove_from_trade_binder():
    user_id = session.get('userid')
    collection_id = request.form.get('card_id')
    card_id = db.db_get_card_id(db_connection, collection_id)
    
    # Check if the card is part of any pending trade offers
    if db.db_is_card_in_pending_trade(db_connection, user_id, card_id):
        flash("Cannot remove the card. It is part of a pending trade offer.", "warning")
        return redirect(url_for('trade_binder'))
    
    # Logic to remove the card from the user's trade binder
    db.db_update_trade_binder(db_connection, user_id, collection_id)

    flash("Card removed from trade binder.", "success")
    return redirect(url_for('trade_binder'))  # Redirect back to the trade binder page

@app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    user_id = session.get('userid')
    wl_id = request.form.get('wl_id')

    # Logic to remove the card from the wishlist
    db.db_remove_card_from_wishlist(db_connection, user_id, wl_id)

    return redirect(url_for('wishlist'))  # Redirect back to the wishlist page

@app.route('/add_to_collection', methods=['POST'])
def add_to_collection():
    #Gets user information from the form
    card_id = request.form.get('card_id')
    user_id = request.form.get('user_id')
    card_name = request.form.get('card_name')
    
    # Logic to add the card to the user's collection
    db.db_add_to_collection(db_connection, user_id, card_id, card_name)
    
    # After adding the card to the collection, redirect to a confirmation page or back to search
    return redirect(url_for('index'))
    
@app.route('/add_to_trade_binder', methods=['POST'])
def add_to_trade_binder():
    user_id = session.get('userid')
    card_id = request.form.get('card_id')

    # Update the trade binder status in database
    db.db_add_to_trade_binder(db_connection, user_id, card_id)

    flash("Card added to trade binder.")
    return redirect(url_for('index'))

@app.route('/initiate_trade')
def initiate_trade():
    user_id = session.get('userid')

    #gets the cards the user is interested in
    wishlist_cards = db.db_get_wishlist_cards(db_connection, user_id)

    return render_template('initiate_trade.html', wishlist_cards=wishlist_cards)

@app.route('/select_trade_target', methods=['POST'])
def select_trade_target():
    user_id = session.get('userid')
    wishlist_card_id = request.form['wishlist_card']
    card_id = request.form['wishlist_card']
    
    #gets the card name that was stored to be passed on
    wishlist_card_name = db.db_get_card_name_wishlist(db_connection, wishlist_card_id)
    #gets the users that have this card in their trade binder
    available_users = db.db_get_users_with_card_for_trade(db_connection, card_id)

    #Gets the cards the user can offer to trade for the requested card
    user_trade_binder = db.db_get_trade_binder_cards(db_connection, user_id)

    return render_template('select_trade_target.html', current_user_id=user_id, available_users=available_users, user_trade_binder=user_trade_binder, wishlist_card_id=wishlist_card_id, wishlist_card_name=wishlist_card_name)

@app.route('/finalize_trade_offer', methods=['POST'])
def finalize_trade_offer():
    offer_user_id = session.get('userid')
    target_user_id = request.form['target_user']
    offered_card_id = request.form['offered_card']
    requested_card_id = request.form['wishlist_card_id']
    cash_offer = request.form['cash_offer']
    if cash_offer is '':
        cash_offer = 0
    status = 'sent' #The offer was sent to the other user
    
    #Gets the card name from the users collection
    offered_card_name = db.db_get_card_name_collection(db_connection, offered_card_id)
    #gets the card name from the wishlist
    requested_card_name = db.db_get_card_name_wishlist(db_connection, requested_card_id)
    #Creates a trade offer in the database
    db.db_create_trade_offer(db_connection, offer_user_id, target_user_id, offered_card_id, requested_card_id, cash_offer, status, offered_card_name, requested_card_name)

    return redirect(url_for('view_offers'))

@app.route('/view_offers')
def view_offers():
    user_id = session.get('userid')
    # Query for trades where the user is target_user_id
    received_offers = db.db_offers_received(db_connection,user_id) 
    # Query for trades where the user is offer_user_id
    sent_offers = db.db_offers_sent(db_connection,user_id) 
     #query for accpeted offers
    accepted_offers = db.db_offers_accepted(db_connection, user_id)
    #query for rejected offers
    rejected_offers = db.db_offers_rejected(db_connection, user_id)
     #query for canceled offers
    canceled_offers = db.db_offers_canceled(db_connection, user_id)
    
    return render_template('view_offers.html', received_offers=received_offers, sent_offers=sent_offers, rejected_offers=rejected_offers, accepted_offers=accepted_offers, canceled_offers= canceled_offers)

@app.route('/accept_offer/<int:trade_id>',methods=['POST'])
def accept_offer(trade_id):
    user_id = session.get('userid')
    
    # Fetch trade details to get the IDs of the involved cards and users
    trade_details = db.db_get_trade_details(db_connection, trade_id)
    
    if trade_details and user_id in [trade_details[1], trade_details[2]]:
        # Remove the card from the offering user's trade binder
        db.db_remove_card_from_trade_binder_after_trade(db_connection, trade_details[1], trade_details[3])

        #remove the card from the requested trade binder
        db.db_remove_card_from_trade_binder_after_trade(db_connection, trade_details[2], trade_details[4])
        
        # Remove the card from the recieving user's wishlist
        db.db_remove_card_from_wishlist_after_trade(db_connection, trade_details[1], trade_details[4])

        # Update the trade status to accepted
        db.db_update_status_accepted(db_connection,trade_id)

        flash("Trade completed successfully", "success")
    else:
        flash("Invalid trade or unauthorized access", "danger")

    return redirect(url_for('view_offers'))

@app.route('/reject_offer/<int:trade_id>', methods=['POST'])
def reject_offer(trade_id):
    #update trade status to rejected
    db.db_update_status_rejected(db_connection,trade_id)

    return redirect(url_for('view_offers'))

@app.route('/cancel_offer/<int:trade_id>', methods=['POST'])
def cancel_offer(trade_id):
    #update trade status to canceled
    db.db_update_status_canceled(db_connection,trade_id)
    return redirect(url_for('view_offers'))
    
# Logs the user out
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You were logged out.', 'success')
    return redirect(url_for('login'))

# Makes sure the flash messages are no longer are still there if a user uses the back button or revists the page again
@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)
    