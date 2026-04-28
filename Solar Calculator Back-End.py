import json
import sys
from typing import Any, Tuple, List

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from urllib.parse import urlparse, parse_qs, ParseResult

HOSTNAME: str = "localhost"
HOSTPORT: int = 69

data: dict[str, Any] = dict()

DEFAULT_DATA_SAVE_POINT: str = "./server_data.json"

HOUSE_TYPE_RESIDENTIAL: int = 0
HOUSE_TYPE_COMMERCIAL: int = 1

TIME_AT_HOME_ALL_DAY: int = 0
TIME_AT_HOME_HALF_DAY: int = 1

SOLAR_BATTERY_YES: int = 0
SOLAR_BATTERY_NO: int = 1

def save_data() -> None:
    save_data_json: str = json.dumps(data)
    try:
        with open(DEFAULT_DATA_SAVE_POINT) as outfile:
            outfile.write(save_data_json)
    except OSError as e:
        print(f"ERROR: Failed to write save file to disk : {e}")
        print(f"If you care about the save file, copy the following data, otherwise press ENTER...:\n{save_data_json}")
        sys.stdin.read(1)
        sys.exit(1)

def load_data() -> None:
    global data
    try:
        with open(DEFAULT_DATA_SAVE_POINT) as infile:
            save_data_in: str = infile.read()
            data = json.loads(save_data_in)
    except OSError as e:
        print(f"ERROR: Failed to read in save file : {e}")
        print("Press ENTER to continue")
        sys.stdin.read(1)
        sys.exit(1)

DOCTYPE_HTML: str = "text/html"
DOCTYPE_JS: str = "application/javascript"
DOCTYPE_JSON: str = "application/json"

# The variable to help facilitate easy serving of files
files: dict[str, str] = {
    "/": "./index.html",
    "/index/html": "./index.html",
    "/html/login.html": "/html/login.html",
}

curr_path: str = ""

def resolve_path(path: str) -> Tuple[str, str]:
    doctype: str = ""
    if path.endswith(".html"):
        doctype = DOCTYPE_HTML
    elif path.endswith(".js"):
        doctype = DOCTYPE_JS
    return (files[path], doctype)

# I'm lazy. So everything is a GET request, no matter the purpose
class BackendServer(BaseHTTPRequestHandler):
    def serve_file(self, path: str):
        resolved_path: Tuple[str, str] = resolve_path(path)
        file, content_type = resolved_path

        data: bytes = bytes()
        try:
            with open(file, "rb") as infile:
                data = infile.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except:
            self.send_response(500)

    def do_GET(self):
        global curr_path, data
        parsed_url: ParseResult = urlparse(self.path)

        if parsed_url.path != curr_path:
            curr_path = parsed_url.path
            self.serve_file(parsed_url.path)
            return

        params: dict[str, List[str]] = parse_qs(parsed_url.query)

        def get_param(name: str) -> str:
            return params.get(name, [""])[0]

        match get_param("get_type"):
            case "login":
                name: str = get_param("name")
                password: str = get_param("password")

                usernames: List[str] = [user["name"] for user in data["users"]]
                user_idx: int = usernames.index(name)

                if name not in usernames:
                    self.send_response(401)
                    self.end_headers()
                    return
                elif data["users"][user_idx]["password"] != password:
                    self.send_response(401)
                    self.end_headers()
                    return

                calculated: bool = isinstance(data["users"][user_idx].get("calculations"), dict) == False

                response_json: str = json.dumps({
                    "name": name,
                    "calculated": "yes" if calculated == True else "no"
                    });

                self.send_response(200)
                self.send_header("Content-Type", DOCTYPE_JSON)
                self.send_header("Content-Length", str(len(response_json)))
                self.end_headers()
                self.wfile.write(response_json.encode("utf-8"))
            case "signup":
                name: str = get_param("name")
                email: str = get_param("email")
                phone: str = get_param("phone")
                password: str = get_param("password")

                data["users"].append({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "password": password
                })
            case "calculate":
                postcode: str = get_param("postcode") # type: ignore
                time_at_home: int = int(get_param("time_at_home")) # type: ignore
                address: str = get_param("address") # type: ignore
                property_type: int = int(get_param("property_type")) # type: ignore
                electric_bill: int = int(get_param("electric_bill")) # type: ignore
                daily_use: int = int(get_param("daily_use")) # type: ignore
                bill_period: int = int(get_param("bill_period")) # type: ignore
                cost_per_kwh: int = int(get_param("cost_per_kwh")) # type: ignore
                solar_battery: int = int(get_param("solar_battery")) # type: ignore

                # MAGIC NUMBER 500 BECAUSE I DON'T HAVE TIME AAAAAAAAAAAAAAAAA
                # return (profits, savings, average_yearly_generation, average_yearly_earning)
                profits, savings, year_generated, year_earnings = calculate(electric_bill, bill_period, 500, int(cost_per_kwh / electric_bill))

                result_json: dict[str, Any] = {
                    "profits": profits,
                    "savings": savings,
                    "excess": year_generated,
                    "returns": year_earnings
                }

                result_json_str: str = json.dumps(result_json)

                self.send_response(200)
                self.send_header("Content-Type", DOCTYPE_JSON)
                self.send_header("Content-Length", str(len(result_json_str)))
                self.end_headers()
                self.wfile.write(result_json_str.encode("utf-8"))
            case _:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"ERR NOT FOUND")
                return

