import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
from datetime import datetime, timedelta, timezone
from src.services.user_service import UserService
from src.services.auction_service import AuctionService
from src.services.bid_service import BidService
from src.services.payment_service import PaymentService
from src.services.reporting_service import ReportingService

# Initialize all backend services
us = UserService()
asvc = AuctionService()
bsvc = BidService()
psvc = PaymentService()
rsvc = ReportingService()

# --- Alias mapping dictionary ---
id_map = {}

def resolve_id(value: str) -> str:
    """Converts alias like U1 or A1 to actual UUID"""
    return id_map.get(value, value)


# --- Streamlit Page Config ---
st.set_page_config(page_title="Silent Bid Network", page_icon="💼", layout="wide")

# --- Custom Page Header ---
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>💼 The Silent Bid Network</h1>
<h4 style='text-align: center; color: gray;'>A Secure, Transparent, and Fun Bidding Platform</h4>
<hr style="border: 1px solid #ddd;">
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📋 Navigation Menu")
menu = st.sidebar.radio(
    "Choose an option:",
    [
        "🏠 Home",
        "👤 Register User",
        "🛒 Create Auction",
        "📜 List Open Auctions",
        "💰 Place Sealed Bid",
        "🔓 Reveal Bid",
        "🏆 Declare Winner",
        "💳 Record Payment",
        "📈 Auction Report"
    ]
)

# --- Home Page ---
if menu == "🏠 Home":
    st.markdown("""
    ### 👋 Welcome to The Silent Bid Network
    This platform simulates a **sealed-bid auction system** where:
    - Users register to participate.
    - Auctions are created with reserve prices and durations.
    - Participants submit **sealed bids** (hidden amounts).
    - After the auction ends, bids are revealed.
    - The system declares a winner automatically.
    - Payments and reports can be generated instantly.
    """)
    st.info("Start by registering a user from the sidebar ➡️")

# --- Register User ---
elif menu == "👤 Register User":
    st.header("👤 Register a New User")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        email = st.text_input("Email Address")

    if st.button("✅ Register User"):
        try:
            user = us.register(name, email)
            alias = f"U{len([k for k in id_map if k.startswith('U')]) + 1}"
            id_map[alias] = user["id"]
            st.success(f"User Registered Successfully!\n\n**Alias:** {alias}\n**UUID:** {user['id']}")
        except Exception as e:
            st.error(f"Registration Failed: {e}")

# --- Create Auction ---
elif menu == "🛒 Create Auction":
    st.header("🛒 Create a New Auction")
    title = st.text_input("Auction Title")
    desc = st.text_area("Description")
    reserve = st.number_input("Reserve Price (₹)", min_value=1.0)
    start_in = st.number_input("Start In (Minutes from now)", min_value=0)
    duration = st.number_input("Duration (Minutes)", min_value=1)
    creator = st.text_input("Creator (UUID or Alias)")

    if st.button("🚀 Launch Auction"):
        try:
            creator_id = resolve_id(creator)
            start = datetime.now(timezone.utc) + timedelta(minutes=start_in)
            end = start + timedelta(minutes=duration)
            auction = asvc.create(title, desc, reserve, start, end, creator_id)

            alias = f"A{len([k for k in id_map if k.startswith('A')]) + 1}"
            id_map[alias] = auction["id"]

            st.success(f"Auction Created Successfully!\n\n**Alias:** {alias}\n**UUID:** {auction['id']}")
        except Exception as e:
            st.error(f"Error Creating Auction: {e}")

# --- List Open Auctions ---
elif menu == "📜 List Open Auctions":
    st.header("📜 Active Auctions")
    try:
        auctions = asvc.list_open()
        if not auctions:
            st.info("No auctions are open currently.")
        else:
            for a in auctions:
                with st.expander(f"🔹 {a['title']}"):
                    st.write(f"🆔 **Auction ID:** {a['id']}")
                    st.write(f"📄 **Description:** {a['description']}")
                    st.write(f"💰 **Reserve Price:** ₹{a['reserve_price']}")
                    st.write(f"⏰ **Ends At:** {a['end_time']}")
    except Exception as e:
        st.error(f"Error Fetching Auctions: {e}")

# --- Place Bid ---
elif menu == "💰 Place Sealed Bid":
    st.header("💰 Place Your Sealed Bid")
    col1, col2 = st.columns(2)
    with col1:
        auction_id = st.text_input("Auction ID or Alias")
    with col2:
        bidder_id = st.text_input("Bidder ID or Alias")

    commitment = st.text_input("Commitment String (any text)")
    if st.button("📨 Submit Bid"):
        try:
            auction_id = resolve_id(auction_id)
            bidder_id = resolve_id(bidder_id)
            bid = bsvc.place_sealed(auction_id, bidder_id, commitment)
            alias = f"B{len([k for k in id_map if k.startswith('B')]) + 1}"
            id_map[alias] = bid["id"]
            st.success(f"Bid Submitted!\n\n**Alias:** {alias}\n**Bid UUID:** {bid['id']}")
        except Exception as e:
            st.error(f"Error Placing Bid: {e}")

# --- Reveal Bid ---
elif menu == "🔓 Reveal Bid":
    st.header("🔓 Reveal Your Bid Amount")
    bid_id = st.text_input("Bid ID or Alias")
    amount = st.number_input("Enter Bid Amount (₹)", min_value=1.0)
    if st.button("🔍 Reveal"):
        try:
            bid_id = resolve_id(bid_id)
            result = bsvc.reveal(bid_id, amount)
            st.success(f"Bid Revealed Successfully!\n\n{result}")
        except Exception as e:
            st.error(f"Error Revealing Bid: {e}")

# --- Declare Winner ---
elif menu == "🏆 Declare Winner":
    st.header("🏆 Declare Auction Winner")
    auction_id = st.text_input("Auction ID or Alias")
    if st.button("🎯 Declare"):
        try:
            auction_id = resolve_id(auction_id)
            winner = bsvc.declare_winner(auction_id)
            if winner:
                st.success(f"Winner Declared!\n\n{winner}")
            else:
                st.warning("No winner — either no bids or reserve not met.")
        except Exception as e:
            st.error(f"Error Declaring Winner: {e}")

# --- Record Payment ---
elif menu == "💳 Record Payment":
    st.header("💳 Record Payment for Winning Bid")
    auction_id = st.text_input("Auction ID or Alias")
    bid_id = st.text_input("Winning Bid ID or Alias")
    payer_id = st.text_input("Payer User ID or Alias")
    amount = st.number_input("Payment Amount (₹)", min_value=1.0)

    if st.button("💾 Record Payment"):
        try:
            auction_id = resolve_id(auction_id)
            bid_id = resolve_id(bid_id)
            payer_id = resolve_id(payer_id)
            pay = psvc.record(auction_id, bid_id, payer_id, amount)
            st.success(f"Payment Recorded Successfully!\n\n{pay}")
        except Exception as e:
            st.error(f"Error Recording Payment: {e}")

# --- Auction Report ---
elif menu == "📈 Auction Report":
    st.header("📊 Auction Summary Report")
    auction_id = st.text_input("Auction ID or Alias")
    if st.button("📄 Generate Report"):
        try:
            auction_id = resolve_id(auction_id)
            report = rsvc.summary(auction_id)
            st.json(report)
        except Exception as e:
            st.error(f"Error Generating Report: {e}")
