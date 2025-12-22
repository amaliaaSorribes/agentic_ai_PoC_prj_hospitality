import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

QA_PATH_EXTERNAL = PROJECT_ROOT / "ai_agents_hospitality-api" / "agents"

sys.path.insert(0, str(QA_PATH_EXTERNAL))

from bookings_sql_agent import execute_and_format_sql_query, db

bookings_count = '''SELECT COUNT(*) FROM bookings
WHERE hotel_name = 'Obsidian Tower'
AND check_in_date >= '2025-01-01';'''

total_revenue = '''SELECT SUM(total_price) FROM bookings
WHERE hotel_name = 'Obsidian Tower' 
AND check_in_date BETWEEN '2025-01-01' AND '2025-01-31';'''

print("Hotel Analytics Queries Results:\n")
print("1. Bookings Count for Obsidian Tower in 2025:\n")
execute_and_format_sql_query(db, bookings_count)
print("2. Total Revenue for Obsidian Tower in January 2025:\n")
total_nights = execute_and_format_sql_query(db, total_revenue)

number_of_rooms = 50  # ejemplo
number_of_days = 31   # enero
total_occupied_nights = float(total_nights.strip("[]()Decimal,''"))

occupancy_rate = (total_occupied_nights / (number_of_rooms * number_of_days)) * 100
rounded_occupancy_rate = round(occupancy_rate, 2)
print(f"3. Occupancy Rate for Obsidian Tower in January 2025\n\n Result: {rounded_occupancy_rate}%\n")
print("-"*40+"\n")

total_available_rooms = number_of_rooms * number_of_days
revpar = total_occupied_nights / total_available_rooms
rounded_revpar = round(revpar, 2)
print(f"4. RevPAR for Obsidian Tower in January 2025\n\n Result: {rounded_revpar}\n")