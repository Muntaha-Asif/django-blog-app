# 📰 Django Blog Application

A full-featured blogging platform built with Django, featuring user authentication, CRUD operations, real-time interactions, and a modern responsive UI.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)


## ✨ Features

### 🔐 Authentication & Authorization
- User registration with validation
- Secure login/logout system
- Password hashing with Django's built-in authentication
- Role-based permissions (only authors can edit/delete their posts)
- Session management

### 📝 Blog Functionality
- **CRUD Operations**: Create, Read, Update, Delete blog posts
- **Rich Content**: Support for text content and image uploads
- **Draft System**: Save posts as drafts or publish immediately
- **Categories**: Organize posts into categories
- **Search**: Full-text search across titles, content, and authors
- **Pagination**: Efficient loading with 6 posts per page

### 💬 Social Features
- **Like System**: AJAX-powered like/unlike functionality
- **Comments**: Threaded comment system with replies
- **View Counter**: Track post popularity
- **Reading Time**: Auto-calculated based on word count

### 👤 User Profiles
- Customizable avatars
- Bio and location information
- Personal website links
- User-specific post listings
- View posts by specific authors

### 📊 Analytics Dashboard
- Total posts, views, likes, and comments
- Published vs draft posts tracking
- Recent posts overview
- Most popular posts ranking
- Personal statistics and insights

### 🎨 Modern UI/UX
- Responsive design (mobile, tablet, desktop)
- Beautiful gradient backgrounds
- Smooth CSS animations
- Interactive hover effects
- Card-based layout
- Modern color scheme

---

## 🛠️ Technologies Used

### Backend
- **Python 3.10+**
- **Django 5.2** - Web framework
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Pillow** - Image processing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with custom animations
- **JavaScript (ES6+)** - Interactive features
- **AJAX** - Asynchronous operations
- **Fetch API** - HTTP requests

### Deployment
- **PythonAnywhere** - Hosting platform
- **Git** - Version control
- **WhiteNoise** - Static file serving (if using)

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- pip (Python package manager)
- Git
- Virtual environment tool

---

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/django-blog-app.git
cd django-blog-app
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to set username, email, password

# Create profiles for existing users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from blog.models import Profile
>>> for user in User.objects.all():
...     Profile.objects.get_or_create(user=user)
>>> exit()
```

### 6. Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure
```
DjangoBlogApp/
│
├── blog_project/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI configuration
│   ├── templates/            # Shared templates
│   │   └── base.html         # Base template
│   └── static/               # Static files (CSS, JS)
│
├── blog/                      # Main blog application
│   ├── migrations/           # Database migrations
│   ├── templates/blog/       # Blog-specific templates
│   │   ├── home.html
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form classes
│   ├── models.py            # Database models
│   ├── signals.py           # Signal handlers
│   ├── urls.py              # Blog URL patterns
│   └── views.py             # View functions and classes
│
├── accounts/                 # Authentication application
│   ├── templates/accounts/  # Auth templates
│   │   ├── login.html
│   │   ├── register.html
│   │   └── logout.html
│   ├── __init__.py
│   ├── urls.py
│   └── views.py
│
├── media/                    # User-uploaded files
│   ├── post_images/         # Blog post images
│   └── avatars/             # User avatars
│
├── staticfiles/             # Collected static files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🗄️ Database Schema

### Models Overview
```
User (Django built-in)
├── Profile (One-to-One)
│   ├── avatar
│   ├── bio
│   ├── website
│   └── location
│
└── Post (Foreign Key)
    ├── title
    ├── content
    ├── image
    ├── category (Foreign Key to Category)
    ├── status (draft/published)
    ├── views
    ├── date_posted
    └── date_updated
    │
    ├── Like (Foreign Key)
    │   ├── user
    │   └── created_at
    │
    └── Comment (Foreign Key)
        ├── author
        ├── content
        ├── parent (self-referencing for replies)
        └── date_posted
```

---

## 🔑 Key Features Explained

### AJAX-Powered Like System

The like functionality uses AJAX for a seamless user experience:

**Frontend (JavaScript):**
```javascript
function toggleLike(postId) {
    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        // Update UI without page reload
        updateLikeButton(data.liked);
        updateLikeCount(data.total_likes);
    });
}
```

**Backend (Django):**
```python
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(
        user=request.user, 
        post=post
    )
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })
```

### Automated Profile Creation

Using Django signals to automatically create user profiles:
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### Advanced Search

