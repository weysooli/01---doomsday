import random


def date():
    """Generate or validate a custom input date."""

    def is_leap(year):
        # Determine if the year is a leap year
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                return False
            return True
        return False

    def generate_year_weighted(
        target_min=1850,
        target_max=2050,
        overall_min=1,
        overall_max=3000,
        skew_strength=0.45,
    ):
        # Generates a year between 1 and 3000 with a bias between 1850 to 2050

        target_mean = (target_min + target_max) / 2
        target_std_dev = (target_max - target_min) * skew_strength

        while True:
            # Generate a random year using normal distribution
            year = int(random.gauss(target_mean, target_std_dev))

            # Validate the year falls within the overall range
            if overall_min <= year <= overall_max:
                return year

    def generate_random_date():
        year = generate_year_weighted()

        # Determine if it's a leap year
        leap = is_leap(year)

        # Generate a random month
        month = random.randint(1, 12)

        # Determine the number of days in the month and generate a random day
        if month in {1, 3, 5, 7, 8, 10, 12}:
            day = random.randint(1, 31)
        elif month == 2:
            if leap:
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        else:
            day = random.randint(1, 30)
        return year, month, day

    def parse_custom_date(date_input):
        try:
            month, day, year = map(int, date_input.split("/"))
            if not 1 <= month <= 12:
                raise ValueError("Month must be between 1 and 12.")
            if not 1 <= day <= 31:
                raise ValueError("Day must be between 1 and 31.")
            if not 1 <= year <= 3000:
                raise ValueError("Year must be between 1 and 3000.")

            if month in {4, 6, 9, 11} and day > 30:
                raise ValueError("Invalid day for the given month.")
            if month == 2:
                if is_leap(year) and day > 29:
                    raise ValueError("Invalid day for February in a leap year.")
                elif not is_leap(year) and day > 28:
                    raise ValueError("Invalid day for February in a non-leap year.")
            return year, month, day

        except ValueError as e:
            print(f"Invalid input: {e} Please try again.")

    # Return the functions used in following functions
    return generate_random_date, parse_custom_date, is_leap


def find_doomsday():
    """Determine the day/doomsday given the date/year"""

    _, _, is_leap = date()

    # Dictionary to map index to day of the week
    dict_day = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }

    def dooms_day(year):
        # Gregorian calendar repeats every 400 years
        a = year % 400

        # Determine the anchor day based on the century
        if 0 <= a < 100:
            anchor = 2  # Tuesday
        elif 100 <= a < 200:
            anchor = 0  # Sunday
        elif 200 <= a < 300:
            anchor = 5  # Friday
        else:
            anchor = 3  # Wednesday

        # Find the doomsday for the year's last two digits
        y = year % 100

        # Doomsday algorithm developed by John Conway
        doomsday = (y // 12 + y % 12 + (y % 12) // 4 + anchor) % 7

        # Return the index of the doomsday
        return doomsday

    def day_of_week(year, month, day, doomsday_index):
        # Dictionary for known doomsday date (month, day) pairs
        month_doomsday = {
            1: 3,  # January 3 (January 4 in leap years)
            2: 28,  # February 28 (February 29 in leap years)
            3: 14,  # March 14
            4: 4,  # April 4
            5: 9,  # May 9
            6: 6,  # June 6
            7: 11,  # July 11
            8: 8,  # August 8
            9: 5,  # September 5
            10: 10,  # October 10
            11: 7,  # November 7
            12: 12,  # December 12
        }

        # Adjust for leap years
        if is_leap(year):
            month_doomsday[1] = 4
            month_doomsday[2] = 29

        # Calculate the day of the week
        delta = day - month_doomsday[month]
        day_index = (doomsday_index + delta) % 7

        # Return the day of the week
        return dict_day[day_index]

    return dooms_day, day_of_week, dict_day


def learn():
    """Return the day of the week, given the input of a date"""

    # Call the necessary functions and variables from prior functions
    _, parse_custom_date, _ = date()
    dooms_day, day_of_week, _ = find_doomsday()

    while True:
        custom_date = input(
            "Please input a date in MM/dd/yyyy format (or type 'q' to quit): "
        )

        # Allow the user to exit
        if custom_date.lower() == "q":
            break

        parsed_date = parse_custom_date(custom_date)

        # Allow the user to be re-prompted upon a ValueError
        if parsed_date is None:
            continue

        year, month, day = parsed_date
        doomsday_index = dooms_day(year)
        correct_day = day_of_week(year, month, day, doomsday_index)
        print(f"{month}/{day}/{year} is a {correct_day}.")


def quiz():
    """Main quiz function."""

    # Call the necessary functions and variables from prior functions
    generate_random_date, _, _ = date()
    dooms_day, day_of_week, dict_day = find_doomsday()

    def check_guess(correct_day):
        # Loop to ensure valid input as a day of week
        while True:
            guess = input("Your guess: ").strip().capitalize()
            if guess in dict_day.values():
                return guess == correct_day
            else:
                print("Invalid input. Please enter a valid day of the week.")

    # Select difficulty level
    print(
        """Select your desired game mode:\n"""
        """1 - Determine the doomsday for a given year.\n"""
        """2 - Determine the day of the week for a given date, written in MM/dd/yyyy format."""
    )
    while True:
        try:
            level = int(input("Enter 1 or 2: "))
            if level not in [1, 2]:
                raise ValueError
            break
        except ValueError:
            print("Invalid option. Please enter 1 or 2.")

    # Initialize score
    score = 0
    total_rounds = 0
    while True:
        try:
            n = int(input("How many rounds would you like to try?: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:

        # Generate a random date/year
        year, month, day = generate_random_date()
        doomsday_index = dooms_day(year)

        if level == 1:
            # Doomsday given the year
            correct_day = dict_day[doomsday_index]
            print(f"What is the doomsday for the year {year}?")

        elif level == 2:
            # Day of the week given the date
            correct_day = day_of_week(year, month, day, doomsday_index)
            print(f"What is the day of the week for {month:02}/{day:02}/{year}?")

        # Check the input guess
        is_correct = check_guess(correct_day)
        total_rounds += 1

        if is_correct:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct_day}.")

        # Check if the user wishes to continue after reaching desired number of rounds
        if total_rounds == n:
            print(f"Your current score is {score} out of {total_rounds}.")

            # Loop until a valid response (y/n) is given
            while True:
                prompt = input("Would you like to continue? (y/n): ").lower().strip()
                if prompt == "y":
                    # Loop until a valid integer is given
                    while True:
                        try:
                            n += int(
                                input("How many more rounds would you like to try?: ")
                            )
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid integer.")
                    break
                elif prompt == "n":
                    break
                else:
                    print("Invalid input. Please enter 'y' to continue or 'n' to quit.")

        if total_rounds == n:
            break

    if total_rounds > 0:
        score_percent = (score / total_rounds) * 100
        print(f"Your final score is {score_percent:.2f}%. Thanks for playing!")
    else:
        print("No rounds were played.")


trial = input("Would you like to learn or quiz?: ")
if trial == "learn":
    learn()
elif trial == "quiz":
    quiz()
else:
    print("please respect your time better.")


# to do:
# Properly running the program
# fix the last loop so i don't need another if statement to break out?
# add a clock function to test how long you take, add a scoring component to the time taken as well
# get it on github
