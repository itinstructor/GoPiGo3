#!/usr/bin/env python3
"""
    Name: startup_mailer.py
    Author: William Loring
    Created: 09/06/21
    Purpose: Email the IP address of the Raspberry Pi
# ------------------------------------------------
# History
# ------------------------------------------------
# Author  Date      Comments
# Loring  10/23/21  Added test for internet access to get local IP address

"""

import smtplib  # Use to send mail
from email.message import EmailMessage  # Create email message
import ssl  # Create secure context to send mail
import datetime  # Get the current date and time
from time import sleep  # Use in loop to pause for trying connections
import requests  # Import requests to make HTTP requests
import platform  # Import platform to get the hostname

# *************************************************************************#
# Change the following email address to
# the email account that will receive email
# Add another email address to the list to
# send messages to multiple accounts
EMAIL_DEST = ["Your email"]

# *************************************************************************#
# Email account and password used to send email
EMAIL_FROM = "you@gmail.com"
EMAIL_PASSWORD = "app password"

# *************************************************************************#
#     DO NOT CHANGE ANYTHING BELOW THIS POINT                              #
# *************************************************************************#
# Constants for connection to smtp server
SMTP_SERVER = "smtp.gmail.com"
PORT = 587


# ----------------------------- SEND MAIL ---------------------------------- #
def send_mail(email_source, email_password, email_destination):
    # Test internet access and return local ip address
    local_ip_address = get_ip_address()
    hostname = platform.node()
    # Track how many times we tried to send email
    tries = 0
    # Loop until we connect with the SMTP server
    while True:
        # After 60 tries, exit
        if tries > 60:
            exit()
        try:
            # Connect to SMTP server
            smtpserver = smtplib.SMTP(SMTP_SERVER, PORT, timeout=30)
            break
        except Exception as e:
            print(e)
            # Increment the number of tries
            tries = tries + 1
            # Wait 5 second before we try again
            sleep(5)

    # Show all communication with the server, for testing only
    # smtpserver.set_debuglevel(True)

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Say hello to the smtp server
    smtpserver.ehlo()
    smtpserver.starttls(context=context)
    smtpserver.ehlo
    # Logon to the smtp server
    smtpserver.login(email_source, email_password)

    # Get current time and date
    today = datetime.datetime.now()
    # Format current time and date
    today = today.strftime("%I:%M %p %x")

    # Email message
    message_content = f"{today}\n{hostname} IP address: {local_ip_address}"
    subject = f"{local_ip_address} {hostname} {today}"

    # Create Email message
    msg = EmailMessage()
    msg.set_content(message_content)
    msg["Subject"] = subject
    msg["From"] = email_source
    msg["To"] = email_destination

    # Send email message
    smtpserver.send_message(msg)
    # Say goodbye to the smtp server
    smtpserver.quit()


# ----------------------TEST INTERNET CONNECTION --------------------------- #
def get_ip_address():
    """Get public IP Address by querying an external service."""
    tries = 0
    while True:
        if tries > 60:
            exit()
        try:
            # Make a request to an external service to get the public IP
            response = requests.get(
                "https://api.ipify.org?format=json", timeout=10
            )
            # Raise an error for HTTP issues
            response.raise_for_status()  
            local_ip_address = response.json()["ip"]
            break
        except Exception as e:
            print(e)  # Print exception for debugging
            tries += 1
            sleep(5)  # Wait 5 seconds before retrying
    return local_ip_address


def main():
    send_mail(
        EMAIL_FROM,
        EMAIL_PASSWORD,
        EMAIL_DEST,
    )


# Call main function
if __name__ == "__main__":
    main()