Multi-field search using Django Q objects:
```python
queryset = Post.objects.filter(
    Q(title__icontains=query) |
    Q(content__icontains=query) |
    Q(author__username__icontains=query)
)
```

---

## 🎨 UI/UX Highlights

- **Gradient Backgrounds**: Modern purple gradient theme
- **Card Design**: Clean, shadow-based card layouts
- **Animations**: Smooth CSS transitions and hover effects
- **Responsive Grid**: Auto-adjusting grid layout for different screen sizes
- **Mobile Menu**: Hamburger menu for mobile devices
- **Loading States**: Visual feedback for async operations
- **Form Validation**: Real-time client-side validation

---

## 🚀 Deployment

### Deploy to PythonAnywhere

1. **Create account** at [PythonAnywhere](https://www.pythonanywhere.com)

2. **Clone repository**:
```bash
git clone https://github.com/yourusername/django-blog-app.git
```

3. **Setup virtual environment**:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

4. **Configure settings**:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
DEBUG = False
```

5. **Setup database**:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

6. **Configure WSGI** and **static files** in PythonAnywhere web tab

7. **Reload** your web app

**Detailed deployment guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with post list |
| GET | `/post/<id>/` | View single post |
| GET | `/post/new/` | Create post form |
| POST | `/post/new/` | Submit new post |
| GET | `/post/<id>/update/` | Edit post form |
| POST | `/post/<id>/update/` | Submit post update |
| GET | `/post/<id>/delete/` | Delete confirmation |
| POST | `/post/<id>/delete/` | Confirm deletion |
| POST | `/post/<id>/like/` | Like/unlike post (AJAX) |
| POST | `/post/<id>/comment/` | Add comment |
| POST | `/comment/<id>/delete/` | Delete comment |
| GET | `/category/<slug>/` | Posts by category |
| GET | `/user/<username>/` | Posts by user |
| GET | `/profile/` | User profile page |
| POST | `/profile/` | Update profile |
| GET | `/dashboard/` | User dashboard |
| GET | `/accounts/register/` | Registration form |
| POST | `/accounts/register/` | Submit registration |
| GET | `/accounts/login/` | Login form |
| POST | `/accounts/login/` | Submit login |
| POST | `/accounts/logout/` | Logout |

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing Checklist

- [ ] User registration works
- [ ] Login/logout functionality
- [ ] Create new post
- [ ] Edit own post (permissions work)
- [ ] Delete own post
- [ ] Cannot edit others' posts
- [ ] Like/unlike posts
- [ ] Add comments
- [ ] Delete own comments
- [ ] Search functionality
- [ ] Category filtering
- [ ] Profile update
- [ ] Image upload
- [ ] Draft/publish workflow
- [ ] Responsive design (mobile, tablet)
- [ ] Dashboard statistics

---

## 🔒 Security Features

- **CSRF Protection**: Django's built-in CSRF tokens
- **SQL Injection Prevention**: ORM automatically escapes queries
- **XSS Protection**: Template auto-escaping
- **Password Hashing**: PBKDF2 algorithm with salt
- **Session Security**: Secure session management
- **Permission Checks**: User-specific authorization
- **File Upload Validation**: Image type verification

---

## 🐛 Known Issues & Future Enhancements

### Known Issues
- None currently reported

### Planned Features
- [ ] Email notifications for comments
- [ ] Social media sharing buttons
- [ ] Tags system in addition to categories
- [ ] Bookmark/save posts
- [ ] Follow/unfollow users
- [ ] Rich text editor (WYSIWYG)
- [ ] Post scheduling
- [ ] Advanced analytics
- [ ] API for mobile apps (Django REST Framework)
- [ ] Dark mode toggle

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Muntaha Asif**

- GitHub: (https://github.com/Muntaha-Asif)
- LinkedIn: (https://www.linkedin.com/in/muntaha-asif-84156732a/)

---

## 🙏 Acknowledgments

- Django Documentation
- Python Community
- Stack Overflow Community
- Bootstrap (for inspiration)
- All contributors and testers

---

## 📞 Support

If you have any questions or need help, feel free to:
- Open an issue
- Contact me via email
- Connect on LinkedIn

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Built with ❤️ using Django**

---

## 📊 Project Statistics

- **Lines of Code**: ~3,000+
- **Files**: 30+
- **Models**: 5
- **Views**: 15+
- **Templates**: 12+
- **Development Time**: 2 weeks

---

*Last Updated: January 2026*
```
