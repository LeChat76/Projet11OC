from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def clubSummary(self):
        self.client.get('clubsSummary')
    
    @task
    def login(self):
        self.client.post('showSummary', {'email':'admin@irontemple.com'})
    
    @task
    def book(self):
        self.client.get('book/Fall Classic/Iron Temple')

    @task
    def logout(self):
        self.client.get('logout')