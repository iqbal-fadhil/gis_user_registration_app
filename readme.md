# 🗺️ GIS User Registration App

This is a Django 5.2-based web application that allows users to register with extended profile information, including geographic location using **GeoDjango** and **PostGIS**.

---

## 🚀 Features

* ✅ User registration and login
* ✅ Extended user profile with:

  * Home address
  * Phone number
  * Geographic location (PointField with latitude & longitude)
* ✅ Spatial data support using GeoDjango
* ✅ PostgreSQL + PostGIS backend
* ✅ Unit test for registration with profile

---

## 🧩 Requirements

* Python 3.10+
* PostgreSQL with PostGIS
* Spatial libraries:

  * GEOS
  * PROJ
  * GDAL

---

## 📦 Python Dependencies (`requirements.txt`)

```txt
asgiref==3.8.1
Django==5.2
django-leaflet==0.31.0
geojson==3.2.0
psycopg2==2.9.10
psycopg2-binary==2.9.10
sqlparse==0.5.3
typing_extensions==4.13.2
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/gis-user-registration.git
   cd gis-user-registration
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL + PostGIS**
   Make sure your PostgreSQL database has the PostGIS extension enabled:

   ```sql
   CREATE EXTENSION postgis;
   ```

5. **Configure database settings in `settings.py`**

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   ```

6. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the app at**

   ```
   http://localhost:8000/register/
   ```
---


## 🧪 How to Test the App

### ✅ Functional Test via Browser

1. **Register a new user**

   * Visit `http://localhost:8000/register/`
   * Fill in the form and submit
   * The user will automatically be:

     * Logged in
     * Assigned `is_staff=True` so they can access the Django admin
     * Redirected to home page

2. **Edit Profile**

   * Go to `http://localhost:8000/profile/edit/`
   * Update your home address, phone number, and choose your location on the map

3. **View Profile**

   * Go to `http://localhost:8000/profile/` to see your profile data

4. **Log out and log back in**

   * Log out at `http://localhost:8000/logout/`
   * Log in again at `http://localhost:8000/login/`

---

## 🔐 Admin Dashboard Access

All users registered via the site are now created as **staff** users and can log into the Django admin panel.
 
* Go to `http://localhost:8000/admin/`
* Login with your user credentials

### 🎯 Admin Permissions

* **Regular staff users** (registered via the site):

  * Can access Django admin
  * Can view and edit **only their own** `UserProfile` entry
  * Cannot see or modify other users' profiles

* **Superusers** (created via `createsuperuser`):

  * Can view and edit **all** `UserProfile` entries
  * Have full control over the Django admin dashboard

---


---

## 🧪 Running Tests

To run tests:

```bash
python manage.py test
```

Use the test from branch testing.
Make sure user of PostgreSQL is ready (exists and as a SUPERUSER) before running test
Just input the name of desired database (not the database for running the project).

---

## 📂 Project Structure

```
gisproject/
├── gisapp/
│   ├── migrations/
│   ├── templates/
|   |   └── base.html
|   |   └── edit_profile.html
|   |   └── login.html
|   |   └── profile.html
|   |   └── register.html
|   |   └── user_locations_map.html
│   ├── tests.py
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── gisproject/
│   └── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## ⚠️ Notes

* If using `psycopg2` in development, you can use `psycopg2-binary`. For production, prefer `psycopg2`.
* Make sure GDAL, GEOS, and PROJ are installed on your system:

  ```bash
  sudo apt install binutils libproj-dev gdal-bin
  ```
