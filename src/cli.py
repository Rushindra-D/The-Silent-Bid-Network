# src/cli.py
from datetime import datetime, timedelta, timezone
from src.services.user_service import UserService
from src.services.auction_service import AuctionService
from src.services.bid_service import BidService
from src.services.payment_service import PaymentService
from src.services.reporting_service import ReportingService

us = UserService()
asvc = AuctionService()
bsvc = BidService()
psvc = PaymentService()
rsvc = ReportingService()

def menu():
    print("\n--- Silent Auction Menu ---")
    print("1. Register user")
    print("2. Create auction")
    print("3. List open auctions")
    print("4. Place bid (sealed)")
    print("5. Reveal bid")
    print("6. Declare winner")
    print("7. Record payment")
    print("8. Auction report")
    print("9. Exit")

def run_menu():
    while True:
        menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            user = us.register(name, email)
            print("Registered:", user)

        elif choice == "2":
            title = input("Auction title: ").strip()
            desc = input("Description: ").strip()
            reserve = float(input("Reserve price: "))
            start_in = int(input("Start in minutes from now: "))
            duration = int(input("Duration in minutes: "))
            creator_id = input("Creator user id: ").strip()
            start = datetime.now(timezone.utc) + timedelta(minutes=start_in)
            end = start + timedelta(minutes=duration)
            auction = asvc.create(title, desc, reserve, start, end, creator_id)
            print("Auction created:", auction)

        elif choice == "3":
            auctions = asvc.list_open()
            if not auctions:
                print("No open auctions")
            else:
                for a in auctions:
                    print(f"{a['id']} | {a['title']} | Reserve={a['reserve_price']} | Ends={a['end_time']}")

        elif choice == "4":
            auction_id = input("Auction ID: ").strip()
            bidder_id = input("Bidder ID: ").strip()
            commitment = input("Commitment (any string): ").strip()
            bid = bsvc.place_sealed(auction_id, bidder_id, commitment)
            print("Bid placed (sealed):", bid)

        elif choice == "5":
            bid_id = input("Bid ID: ").strip()
            amount = float(input("Reveal amount: "))
            r = bsvc.reveal(bid_id, amount)
            print("Bid revealed:", r)

        elif choice == "6":
            auction_id = input("Auction ID: ").strip()
            winner = bsvc.declare_winner(auction_id)
            if winner:
                print("Winner:", winner)
            else:
                print("No winner (no revealed bids or reserve not met)")

        elif choice == "7":
            auction_id = input("Auction ID: ").strip()
            bid_id = input("Winning bid ID: ").strip()
            payer_id = input("Payer user ID: ").strip()
            amount = float(input("Payment amount: "))
            pay = psvc.record(auction_id, bid_id, payer_id, amount)
            print("Payment recorded:", pay)

        elif choice == "8":
            auction_id = input("Auction ID: ").strip()
            report = rsvc.summary(auction_id)
            print("Report:", report)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

def main():
    run_menu()

if __name__ == "__main__":
    main()
