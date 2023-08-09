import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
DAYS = ['Monday', 'Tuesday', 'Wednsday', 'Thusrday', 'Friday', 'Saturday', 'Sunday', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    repeat = True
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while repeat:
        global city
        city = input("Pelase choose the city: ").lower()

        if city not in CITY_DATA:
            print("City does not exist, please try again.")

        # while repeat_month:

        if city in CITY_DATA:
            while repeat:
                month = input("Pelase choose the month: ").title()
                if month not in MONTH:
                    print("Month does not exist, please try again.")
                if month in MONTH:
                    while repeat:
                        day = input("Pelase choose the day: ").title()
                        if day not in DAYS:
                            print("Day does not exist, please try again.")
                        else:
                            repeat = False


    print('-'*40)
    return city, month, day

#get_filters()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Sart Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Sart Time'].dt.month
    df['day_of_week'] = df['Sart Time'].dt.dayofweek
    df['hour'] = df['Sart Time'].dt.hour

    if month != 'All':
        month = MONTH.index(month) + 1
        df = df[df['month'] == month]
    if day != 'All':
        day = DAYS.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df
    
def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc: start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #print(df['month'])
    common_month = df['month'].mode()[0]
    print(f"Most comon month: {MONTH[common_month -1]}")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most comon day: {DAYS[common_day - 1]}")
    # display the most common start hour
    common_star_hour = df['hour'].mode()[0]
    print(f"Most comon hour: {common_star_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].value_counts().index[0]
    start_count = df['Start Station'].value_counts().max()
    print(f"Most commonly used start station is {most_used_start_station} and it has been used {start_count} times.")

    # display most commonly used end station
    most_used_end_station = df['End Station'].value_counts().index[0]
    end_count = df['End Station'].value_counts().max()
    print(f"Most commonly used end station is {most_used_end_station} and it has been used {end_count} times.")


    # display most frequent combination of start station and end station trip

    #common_start_and_end = df[['Start Station','End Station']].value_counts().index[0]
    #start_end_count = df[['Start Station','End Station']].value_counts().max()
    #print(f"Most commonly used start and end stations are {common_start_and_end} and they have been used {start_end_count} times.")

    pop_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most popular trip is: from {pop_trip.mode()[0]}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['diference'] = df['End Time'] - df['Start Time']
    df['sum'] = df['diference'].sum()
    print(f"Total trip duration: {df['sum'].max()}")

    # display mean travel time
    df['average'] = df['diference'].mean()
    print(f"Average travel time: {df['average'].max()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    #user_type_count.to_string(dtype=False)
    print(f"Count of user type:\n{user_type_count.to_string()}")
    try:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(f"\nCount of user gender:\n{gender.to_string()}")

        # Display earliest, most recent, and most common year of birth
        erliest_yob = df['Birth Year'].sort_values().min()
        print(f"\nErliest year of birth: {int(erliest_yob)}")

        recent_yob = df['Birth Year'].sort_values().max()
        print(f"Most recent year of birth: {int(recent_yob)}")

        common_yob = df['Birth Year'].value_counts().idxmax()
        print(f"Most common year of birth: {int(common_yob)}")

    except:
        print(f'\nFor {city.title()} data about this part is not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()




