# Quick Start Guide - FMD Watch Eswatini

Get your FMD monitoring platform running in 5 minutes!

## 🚀 Super Quick Setup

```bash
# 1. Navigate to project directory
cd fmd_eswatini

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted

# 6. Load sample data
python manage.py shell < load_sample_data.py

# 7. Run the server
python manage.py runserver
```

## 🎉 You're Ready!

- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/outbreaks/

The interactive map will display using OpenStreetMap tiles (no API key required).

## 📝 Next Steps

1. **Add Real Data**: Use admin panel to add actual outbreak data
2. **Customize**: Update colors, logos, and contact information
3. **Configure**: Update settings for your production environment

## 🆘 Troubleshooting

**Map not showing?**
- Check browser console (F12) to see any JavaScript errors
- Ensure internet connection for OpenStreetMap tiles

**Sample data not loading?**
- Make sure migrations are run: `python manage.py migrate`
- Try running the script again

**Admin panel login issues?**
- Re-create superuser: `python manage.py createsuperuser`

**Port 8000 already in use?**
- Use different port: `python manage.py runserver 8001`

## 📚 Learn More

See README.md for detailed documentation, API endpoints, and deployment instructions.

---

**Need Help?**
Check Django documentation: https://docs.djangoproject.com/