
import mysql.connector

# Establishing MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hema2326",
    database="election"
)

mycursor = mydb.cursor()

class CandidateUser:
    @staticmethod
    def cantitate():
        sql_check = "SELECT Id FROM canditate_details WHERE Name = %s"
        sql_insert = "INSERT INTO canditate_details (Id, Name, political_party) VALUES (%s, %s, %s)"        
        
        Id = [1, 2, 3]
        Name = ["Vijay", "Seemaan", "Annamalai"]
        political_party = ["TVK", "NTK", "PGP"]
        
        # Prepare a list of tuples for all candidates
        candidates = []
        try:
            for i in range(len(Id)):
                # Check if candidate with the same name already exists
                mycursor.execute(sql_check, (Name[i],))
                result = mycursor.fetchone()
                
                if not result:  # If result is None (candidate name doesn't exist), insert the candidate
                    candidates.append((Id[i], Name[i], political_party[i]))
                else:
                    print(f"Skipping insertion for '{Name[i]}' as it already exists in the database.")
            
            if candidates:
                # Print candidates for debugging
                print("Candidates to be inserted:", candidates)

                # Execute the query for each candidate
                mycursor.executemany(sql_insert, candidates)
                mydb.commit()
            else:
                print("No new candidates to insert.")
        except mysql.connector.Error as err:
            print("Error:", err)

class VoterUser:
    @staticmethod
    def display_candidates():
        try:
            sql_select = "SELECT Id, Name, political_party FROM canditate_details"
            mycursor.execute(sql_select)
            candidates = mycursor.fetchall()
            
            if candidates:
                print("Candidates:")
                for candidate in candidates:
                    print(f"{candidate[0]} - {candidate[1]} ({candidate[2]})")
            else:
                print("No candidates found.")
        except mysql.connector.Error as err:
            print("Error:", err)

    @staticmethod
    def vote(candidate_name):
        try:
            sql_update = "UPDATE canditate_details SET total_votes = total_votes + 1 WHERE Name = %s"
            mycursor.execute(sql_update, (candidate_name,))
            mydb.commit()  # Commit the transaction to apply the update immediately
            print(f"Voted successfully for '{candidate_name}'.")
        except mysql.connector.Error as err:
            print("Error:", err)

try:
    role = input("Are you a 'candidate' or 'voter'? ").lower()
    if role == 'candidate':
        CandidateUser.cantitate()
    elif role == 'voter':
        VoterUser.display_candidates()
        print("\nVote for a candidate (enter candidate's name):")
        candidate_to_vote = input().strip()
        VoterUser.vote(candidate_to_vote)
    else:
        print("Please enter either 'candidate' or 'voter'.")
   
except mysql.connector.Error as err:
    print("Database Error:", err)
finally:
    if mydb:
        mydb.close()
