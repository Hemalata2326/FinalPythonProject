import mysql.connector

# Establishing MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hema2326",
    database="movie_booking_system"
)
cursor = mydb.cursor()

def setup_database():
    # Predefined movies
    ids = [1, 2, 3]
    names = ["Beast", "Kazhugu", "Thirupachi"]
    available_tickets = [50, 30, 20]
    
    # Insert movies if not already in the database
    for i in range(len(ids)):
        cursor.execute("SELECT id FROM movies WHERE id = %s", (ids[i],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO movies (id, name, available_tickets) VALUES (%s, %s, %s)", (ids[i], names[i], available_tickets[i]))
    
    mydb.commit()

def show_movies():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    
    print("Available movies:")
    for movie in movies:
        print(f"ID: {movie[0]}, Name: {movie[1]}, Available Tickets: {movie[2]}")

def book_ticket(user_name):
    show_movies()
    
    movie_id = int(input("Enter the movie ID to book a ticket: "))
    
    # Check ticket availability
    cursor.execute("SELECT available_tickets FROM movies WHERE id = %s", (movie_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.execute("INSERT INTO booking (movie_id, user_name) VALUES (%s, %s)", (movie_id, user_name))
        cursor.execute("UPDATE movies SET available_tickets = available_tickets - 1 WHERE id = %s", (movie_id,))
        mydb.commit()
        print("Ticket booked successfully!")
    else:
        print("Sorry, no tickets available.")

def main():
    setup_database()
    
    user_name = input("Enter your name: ")
    
    while True:
        print("\nMovie Ticket Booking System")
        print("1. Show Movies")
        print("2. Book Ticket")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            show_movies()
        elif choice == '2':
            book_ticket(user_name)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
