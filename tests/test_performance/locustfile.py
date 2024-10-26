from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"

    def on_start(self):
        """Executed when a simulated user starts interacting with the system."""
        self.client.get("/")  # Charge la page d'accueil avant de se connecter
        self.login()

    def login(self):
        # Connection avec un email valide depuis clubs.json
        response = self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        if "Welcome" in response.text:  # Vérifie la réponse en texte plutôt qu'en bytes
            print("Login successful")
        else:
            print("Login failed")

    @task(2)
    def view_competitions(self):
        """Simulate viewing the available competitions."""
        # D'abord se connecter pour voir les compétitions
        self.login()
        response = self.client.get("/showSummary", data={"email": "john@simplylift.co"})
        if "Competitions" in response.text:
            print("Viewed competitions successfully")
        else:
            print("Failed to view competitions")

    @task(1)
    def make_reservation(self):
        """Simulate reserving places for a competition."""
        # D'abord se connecter
        self.login()
        # Faire une réservation
        response = self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",  # Nom exact de la compétition
            "club": "Simply Lift",
            "places": "2"
        })
        if "Reservation effectuee avec succes" in response.text:
            print("Reservation successful")
        else:
            print("Reservation failed")

    @task(1)
    def test_booking_page(self):
        """Test accessing the booking page for a specific competition."""
        self.login()
        response = self.client.get("/book/Spring Festival/Simply Lift")
        if "Places available" in response.text:
            print("Booking page accessed successfully")
        else:
            print("Failed to access booking page")

    @task(1)
    def logout(self):
        """Simulate logging out."""
        response = self.client.get("/logout")
        if response.status_code == 302:  # Code de redirection
            print("Logout successful")
        else:
            print("Logout failed")

    @task(3)
    def failed_login(self):
        """Simulate a failed login."""
        response = self.client.post("/showSummary", data={"email": "wrongemail@simplylift.com"})
        if "Email non trouve" in response.text:
            print("Email non trouve successful")
        else:
            print("Failed login test failed")