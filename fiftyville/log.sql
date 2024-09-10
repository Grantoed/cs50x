-- Keep a log of any SQL queries you execute as you solve the mystery.

-- All you know is that the theft took place
-- on July 28, 2023 and that it took place on
-- Humphrey Street.
-- Find crime reports for this day and street

SELECT
  description
FROM
  crime_scene_reports
WHERE
  year = 2023
  AND month = 7
  AND day = 28
  AND street = 'Humphrey Street';

-- Theft took place at 10.15am.
-- Three witnesses were interviewed.
-- All mentioned bakery.
-- Find interviews taken on this day which mention bakery

SELECT
  *
FROM
  interviews
WHERE
  year = 2023
  AND month = 7
  AND day = 28
  AND transcript LIKE "%bakery%";

-- 1. Check license plates in bakery security footage
--    in 10 minutes timeframe of when theft happened

SELECT
  activity,
  license_plate,
  minute
FROM
  bakery_security_logs
WHERE
  year = 2023
  AND month = 7
  AND day = 28
  AND hour = 10;

-- 2. Check atm withdrawals at Leggett Street for 07/28

SELECT
  *
FROM
  atm_transactions
WHERE
  year = 2023
  AND month = 7
  AND day = 28
  AND atm_location = 'Leggett Street'
  AND transaction_type = 'withdraw';

-- 3. Check phone calls with duration of less then a mintute for 07/28.
--    The thief asked the person on the other end to purchase flight ticket
--    out of Fiftiville tomorrow.

SELECT
  *
FROM
  phone_calls
WHERE
  year = 2023
  AND month = 7
  AND day = 28
  AND duration < 60;

-- Find people who made withdrawals on Legget Street on the day of theft

SELECT
  *
FROM
  people
WHERE
  id IN (
    SELECT
      person_id
    FROM
      bank_accounts
    WHERE
      bank_accounts.account_number IN (
        SELECT
          account_number
        FROM
          atm_transactions
        WHERE
          year = 2023
          AND month = 7
          AND day = 28
          AND atm_location = 'Leggett Street'
          AND transaction_type = 'withdraw'
      )
  );

-- Find people associated with the license plates that appeared
-- in the bakery footage

SELECT
  *
FROM
  people p
  JOIN bakery_security_logs ON p.license_plate = bakery_security_logs.license_plate
WHERE
  day = 28
  AND month = 7
  AND year = 2023
  AND hour = 10
  AND minute BETWEEN 15
  AND 25;

 -- Find the names of the people who made the calls

SELECT
  people.name
FROM
  people
  JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE
  phone_calls.year = 2023
  AND phone_calls.month = 7
  AND phone_calls.day = 28
  AND phone_calls.duration <= 60;

 -- Find the id of the airport in Fiftyville

SELECT
  *
FROM
  airports
WHERE
  city = 'Fiftyville';

-- id is 8

-- Find the earlies flight on the day after the theft

SELECT
  *
FROM
  flights
WHERE
  origin_airport_id = 8
  AND flights.year = 2023
  AND flights.month = 7
  AND flights.day = 29;

 -- The earlies flight is at 8.20am

 -- Find people who were on this flight

SELECT
  people.name
FROM
  people
  JOIN passengers ON people.passport_number = passengers.passport_number
  JOIN flights ON passengers.flight_id = flights.id
  JOIN airports ON flights.origin_airport_id = airports.id
WHERE
  airports.city = 'Fiftyville'
  AND flights.year = 2023
  AND flights.month = 7
  AND flights.day = 29
  AND flights.hour = 8
  AND flights.minute = 20;

-- The person who mathces the result and appeared before is Bruce.
-- He must be our thief.

 -- Find the destination city

SELECT
  airports.city
FROM
  airports
  JOIN flights ON airports.id = flights.destination_airport_id
WHERE
  flights.origin_airport_id = 8
  AND flights.year = 2023
  AND flights.month = 7
  AND flights.day = 29
  AND flights.hour = 8
  AND flights.minute = 20;

 -- New York City

 -- What is Bruce's phone

SELECT
  phone_number
FROM
  people
WHERE
  name = 'Bruce';

 -- (367) 555-5533

 -- Find accomplice

 SELECT
  people.name
FROM
  people
  JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE
  phone_calls.year = 2023
  AND phone_calls.month = 7
  AND phone_calls.day = 28
  AND phone_calls.duration <= 60
  AND phone_calls.caller = '(367) 555-5533';

 -- Robin

 -- Did Batman become a villain???
