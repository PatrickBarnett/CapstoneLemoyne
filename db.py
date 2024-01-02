import mysql.connector

#checks the databse to see if that username is already taken
def db_get_user_count(db_connection:mysql.connector, username):
    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    user_count = cur.fetchone()
    cur.close()
    return user_count[0] if user_count else 0

#adds user to the database
def db_create_user(db_connection:mysql.connector, username, hashed_password):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db_connection.commit()
    cur.close()
    
#grabs the user information from the databse
def db_get_user(db_connection:mysql.connector, username):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user

#Grab the cards from the users collection table
def db_get_collection(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_id, collection_id FROM users_collection WHERE user_id = %s", (user_id,))
    card_ids = cur.fetchall()
    cur.close()
    return card_ids

#Grab the card_id
def db_get_card_id(db_connection:mysql.connector, collection_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_id FROM users_collection WHERE collection_id = %s", (collection_id,))
    card_id = cur.fetchone()[0]
    cur.close()
    return card_id

#Add card to wishlist
def db_add_to_wishlist(db_connection:mysql.connector, user_id, card_id, card_name):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO USERS_WISHLIST(user_id, card_id, card_name) VALUES(%s, %s, %s)", (user_id, card_id, card_name))
    db_connection.commit()
    cur.close()

#Add card to collection
def db_add_to_collection(db_connection:mysql.connector, user_id, card_id, card_name):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO USERS_COLLECTION(user_id, card_id, card_name) VALUES(%s, %s, %s)", (user_id, card_id, card_name))
    db_connection.commit() 
    cur.close()

#Add card to trade binder
def db_add_to_trade_binder(db_connection:mysql.connector, user_id, card_id):
    cur = db_connection.cursor()
    cur.execute("UPDATE USERS_COLLECTION SET trade = 'Y' WHERE user_id = %s AND card_id = %s", (user_id, card_id))
    db_connection.commit()  
    cur.close()

#Get card_id in users wishlist
def db_get_wishlist_card_ids(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_id, wl_id FROM users_wishlist WHERE user_id = %s", (user_id,))
    wishlist_card_ids = cur.fetchall()
    cur.close()
    return wishlist_card_ids

#Get card_id in trade binder
def db_get_trade_binder_ids(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_id, collection_id FROM users_collection WHERE user_id = %s AND trade = 'Y'", (user_id,))
    card_ids = cur.fetchall()
    cur.close()
    return card_ids

#Get cards in users wishlist
def db_get_wishlist_cards(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_wishlist WHERE user_id = %s", (user_id,))
    wishlist_cards = cur.fetchall()
    cur.close()
    return wishlist_cards

#Get cards in trade binder
def db_get_trade_binder_cards(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_collection WHERE user_id = %s AND trade = 'Y'", (user_id,))
    user_trade_binder = cur.fetchall()
    cur.close()
    return user_trade_binder

#Find users who have card_id in their collection
def db_get_users_with_card_for_trade(db_connection:mysql.connector, card_id):
    cur = db_connection.cursor()
    cur.execute("SELECT user_id FROM users_collection WHERE card_id = %s AND trade = 'Y'", (card_id,))
    user_ids = cur.fetchall()
    cur.close()
    return user_ids

#Get the card name from the users collection
def db_get_card_name_collection(db_connection:mysql.connector, card_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_name FROM users_collection where card_id = %s", (card_id,))
    card_name = cur.fetchone()[0]
    cur.close()
    return card_name

#Get the card name from the users wishlist
def db_get_card_name_wishlist(db_connection:mysql.connector, card_id):
    cur = db_connection.cursor()
    cur.execute("SELECT card_name FROM users_wishlist where card_id = %s", (card_id,))
    card_name = cur.fetchone()[0]
    cur.close()
    return card_name

#Insert the trade information into the database
def db_create_trade_offer(db_connection:mysql.connector, offer_user_id, target_user_id, offered_card_id, requested_card_id, cash_offer, status, offered_card_name, requested_card_name):
    cur =db_connection.cursor()
    cur.execute("INSERT INTO users_trades(offer_user_id, target_user_id, offered_card_id, requested_card_id, cash_offer, status, offered_card_name, requested_card_name)"
                + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (offer_user_id, target_user_id, offered_card_id, requested_card_id, cash_offer, status, offered_card_name, requested_card_name))
    db_connection.commit()
    cur.close()

#Checks to see what offers the user has recieved
def db_offers_received(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE target_user_id = %s AND status = 'sent'", (user_id,))
    received_offers = cur.fetchall()
    cur.close()
    return received_offers

#Checks to see that offers the user has sent
def db_offers_sent(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE offer_user_id = %s AND status = 'sent'", (user_id,))
    sent_offers = cur.fetchall()
    cur.close()
    return sent_offers

#Checks to see that offers the user has accepted
def db_offers_accepted(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE (offer_user_id = %s OR target_user_id = %s) AND status = 'accepted'", (user_id, user_id))
    sent_offers = cur.fetchall()
    cur.close()
    return sent_offers

#Checks to see that offers the user has rejected
def db_offers_rejected(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE (offer_user_id = %s OR target_user_id = %s) AND status = 'rejected'", (user_id,user_id))
    sent_offers = cur.fetchall()
    cur.close()
    return sent_offers
 
 #Checks to see that offers the user has canceled
def db_offers_canceled(db_connection:mysql.connector, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE (offer_user_id = %s OR target_user_id = %s) AND status = 'canceled'", (user_id,user_id))
    canceled_offers = cur.fetchall()
    cur.close()
    return canceled_offers

#Update status in trades to accepted
def db_update_status_accepted(db_connection:mysql.connector, trade_id):
    cur = db_connection.cursor()
    cur.execute("UPDATE users_trades SET status = 'accepted' where trade_id = %s", (trade_id,))
    db_connection.commit()
    cur.close()

#Update status in trades to rejected
def db_update_status_rejected(db_connection:mysql.connector, trade_id):
    cur = db_connection.cursor()
    cur.execute("UPDATE users_trades SET status = 'rejected' where trade_id = %s", (trade_id,))
    db_connection.commit()
    cur.close()

#Update status in trades to canceled
def db_update_status_canceled(db_connection:mysql.connector, trade_id):
    cur = db_connection.cursor()
    cur.execute("UPDATE users_trades SET status = 'canceled' where trade_id = %s", (trade_id,))
    db_connection.commit()
    cur.close()

#remove a card from the users collecion
def db_remove_card_from_collection(db_connection:mysql.connector, user_id, collection_id):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM users_collection WHERE user_id = %s AND collection_id = %s", 
                (user_id, collection_id))
    db_connection.commit()
    cur.close()

#update card from trade binder
def db_update_trade_binder(db_connection:mysql.connector, user_id, collection_id):
    cur = db_connection.cursor()
    cur.execute("UPDATE USERS_COLLECTION SET trade = '' WHERE user_id = %s AND collection_id = %s", (user_id, collection_id))
    db_connection.commit()  
    cur.close()

#Remove card from trade binder
def db_remove_card_from_trade_binder_after_trade(db_connection:mysql.connector, user_id, card_id):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM USERS_COLLECTION WHERE user_id = %s AND card_id = %s", (user_id, card_id))
    db_connection.commit()  
    cur.close()

#remove a card from the users wishlist
def db_remove_card_from_wishlist(db_connection:mysql.connector, user_id, wl_id):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM users_wishlist WHERE user_id = %s AND wl_id = %s", (user_id, wl_id))
    db_connection.commit()
    cur.close()

#remove a card from the users wishlist after trade
def db_remove_card_from_wishlist_after_trade(db_connection:mysql.connector, user_id, card_id):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM users_wishlist WHERE user_id = %s AND card_id = %s", (user_id, card_id))
    db_connection.commit()
    cur.close()

#checks to see if the card is in the process of a trade  
def db_is_card_in_pending_trade(db_connection:mysql.connector, user_id, card_id):
    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users_trades WHERE offer_user_id = %s AND offered_card_id = %s AND status = 'sent'", (user_id, card_id))
    count = cur.fetchone()[0]
    cur.close()
    return count

#Gets the information about the trade
def db_get_trade_details(db_connection:mysql.connector, trade_id):
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM users_trades WHERE trade_id = %s", (trade_id,))
    trade_details = cur.fetchone()
    cur.close()
    return trade_details