import requests
import sys

BASE_URL = "http://localhost:8006"
EMAIL = "test@example.com"
PASSWORD = "password123"


def verify():
    # 1. Register/Login
    print("1. Authenticating...")
    # Try login first
    resp = requests.post(
        f"{BASE_URL}/auth/access-token", data={"username": EMAIL, "password": PASSWORD}
    )
    if resp.status_code != 200:
        # Try register
        print("   User not found, registering...")
        resp = requests.post(
            f"{BASE_URL}/users/",
            json={
                "email": EMAIL,
                "hashed_password": PASSWORD,
                "full_name": "Test User",
                "company_name": "Test Corp",
            },
        )
        if resp.status_code != 200:
            print(f"Failed to register: {resp.text}")
            sys.exit(1)
        # Login again
        resp = requests.post(
            f"{BASE_URL}/auth/access-token",
            data={"username": EMAIL, "password": PASSWORD},
        )
        if resp.status_code != 200:
            print(f"Failed to login: {resp.text}")
            sys.exit(1)

    token = resp.json()["access_token"]  # pyright: ignore[reportAny]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Authenticated.")

    # 2. Create Invoice
    print("2. Creating Invoice...")
    invoice_data = {
        "invoice_number": "INV-001",
        "client_name": "Client A",
        "client_email": "client@example.com",
        "total_amount": 100.0,
        "content": {
            "items": [{"description": "Service A", "quantity": 1, "unit_price": 100.0}]
        },
    }
    resp = requests.post(f"{BASE_URL}/invoices/", json=invoice_data, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to create invoice: {resp.text}")
        sys.exit(1)
    invoice = resp.json()  # pyright: ignore[reportAny]
    invoice_id = invoice["id"]  # pyright: ignore[reportAny]
    print(f"   Invoice created: {invoice_id}")

    # 3. Get Invoice PDF
    print("3. Fetching PDF...")
    resp = requests.get(f"{BASE_URL}/invoices/{invoice_id}/pdf", headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get PDF: {resp.text}")
        sys.exit(1)

    if resp.headers["content-type"] != "application/pdf":
        print(f"Wrong content type: {resp.headers['content-type']}")
        sys.exit(1)

    if len(resp.content) < 100:  # detailed check
        print("PDF seems too small")
        sys.exit(1)

    print("   PDF fetched successfully.")
    print("Verification Passed!")


if __name__ == "__main__":
    verify()
