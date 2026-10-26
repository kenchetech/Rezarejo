import requests
import base64
import os
from typing import Dict, Any

class MPesaB2CService:
    def __init__(self):
        self.env = os.getenv("MPESA_ENV", "sandbox")
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.initiator_name = os.getenv("MPESA_INITIATOR_NAME", "RezarejoAdmin")
        self.security_credential = os.getenv("MPESA_SECURITY_CREDENTIAL", "")
        self.shortcode = os.getenv("MPESA_B2C_SHORTCODE", "600000")
        self.callback_url = os.getenv("MPESA_B2C_CALLBACK_URL", "https://api-rezarejo.pamarsonstech.co.ke/api/v1/mpesa/b2c-callback")
        self.timeout_url = os.getenv("MPESA_B2C_TIMEOUT_URL", "https://api-rezarejo.pamarsonstech.co.ke/api/v1/mpesa/b2c-timeout")
        self.base_url = "https://api.safaricom.co.ke" if self.env == "production" else "https://sandbox.safaricom.co.ke"

    def get_access_token(self) -> str:
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        response = requests.get(url, headers={"Authorization": f"Basic {encoded_auth}"}, timeout=10)
        if response.status_code == 200:
            return response.json().get("access_token")
        raise Exception(f"Daraja Auth Failed: {response.text}")

    def disburse_payment(self, phone_number: str, amount: float, remarks: str = "Rezarejo Waste Pickup", occasion: str = "WastePayout") -> Dict[str, Any]:
        formatted_phone = phone_number.replace("+", "").strip()
        if formatted_phone.startswith("0"):
            formatted_phone = "254" + formatted_phone[1:]
        access_token = self.get_access_token()
        url = f"{self.base_url}/mpesa/b2c/v3/paymentrequest"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {
            "InitiatorName": self.initiator_name,
            "SecurityCredential": self.security_credential,
            "CommandID": "BusinessPayment",
            "Amount": int(amount),
            "PartyA": self.shortcode,
            "PartyB": formatted_phone,
            "Remarks": remarks[:100],
            "QueueTimeOutURL": self.timeout_url,
            "ResultURL": self.callback_url,
            "Occasion": occasion
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code in [200, 201]:
            return response.json()
        raise Exception(f"M-Pesa B2C Failed: {response.text}")
