# E-commerce Website using Django Framework

**Features :**
- User Authentication and Authorization
- CRUD functionalities 
- Django Form
- Password Change
- Reset Password
- Figure out Top Sell
- Search Product

**Project Documentation :** The **"ecommerce"** directory consists of "settings.py", if a new app is created please ensure that you have included the app name there. **"media"** directory holds all the images uploaded via django-admin(dashboard). Static files stored inside the **"static"** folder. Neccessary templates store inside **"templates"** directory. Here **"base"** folder is the main application folder, it consist of views,model and urls.

**How to Run :**
Please follow the below instructions to run this project in your machine:
1. Clone the repository
    ```sh
    git clone https://github.com/mzahid36/ecommerce2_django.git
    ```
2. Intall necessary libraries(Django 4.2, Pillow 10.0.0).
3. To access the dashboard, please create a superuser.
   ```sh
    python manage.py createsuperuser
    ```
4. To run the project
   ```sh
    python manage.py runserver
    ```