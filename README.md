# GigBridge 
**Connecting Talent with Opportunity**

A full-featured freelance marketplace built with Django 6 and Bootstrap 5, developed as a 3-week team project.

---

## 📸 Screenshots

### Landing Page
![Landing Page](images/landing.png)

### Browse Tasks
![Browse Tasks](images/browse_tasks.png)

### Client Dashboard
![Client Dashboard](images/client_dashboard.png)

### Find Freelancers
![Find Freelancers](images/freelancers.png)

### Login & Register
![Login](images/login.png)

---

## ✨ Features

### For Clients
- Register as a client and post detailed tasks with budgets, deadlines and required skills
- Browse freelancer profiles filtered by skill and availability
- Receive and review proposals with cover letters and pricing
- Award tasks to the best candidate in one click
- Mark tasks complete and leave star ratings and reviews

### For Freelancers
- Register and build a profile with skills, bio, and hourly rate
- Browse and search open tasks by category and budget
- Submit proposals with cover letters and estimated delivery time
- Track proposal status from a personal dashboard
- Build a review history to attract more clients

### Platform
- Role-based access control — clients and freelancers see different dashboards
- In-app notification bell for proposals, awards, and reviews
- Public browse pages for tasks and freelancers — no login required
- Fully responsive at 375px (mobile), 768px (tablet), and 1280px (desktop)
- Custom branded 404 and 500 error pages

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6 |
| Frontend | Bootstrap 5 (CDN) + Custom CSS |
| Database | SQLite (development) |
| Authentication | Django built-in session auth |
| Icons | Bootstrap Icons 1.11 |
| Fonts | DM Sans (headings) · Inter (body) |

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.12+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/thevinduperera/gigbridge.git
cd gigbridge
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## ⚠️ Important — Add Categories Before Posting Tasks

The **Post a New Task** form includes a **Category** dropdown. This dropdown will appear empty until categories are added through the Django admin panel.

**To add categories:**

1. Go to **http://127.0.0.1:8000/admin**
2. Log in with your superuser credentials
3. Click **Categories** under the Tasks section
4. Click **Add Category** and create your categories

**Suggested default categories to add:**
- Web Development
- Graphic Design
- Writing & Content
- Digital Marketing
- Mobile Apps
- Data & Analytics
- Video & Animation
- Accounting & Finance

Once categories are added, they will automatically appear in the Post a Task form and the Browse by Category section on the landing page.

---

## 🗂 Project Structure
```bash
gigbridge/
├── gigbridge/         
├── accounts/            
├── tasks/               
├── proposals/         
├── core/                
├── static/
│   ├── css/main.css     
│   └── js/main.js      
├── templates/
│   ├── base.html      
│   ├── navbar.html      
│   ├── footer.html     
│   ├── 404.html        
│   ├── 500.html        
│   ├── core/            
│   ├── accounts/        
│   ├── tasks/           
│   └── proposals/       
├── images/               
├── requirements.txt
└── README.md
```
---

## 👥 Team

| Member | App | Responsibilities |
|---|---|---|
| Member 1 - Dimeth | `accounts` | Custom user model, authentication, role-based profiles |
| Member 2 - Thevindu | `tasks` | Task CRUD, categories, client & freelancer dashboards |
| Member 3 - Linal | `proposals` | Proposal submission, award/reject flow, review system |
| Member 4 - Akila | `core` | Landing page, public browse pages, notifications, global UI/CSS |

---

## 🎨 Design System

All colours are defined as CSS variables in `static/css/main.css`. Never use raw hex values in templates — always use the variables.

| Variable | Hex | Usage |
|---|---|---|
| `--slate-900` | `#0f172a` | Navbar, hero background, headings |
| `--slate-800` | `#1e293b` | Footer, stats strip |
| `--slate-700` | `#334155` | Dark body text |
| `--slate-500` | `#64748b` | Muted text, placeholders |
| `--slate-200` | `#e2e8f0` | Borders, dividers |
| `--slate-100` | `#f1f5f9` | Page backgrounds, badges |
| `--teal-600` | `#0d9488` | Primary buttons, accents, links |
| `--teal-500` | `#14b8a6` | Hover states, highlights |
| `--teal-100` | `#ccfbf1` | Light teal fills, badges |

**Fonts:** DM Sans (headings, 700/500 weight) · Inter (body, 400/500 weight)

---

## 📋 Git Commit Conventions
- feat: add proposal submission form
- fix: correct task status update logic
- style: apply teal accent to dashboard cards
- refactor: extract notification helper to utils.py
- docs: update README with setup instructions
- chore: add Pillow to requirements.txt

---

## 🔗 Key URLs

| URL | Page |
|---|---|
| `/` | Landing page |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/tasks/` | Browse tasks |
| `/freelancers/` | Find freelancers |
| `/notifications/` | Notifications |
| `/tasks/dashboard/client/` | Client dashboard |
| `/tasks/dashboard/freelancer/` | Freelancer dashboard |
| `/admin/` | Django admin |

---

*Built with ❤️ by the GigBridge Team*
