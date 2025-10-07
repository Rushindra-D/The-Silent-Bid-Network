# app.py
import streamlit as st
from datetime import datetime, timedelta

from src.services.user_service import UserService
from src.services.auction_service import AuctionService
from src.services.bid_service import BidService
from src.services.payment_service import PaymentService
from src.services.reporting_service import ReportingService

# Initialize services
user_service = UserService()
auction_service = AuctionService()
bid_service = BidService()
payment_service = PaymentService()
report_service = ReportingService()

# Streamlit page setup
st.set_page_config(page_title="Silent Bid Network", layout="wide")

st.title("💰 Silent Bid Network")
st.markdown("Manage Auctions, Bids, and Winners in real time.")

menu = st.sidebar.radio("Navigate", [
    "🏠 Home", 
    "👤 Register User", 
    "📦 Create Auction", 
    "📋 View Auctions", 
    "💸 Place Bid",
    "🔓 Reveal Bid",
    "🏆 Declare Winner",
    "📊 Reports"
])

# -------------------------------
# 1. Register User
# -------------------------------
if menu == "👤 Register User":
    st.subheader("Register New User")
    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Register"):
        try:
            user = user_service.register(name, email)
            st.success(f"User registered: {user}")
        except Exception as e:
            st.error(str(e))

# -------------------------------
# 2. Create Auction
# -------------------------------
elif menu == "📦 Create Auction":
    st.subheader("Create New Auction")
    title = st.text_input("Auction Title")
    desc = st.text_area("Description")
    reserve = st.number_input("Reserve Price", min_value=0.0, step=0.1)
    duration = st.number_input("Duration (minutes)", min_value=1, value=5)
    creator_id = st.text_input("Creator User UUID")

    if st.button("Create Auction"):
        try:
            start_time = datetime.utcnow()
            end_time = start_time + timedelta(minutes=duration)
            auction = auction_service.create_auction(title, desc, reserve, start_time, end_time, creator_id)
            st.success(f"Auction created: {auction}")
        except Exception as e:
            st.error(str(e))

# -------------------------------
# 3. View Auctions
# -------------------------------
elif menu == "📋 View Auctions":
    st.subheader("Open Auctions")
    try:
        auctions = auction_service.list_open_auctions()
        if not auctions:
            st.warning("No open auctions.")
        else:
            for a in auctions:
                st.write(f"### {a['title']}")
                st.write(f"Reserve: {a['reserve_price']}, Ends: {a['end_time']}")
    except Exception as e:
        st.error(str(e))

# -------------------------------
# 4. Place Sealed Bid
# -------------------------------
elif menu == "💸 Place Bid":
    st.subheader("Place Sealed Bid")
    auction_id = st.text_input("Auction ID")
    bidder_id = st.text_input("Bidder ID")
    commitment = st.text_input("Commitment (secret hash)")

    if st.button("Place Bid"):
        try:
            bid = bid_service.place_sealed(auction_id, bidder_id, commitment)
            st.success(f"Bid placed: {bid}")
        except Exception as e:
            st.error(str(e))

# -------------------------------
# 5. Reveal Bid
# -------------------------------
elif menu == "🔓 Reveal Bid":
    st.subheader("Reveal Your Bid")
    bid_id = st.text_input("Bid ID")
    amount = st.number_input("Reveal Amount", min_value=0.0, step=0.1)

    if st.button("Reveal Bid"):
        try:
            result = bid_service.reveal(bid_id, amount)
            st.success(f"Bid revealed: {result}")
        except Exception as e:
            st.error(str(e))

# -------------------------------
# 6. Declare Winner
# -------------------------------
elif menu == "🏆 Declare Winner":
    st.subheader("Declare Winner")
    auction_id = st.text_input("Auction ID")

    if st.button("Declare"):
        try:
            result = bid_service.declare_winner(auction_id)
            st.success(f"Winner declared: {result}")
        except Exception as e:
            st.error(str(e))

# -------------------------------
# 7. Reports
# -------------------------------
elif menu == "📊 Reports":
    st.subheader("Auction Reports")
    try:
        reports = report_service.generate_report()
        st.json(reports)
    except Exception as e:
        st.error(str(e))

# -------------------------------
# 8. Home
# -------------------------------
else:
    st.markdown("""
    ### Welcome to Silent Bid Network 🎯  
    Use the sidebar to manage auctions, place bids, and declare winners.  
    Backend powered by Supabase, frontend by Streamlit.
    """)
