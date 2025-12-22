-- bookings count

SELECT COUNT(*) FROM bookings
WHERE hotel_name = 'Hotel Name'
AND check_in_date >= '2025-01-01';

-- occupancy rate

Occupancy Rate = (Total Occupied Nights / Total Available Room-Nights) × 100

Where:
- Total Occupied Nights = SUM(total_nights) for the period
- Total Available Room-Nights = Number of Rooms × Number of Days

-- total revenue

SELECT SUM(total_price) FROM bookings 
WHERE hotel_name = 'Hotel Name' 
AND check_in_date BETWEEN '2025-01-01' AND '2025-01-31';

-- RevPAR calculation

RevPAR = Total Revenue / Total Available Room-Nights