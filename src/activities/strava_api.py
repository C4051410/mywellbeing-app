'''
IMPORTANT - This Strava integration is currently limited to one user/athlete
'''
import os
import urllib.parse
import webbrowser
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

import requests
from dotenv import load_dotenv

from activities.activity_queries import save_tokens_for_user, load_tokens_for_user

load_dotenv()

# read strava auth credentials from env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# where strava redirects user after login
REDIRECT_URI = "http://localhost:8550/callback"

# permissions that are requested from strava
SCOPES = "read,activity:read_all"

# dict to pass results between server and main
strava_result = {"token_data": None, "error": None}

def refresh_access_token(user_id, refresh_token):
    # POST request to strava to refresh expired tokens
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={"client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET, "grant_type": "refresh_token", "refresh_token": refresh_token,}, timeout=30,)

    if response.status_code == 200: # success
        new_tokens = response.json() # converts response to python dict
        save_tokens_for_user(user_id, new_tokens) # store tokens
        return new_tokens["access_token"]
    else:
        print("Failed to refresh token:", response.text)
        return None

def get_activities(access_token):
    # GET request to strava api to fetch activities
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"per_page": 10},
        timeout=30,
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get activities:", response.status_code)
        print(response.text)
        return []

def get_saved_activities(user_id):
    # load token
    token_data = load_tokens_for_user(user_id)

    if not token_data:
        return []

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    expires_at = token_data["expires_at"]

    # check if the token has expired
    if time.time() > expires_at:
        access_token = refresh_access_token(user_id, refresh_token)

    # get activities using the valid token
    return get_activities(access_token)

def format_time(seconds):
    if seconds == 0:
        return "0s"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def format_strava_activities(strava_activities):
    formatted = []

    for act in strava_activities:
        if act.get("type") == "WeightTraining":
            print(act)
    # loop through each activity
    for act in strava_activities:
        activity_type = act.get("type", "Activity")
        distance_km = act.get("distance", 0) / 1000
        moving_time = act.get("moving_time", 0)

        parsed_date = None
        start_date = act.get("start_date_local")
        if start_date:
            try:
                dt = start_date.replace("Z", "")
                parsed_date = datetime.fromisoformat(dt)
                formatted_date = parsed_date.strftime("%b %d, %H:%M")
            except Exception:
                formatted_date = "Unknown date"
        else:
            formatted_date = "Unknown date"

        if activity_type == "Ride":
            activity_type = "Cycle"
        elif activity_type == "WeightTraining":
            activity_type = "WeightLifting"

        formatted.append({
            "date": formatted_date,
            "datetime": parsed_date,
            "dist": f"{distance_km:.2f}",
            "seconds": moving_time,
            "time": format_time(moving_time),
            "type": activity_type,
            "calories": str(int(act.get("calories", 0))) if act.get("calories") else None,
            "heart_rate": str(round(act["average_heartrate"])) if act.get("average_heartrate") else None,
            "steps": f"{act['map'].get('polyline', 0):,}" if False else None,
        })

    return formatted

# handles the callback request that strava sends to the app
class StravaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # splits url to read its query parameters
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        # one time auth code from strava
        code = query.get("code", [None])[0]
        print("CALLBACK CODE:", code)

        if not code:
            strava_result["error"] = "Missing code from Strava callback"

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code")
            return

        # exchange auth code for access/refresh tokens
        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code, "grant_type": "authorization_code",},timeout=30,)

        print("TOKEN EXCHANGE STATUS:", response.status_code)
        print("TOKEN EXCHANGE BODY:", response.text)

        if response.status_code == 200: # success
            # save token data
            token_data = response.json()
            strava_result["token_data"] = token_data
            print("TOKEN DATA SET SUCCESSFULLY")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(b"Strava connected! You can close this window.")
            self.wfile.flush()
        else:
            # strava rejected the token exchange
            strava_result["error"] = response.text

            self.send_response(400) # error
            self.end_headers()
            self.wfile.write(b"Failed to connect to Strava")

def connect_strava():
    # clear previous results
    strava_result["token_data"] = None
    strava_result["error"] = None

    # build url that sends the user to strava approval page
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "approval_prompt": "auto",
        "scope": SCOPES,
    }

    auth_url = "https://www.strava.com/oauth/authorize?" + urllib.parse.urlencode(params)

    # temporary web server to catch the callback from strava
    server = HTTPServer(("localhost", 8550), StravaHandler)

    print("Opening Strava login...")
    webbrowser.open(auth_url) # opens strava login in browser

    print("Waiting for Strava callback...")
    server.handle_request()

    if strava_result["error"]:
        raise Exception(strava_result["error"])

    return strava_result["token_data"]