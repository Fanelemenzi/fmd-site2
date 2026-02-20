# FMD Watch - Eswatini

A comprehensive web platform for monitoring Foot and Mouth Disease outbreaks in Eswatini.

## 🌟 Features

- **Interactive Map**: Real-time visualization of FMD outbreaks using Leaflet.js and OpenStreetMap
- **Dip Tank Areas**: 5km radius circles showing affected and clear areas around dip tank locations
- **Outbreak Tracking**: Monitor active, surveillance, and cleared outbreak zones
- **News & Updates**: Stay informed with the latest FMD-related announcements
- **Control Measures**: Comprehensive guidelines for farmers and livestock owners
- **Statistics Dashboard**: Track outbreak statistics by region and status
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **RESTful API**: JSON API for data access and integration

## 🛠️ Technology Stack

### Backend
- **Django 5.0.1** - Python web framework
- **Django REST Framework** - API development
- **PostgreSQL** (recommended for production) / SQLite (development)
- **PostGIS** (for production geospatial queries)

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework
- **Leaflet.js** - Interactive map visualization with OpenStreetMap

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd fmd_eswatini
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

The project is configured to use SQLite for development by default. For production, you should use PostgreSQL with PostGIS.

**Development (SQLite - default):**
No additional configuration needed.

**Production (PostgreSQL with PostGIS):**
1. Install PostgreSQL and PostGIS
2. Create a database
3. Update `config/settings.py` to use PostgreSQL (uncomment the PostgreSQL configuration)

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## 📊 Adding Sample Data

### Using Django Admin

1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add outbreaks and updates through the admin interface

### Using Django Shell

```bash
python manage.py shell
```

Then run:

```python
from outbreaks.models import Outbreak
from updates.models import Update
from django.utils import timezone

# Create sample outbreak
outbreak = Outbreak.objects.create(
    title="Manzini Region Outbreak - February 2024",
    description="FMD outbreak confirmed in the Manzini region affecting cattle.",
    status="active",
    region="manzini",
    latitude=-26.4833,
    longitude=31.3667,
    location_name="Manzini District Farm",
    animals_affected=45,
    animals_quarantined=120,
    date_reported=timezone.now(),
    is_verified=True,
    is_active=True
)

# Create sample update
update = Update.objects.create(
    title="New FMD Prevention Guidelines Released",
    content="The Ministry of Agriculture has released new biosecurity guidelines...",
    update_type="guideline",
    is_published=True,
    is_featured=True
)

print("Sample data created successfully!")
```

## 🗺️ API Endpoints

### Outbreaks API

**List all outbreaks:**
```
GET /api/outbreaks/
```

**Filter by status:**
```
GET /api/outbreaks/?status=active
```

**Filter by region:**
```
GET /api/outbreaks/?region=manzini
```

**Get GeoJSON for map:**
```
GET /api/outbreaks/geojson/
```

**Get statistics:**
```
GET /api/outbreaks/statistics/
```

**Get single outbreak:**
```
GET /api/outbreaks/{id}/
```

### Dip Tanks API

**List all dip tanks:**
```
GET /api/diptanks/
```

**Filter by affected status:**
```
GET /api/diptanks/?affected=true
GET /api/diptanks/?affected=false
```

**Filter by region:**
```
GET /api/diptanks/?region=manzini
```

**Get GeoJSON for map (with 5km radius data):**
```
GET /api/diptanks/geojson/
```

**Combined filters:**
```
GET /api/diptanks/?region=hhohho&affected=true
```

### Updates API

**List all updates:**
```
GET /api/updates/
```

**Filter by type:**
```
GET /api/updates/?type=alert
```

**Get featured updates:**
```
GET /api/updates/?featured=true
```

**Get single update:**
```
GET /api/updates/{id}/
```

## 📱 Pages

- **Home** (`/`) - Map and statistics dashboard
- **About FMD** (`/about/`) - Information about Foot and Mouth Disease
- **Updates** (`/updates/`) - News and announcements
- **Control Measures** (`/control-measures/`) - Prevention and control guidelines
- **Contact** (`/contact/`) - Emergency contacts and reporting information

## 🎨 Customization

### Colors and Branding

The site uses Tailwind CSS. Main colors are:
- Primary: Emerald (green) - `emerald-600`, `emerald-700`
- Active outbreaks: Red - `red-500`, `red-600`
- Surveillance: Amber - `amber-500`, `amber-600`
- Cleared: Green - `green-500`, `green-600`

To customize colors, update the color classes in the templates.

### Map Styling

The map uses OpenStreetMap tiles by default. You can customize the map by:
1. Changing the tile layer in `templates/pages/home.html`
2. Modifying marker colors and styles
3. Adding custom map controls

### Dip Tank Areas

The system includes dip tank management with 5km radius visualization:

**Features:**
- Each dip tank shows a 5km radius circle on the map
- Red circles indicate affected areas (FMD risk)
- Green circles indicate clear areas (safe zones)
- Interactive popups show dip tank details
- Filter controls to show/hide different area types

**Managing Dip Tanks:**
1. Use Django admin to add/edit dip tank locations
2. Set `is_affected` status to control circle color
3. Add capacity and inspection data for better tracking
4. Use the map filters to focus on specific areas

## 🚢 Deployment

### Production Checklist

1. **Set DEBUG to False** in `config/settings.py`
2. **Change SECRET_KEY** to a secure random string
3. **Configure ALLOWED_HOSTS** with your domain
4. **Use PostgreSQL with PostGIS** instead of SQLite
5. **Set up static file serving** (use Nginx or WhiteNoise)
6. **Configure HTTPS** (use Let's Encrypt)
7. **Set up backup systems** for database
8. **Enable CORS** only for trusted domains

### Recommended Hosting Platforms

- **DigitalOcean** - Easy Django deployment with App Platform
- **Render** - Simple deployment with PostgreSQL
- **Railway** - Quick deployment with database
- **AWS/Azure/GCP** - Enterprise-grade infrastructure

## 🔒 Security Notes

- Change the default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Implement rate limiting for API endpoints
- Regular security updates for dependencies
- Use HTTPS in production
- Implement proper user authentication for admin panel

## 📝 License

This project is developed for public health monitoring in Eswatini.

## 🤝 Support

For technical support or questions:
- Check the Django documentation: https://docs.djangoproject.com/
- Leaflet documentation: https://leafletjs.com/
- Tailwind CSS: https://tailwindcss.com/docs

## 📧 Contact

Ministry of Agriculture, Eswatini
Veterinary Services Department
Email: vet@gov.sz
Phone: +268 2404 2731

---

**Important Notes:**

1. **Map Display**: The map uses OpenStreetMap tiles and doesn't require any API keys
2. **Sample Data**: Use the Django admin or shell to add initial outbreak and update data
3. **Production**: Follow the production checklist before deploying to a live server
4. **Backup**: Regularly backup your database, especially in production

## 🎯 Next Steps

1. Create sample outbreak data through admin
2. Customize colors and branding
3. Add real outbreak data
4. Test on different devices
5. Deploy to production server

Good luck with your FMD monitoring platform!