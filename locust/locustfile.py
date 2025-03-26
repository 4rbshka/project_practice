from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  

    @task
    def load_main_page(self):
        self.client.get("/")  

    @task
    def load_users(self):
        self.client.get("/users/") 