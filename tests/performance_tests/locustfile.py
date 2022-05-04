from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def home(self):
        self.client.get('')

    @task
    def clubsboard(self):
        self.client.get('clubsboard')

    @task
    def login(self):
        self.client.post('/showSummary', data=dict(email='john@simplylift.co'))

    @task
    def access_competition(self):
        self.client.post('/showSummary', data=dict(email='john@simplylift.co'))
        self.client.get("/book/Summer%20Festival/Simply%20Lift")

    @task
    def booking_places_on_competition(self):
        self.client.post('/showSummary', data=dict(email='john@simplylift.co'))
        self.client.post(
            '/purchasePlaces',
            data=dict(
                club='Simply Lift',
                competition='Summer Festival',
                places=1
            )
        )

    @task
    def logout(self):
        self.client.post('/showSummary', data=dict(email='john@simplylift.co'))
        self.client.get('/logout')
