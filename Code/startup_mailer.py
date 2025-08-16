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
# Loring  10/23/21  Added test for internet access to get local ip address

"""

import smtplib  # Use to send mail
from email.message import EmailMessage  # Create email message
import ssl  # Create secure context to send mail
import socket  # Create local socket to get local IP address
import datetime  # Get the current date and time
from time import sleep  # Use in loop to pause for trying connections
import platform  # Import platform module for getting hostname
import subprocess  # Access system commands for time sync

# *************************************************************************#
# Change the following email address to
# the email account that will receive email
# Add another email address to the list with a , to
# send messages to multiple accounts
EMAIL_DEST = ["Your Email Address Here", "Another Email Address Here"]

# *************************************************************************#
# Email account and App password to send email through gmail
EMAIL_FROM = "Your Email Address Here"
# Use an App Password for Gmail accounts with 2FA enabled
# Create an App Password at https://myaccount.google.com/apppasswords
APP_PASSWORD = "Your App Password Here"

# Set to True to see all communication with the SMTP server
SMTP_DEBUG = False

# *************************************************************************#
#     DO NOT CHANGE ANYTHING BELOW THIS POINT                              #
# *************************************************************************#
# Constants for connection to smtp server
SMTP_SERVER = "smtp.gmail.com"
PORT = 587


# ----------------------------- SEND MAIL --------------------------------- #
def send_mail(email_source, email_password, email_destination):
    # Test internet access and return local ip address to include in email
    local_ip_address = get_ip_address()

    # Sync system time now that internet access is confirmed
    sync_system_time()

    # Get hostname using platform module
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
            # Wait 5 seconds before we try again
            sleep(5)

    # Show all communication with the server, for testing only
    smtpserver.set_debuglevel(SMTP_DEBUG)

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
    message_content = f"{today} \n{hostname} IP address: {local_ip_address}"
    subject = f"{local_ip_address} {hostname} {today}"

    # Create Email message
    msg = EmailMessage()
    msg.set_content(message_content)
    msg["Subject"] = subject
    msg["From"] = email_source
    msg["To"] = email_destination

    try:
        # Send email message
        smtpserver.send_message(msg)
        print(f"Email sent to {email_destination} with subject: {subject}")
        # Say goodbye to the smtp server
        smtpserver.quit()
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")


# ----------------------TEST INTERNET CONNECTION -------------------------- #
def get_ip_address():
    """Get local IP Address by connecting to Google DNS server
    This step is needed if there is more than one IP address on the host
    """
    tries = 0
    while True:
        if tries > 60:
            exit()
        try:
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # IP address and port to connect to
            local_socket.connect(("8.8.8.8", 80))
            local_ip_address = local_socket.getsockname()[0]
            print(f"Local IP: {local_ip_address}")
            break
        except Exception as e:
            # Print exception for testing
            print(f"Failure getting IP: {e}")
            # Increment the number of tries
            tries = tries + 1
            # Wait 5 second before we try again
            sleep(5)
    return local_ip_address


# --------------------------SYNC SYSTEM TIME ------------------------------ #
def sync_system_time():
    """Synchronize system time using NTP after internet connection is confirmed"""
    try:
        # Update system time using timedatectl (systemd-timesyncd)
        subprocess.run(["sudo", "timedatectl", "set-ntp", "true"], check=True)
        print("NTP synchronization enabled")

        # Force immediate synchronization
        subprocess.run(
            ["sudo", "systemctl", "restart", "systemd-timesyncd"], check=True
        )
        print("Time synchronization service restarted")

        # Wait a moment for sync to complete
        sleep(3)

        # Verify sync status
        result = subprocess.run(
            ["timedatectl", "status"], capture_output=True, text=True
        )
        if "System clock synchronized: yes" in result.stdout:
            print("System time successfully synchronized")
        else:
            print("Time sync may still be in progress")

    except subprocess.CalledProcessError as e:
        print(f"Error synchronizing time: {e}")
    except Exception as e:
        print(f"Unexpected error during time sync: {e}")


def main():
    send_mail(
        EMAIL_FROM,
        APP_PASSWORD,
        EMAIL_DEST,
    )


# Call main function
if __name__ == "__main__":
    main()
