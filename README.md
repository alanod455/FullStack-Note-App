# Note-App

A modern Django web application for managing notes.  
Users can create, view, update, and delete notes with a clean, user-friendly interface.

---

## 🛠️ Technologies Used

- **Backend:** Django 5.2.7  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite  
- **Static files:** CSS stored in `main_app/static/css/`  

---

## 🚀 Installation & Running Locally

1. **Clone the repository:**
```
git clone https://github.com/alanod455/FullStack-Note-App.git 
```
2. **Navigate to the project folder:**
```
cd FullStack-Note-App/Note-Alanoud
```
3. **Install Pipenv if you don't have it:**
```
pip install pipenv
```
4. **Install dependencies and create a virtual environment:**
```
pipenv install
```
5. **Activate the virtual environment:**
```
pipenv shell
```
6. **Apply database migrations:**
```
python manage.py migrate
```
7. **Run the development server:**
```
python manage.py runserver
```
8. **Open your browser and visit:**
```
http://127.0.0.1:8000/
```