if __name__ == "__main__":
    load_data()

    web_server = HTTPServer((HOSTNAME, HOSTPORT), BackendServer)

    try:
        print(f"Web server started at http://{HOSTNAME}:{HOSTPORT} : Press CTRL+C to exit")
        web_server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down web server and saving data")
        web_server.server_close()
        save_data()
        sys.exit(0)

BILL_PERIOD_ANNUAL: int = 0
BILL_PERIOD_QUARTER: int = 1
BILL_PERIOD_MONTH: int = 2
BILL_PERIOD_WEEK: int = 3

def calculate(bill: int, period: int, size: int, generated: int) -> Tuple[float, float, float, float]:
    global BILL_PERIOD_ANNUAL, BILL_PERIOD_QUARTER, BILL_PERIOD_MONTH, BILL_PERIOD_WEEK
    days_between_payments: float = 0.0

    # Calculate Average Daily Usage
    # For some reason a match statement wouldn't work here??!
    if period == BILL_PERIOD_ANNUAL:
        days_between_payments = 365.0
    elif period == BILL_PERIOD_QUARTER:
        days_between_payments = 90.0
    elif period == BILL_PERIOD_MONTH:
        days_between_payments = 30.0
    elif period == BILL_PERIOD_WEEK:
        days_between_payments = 7.0

    actual_usage: float = bill - (1.25 * days_between_payments)
    average_usage: float = round((actual_usage / 0.28) / days_between_payments, 2)

    # Calculate Savings Impact
    average_generation: float = float(size) * float(generated)

    profits: float = 0.0
    savings: float = 0.0

    average_yearly_generation: float = 0.0
    average_yearly_earning: float = 0.0

    difference: float = 0.0

    if average_generation > average_usage:
        difference = round(average_generation - average_usage, 2)
        daily_savings: float = round(difference * 0.08, 2)
        billing_period_profit: float = daily_savings * days_between_payments
        profits = billing_period_profit + bill
    elif average_generation < average_usage:
        power_cover: float = (average_generation / average_usage) * 100.0
        bill_difference: float = (power_cover / 100.0) * bill
        savings = round(bill_difference + bill, 2)

    # calculate yearly values if Daily Generation exceeds Daily Usage
    if average_generation > average_usage:
        average_yearly_generation = round(difference * 365.0, 2)
        average_yearly_earning = average_yearly_generation * 0.08

    return (profits, savings, average_yearly_generation, average_yearly_earning)
