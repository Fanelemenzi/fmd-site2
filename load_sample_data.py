"""
Sample data loader for FMD Watch Eswatini

Run this script to populate your database with sample outbreak and update data.

Usage:
    python manage.py shell < load_sample_data.py

Or in Django shell:
    exec(open('load_sample_data.py').read())
"""

from django.utils import timezone
from datetime import timedelta
from outbreaks.models import Outbreak, DipTank, CordonLine, FootWashStation
from updates.models import Update

print("Loading sample data...")

# Clear existing data (optional - comment out if you want to keep existing data)
# Outbreak.objects.all().delete()
# Update.objects.all().delete()

# Sample Outbreaks
outbreaks_data = [
    {
        'title': 'Manzini Central Outbreak - February 2024',
        'description': 'Active FMD outbreak confirmed in central Manzini region. Approximately 45 cattle affected with typical FMD symptoms including fever, blisters on tongue and hooves.',
        'status': 'active',
        'region': 'manzini',
        'latitude': -26.4833,
        'longitude': 31.3667,
        'location_name': 'Manzini Central Farm',
        'animals_affected': 45,
        'animals_quarantined': 120,
        'date_reported': timezone.now() - timedelta(days=5),
        'date_confirmed': timezone.now() - timedelta(days=3),
        'source': 'Ministry of Agriculture',
        'is_verified': True,
        'is_active': True,
    },
    {
        'title': 'Hhohho Border Area - Surveillance',
        'description': 'Surveillance zone established near northern border after neighboring country reported FMD cases. No confirmed cases in Eswatini yet, but heightened monitoring is in place.',
        'status': 'surveillance',
        'region': 'hhohho',
        'latitude': -26.1833,
        'longitude': 31.1333,
        'location_name': 'Hhohho Border District',
        'animals_affected': 0,
        'animals_quarantined': 250,
        'date_reported': timezone.now() - timedelta(days=10),
        'source': 'Border Veterinary Services',
        'is_verified': True,
        'is_active': True,
    },
    {
        'title': 'Lubombo Region - Cleared',
        'description': 'Previously affected area in Lubombo has been declared FMD-free after 60 days of monitoring. All restrictions have been lifted.',
        'status': 'cleared',
        'region': 'lubombo',
        'latitude': -26.2000,
        'longitude': 31.9000,
        'location_name': 'Lubombo District',
        'animals_affected': 32,
        'animals_quarantined': 85,
        'date_reported': timezone.now() - timedelta(days=90),
        'date_confirmed': timezone.now() - timedelta(days=88),
        'date_cleared': timezone.now() - timedelta(days=5),
        'source': 'Regional Veterinary Office',
        'is_verified': True,
        'is_active': True,
    },
    {
        'title': 'Shiselweni Small-Scale Farm',
        'description': 'Small outbreak detected on a family farm in Shiselweni. Quick response and isolation prevented spread to neighboring farms.',
        'status': 'surveillance',
        'region': 'shiselweni',
        'latitude': -27.0167,
        'longitude': 31.4167,
        'location_name': 'Shiselweni Family Farm',
        'animals_affected': 8,
        'animals_quarantined': 25,
        'date_reported': timezone.now() - timedelta(days=15),
        'date_confirmed': timezone.now() - timedelta(days=12),
        'source': 'District Veterinary Officer',
        'is_verified': True,
        'is_active': True,
    },
]

print("Creating outbreaks...")
for data in outbreaks_data:
    outbreak, created = Outbreak.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        print(f"  ✓ Created: {outbreak.title}")
    else:
        print(f"  - Already exists: {outbreak.title}")

# Sample Updates
updates_data = [
    {
        'title': 'New FMD Prevention Guidelines Released',
        'content': '''The Ministry of Agriculture has released comprehensive new biosecurity guidelines to help farmers prevent FMD outbreaks. 

Key measures include:
- Enhanced farm biosecurity protocols
- Mandatory visitor registration
- Vehicle disinfection at farm gates
- Isolation periods for new animals
- Regular health monitoring schedules

All farmers are encouraged to implement these measures immediately. Training sessions will be conducted in all regions over the next month.

For more information, contact your regional veterinary office or visit the Ministry website.''',
        'update_type': 'guideline',
        'published_at': timezone.now() - timedelta(days=3),
        'source': 'Ministry of Agriculture',
        'is_published': True,
        'is_featured': True,
    },
    {
        'title': 'Vaccination Campaign Scheduled for March',
        'content': '''A nationwide FMD vaccination campaign will be conducted throughout March 2024. All cattle, pigs, sheep, and goats in designated zones must be vaccinated.

Campaign Details:
- Dates: March 1-31, 2024
- Coverage: All four regions
- Cost: Free for farmers
- Required documents: Animal identification records

Mobile vaccination teams will visit all districts. Farmers should ensure their animals are properly identified and records are up to date.

Contact your local veterinary office to schedule your farm visit.''',
        'update_type': 'announcement',
        'published_at': timezone.now() - timedelta(days=7),
        'source': 'Veterinary Services Department',
        'is_published': True,
        'is_featured': True,
    },
    {
        'title': 'FMD Alert: Increased Vigilance Required',
        'content': '''Following confirmed FMD cases in neighboring regions, all farmers and livestock owners are urged to increase vigilance and implement strict biosecurity measures.

Immediate Actions:
1. Inspect animals daily for FMD symptoms
2. Restrict farm visitors
3. Disinfect all vehicles entering farms
4. Report any suspicious symptoms immediately

Emergency Hotline: +268 7600 0000 (24/7)

Early detection is crucial for effective outbreak control. Do not wait if you observe any unusual symptoms in your animals.''',
        'update_type': 'alert',
        'published_at': timezone.now() - timedelta(days=1),
        'source': 'Emergency Response Team',
        'is_published': True,
        'is_featured': True,
    },
    {
        'title': 'Farmer Training Sessions Announced',
        'content': '''Free FMD awareness and management training sessions will be held in all regions during February.

Training will cover:
- FMD identification and symptoms
- Biosecurity best practices
- Emergency response procedures
- Proper reporting protocols
- Vaccination requirements

Sessions are free and open to all farmers, farm workers, and livestock owners. Certificate of attendance will be provided.

Register at your local agricultural office or call +268 2404 2731.''',
        'update_type': 'news',
        'published_at': timezone.now() - timedelta(days=12),
        'source': 'Agricultural Extension Services',
        'is_published': True,
        'is_featured': False,
    },
    {
        'title': 'Movement Restrictions Updated',
        'content': '''Updated animal movement regulations are now in effect for areas under FMD surveillance.

New Regulations:
- Movement permits required for all livestock
- 21-day quarantine for animals entering surveillance zones
- Health certificates must be recent (within 7 days)
- Vehicle disinfection mandatory at checkpoints

These measures are temporary and will be reviewed monthly based on the disease situation.

For permit applications, visit your nearest veterinary office with proper documentation.''',
        'update_type': 'announcement',
        'published_at': timezone.now() - timedelta(days=20),
        'source': 'Ministry of Agriculture',
        'is_published': True,
        'is_featured': False,
    },
]

print("\nCreating updates...")
for data in updates_data:
    update, created = Update.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        print(f"  ✓ Created: {update.title}")
    else:
        print(f"  - Already exists: {update.title}")

# Sample Dip Tanks
diptanks_data = [
    {
        'name': 'Manzini Central Dip Tank',
        'region': 'manzini',
        'latitude': -26.4900,
        'longitude': 31.3700,
        'is_affected': True,  # Affected area
        'capacity': 500,
        'last_inspection': timezone.now() - timedelta(days=2),
        'notes': 'Main dip tank serving central Manzini farms. Currently affected due to nearby outbreak.',
    },
    {
        'name': 'Hhohho Border Dip Tank',
        'region': 'hhohho',
        'latitude': -26.1900,
        'longitude': 31.1400,
        'is_affected': True,  # Affected area
        'capacity': 300,
        'last_inspection': timezone.now() - timedelta(days=5),
        'notes': 'Border area dip tank under surveillance due to neighboring country cases.',
    },
    {
        'name': 'Lubombo East Dip Tank',
        'region': 'lubombo',
        'latitude': -26.2100,
        'longitude': 31.9100,
        'is_affected': False,  # Clear area
        'capacity': 400,
        'last_inspection': timezone.now() - timedelta(days=1),
        'notes': 'Recently cleared area, all restrictions lifted.',
    },
    {
        'name': 'Shiselweni South Dip Tank',
        'region': 'shiselweni',
        'latitude': -27.0200,
        'longitude': 31.4200,
        'is_affected': True,  # Affected area
        'capacity': 250,
        'last_inspection': timezone.now() - timedelta(days=3),
        'notes': 'Small farm area under surveillance after recent detection.',
    },
    {
        'name': 'Manzini West Dip Tank',
        'region': 'manzini',
        'latitude': -26.5000,
        'longitude': 31.2500,
        'is_affected': False,  # Clear area
        'capacity': 350,
        'last_inspection': timezone.now() - timedelta(days=1),
        'notes': 'Clear area with good biosecurity measures in place.',
    },
    {
        'name': 'Hhohho Central Dip Tank',
        'region': 'hhohho',
        'latitude': -26.3000,
        'longitude': 31.2000,
        'is_affected': False,  # Clear area
        'capacity': 450,
        'last_inspection': timezone.now() - timedelta(days=2),
        'notes': 'Central location serving multiple farms, currently clear.',
    },
]

print("\nCreating dip tanks...")
for data in diptanks_data:
    dip_tank, created = DipTank.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        status = "Affected" if dip_tank.is_affected else "Clear"
        print(f"  ✓ Created: {dip_tank.name} - {status}")
    else:
        print(f"  - Already exists: {dip_tank.name}")

# Sample Cordon Lines
cordon_lines_data = [
    {
        'name': 'Manzini Central Cordon Line',
        'region': 'manzini',
        'status': 'active',
        'coordinates': [
            {"lat": -26.4700, "lng": 31.3500},
            {"lat": -26.4800, "lng": 31.3600},
            {"lat": -26.4900, "lng": 31.3700},
            {"lat": -26.5000, "lng": 31.3800},
        ],
        'description': 'Primary cordon line around Manzini Central outbreak area to control cattle movement.',
        'restrictions': 'No cattle movement across this line without permits. All vehicles must be disinfected at checkpoints.',
        'date_established': timezone.now() - timedelta(days=4),
    },
    {
        'name': 'Hhohho Border Control Line',
        'region': 'hhohho',
        'status': 'active',
        'coordinates': [
            {"lat": -26.1700, "lng": 31.1200},
            {"lat": -26.1800, "lng": 31.1300},
            {"lat": -26.1900, "lng": 31.1400},
            {"lat": -26.2000, "lng": 31.1500},
        ],
        'description': 'Border surveillance cordon line to prevent cross-border FMD transmission.',
        'restrictions': 'Enhanced screening for all livestock and livestock products. 48-hour quarantine for animals crossing.',
        'date_established': timezone.now() - timedelta(days=8),
    },
    {
        'name': 'Shiselweni Farm Isolation Line',
        'region': 'shiselweni',
        'status': 'active',
        'coordinates': [
            {"lat": -27.0000, "lng": 31.4000},
            {"lat": -27.0100, "lng": 31.4100},
            {"lat": -27.0200, "lng": 31.4200},
            {"lat": -27.0300, "lng": 31.4300},
        ],
        'description': 'Isolation cordon around affected farm in Shiselweni to prevent local spread.',
        'restrictions': 'Complete livestock movement ban within 2km radius. Farm access restricted to authorized personnel only.',
        'date_established': timezone.now() - timedelta(days=12),
    },
    {
        'name': 'Lubombo Cleared Zone Boundary',
        'region': 'lubombo',
        'status': 'inactive',
        'coordinates': [
            {"lat": -26.1800, "lng": 31.8800},
            {"lat": -26.1900, "lng": 31.8900},
            {"lat": -26.2000, "lng": 31.9000},
            {"lat": -26.2100, "lng": 31.9100},
        ],
        'description': 'Former cordon line around Lubombo area, now deactivated after area was cleared.',
        'restrictions': 'No longer active - area has been declared FMD-free.',
        'date_established': timezone.now() - timedelta(days=85),
        'date_expires': timezone.now() - timedelta(days=5),
    },
]

print("\nCreating cordon lines...")
for data in cordon_lines_data:
    cordon_line, created = CordonLine.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        print(f"  ✓ Created: {cordon_line.name} - {cordon_line.get_status_display()}")
    else:
        print(f"  - Already exists: {cordon_line.name}")

# Sample Foot Wash Stations
footwash_stations_data = [
    {
        'name': 'Manzini Highway Station',
        'region': 'manzini',
        'road_name': 'MR3 Highway',
        'road_type': 'highway',
        'latitude': -26.4600,
        'longitude': 31.3400,
        'instructions': '''MANDATORY FOOT WASH PROCEDURE:
1. Stop vehicle at designated area
2. All passengers must exit vehicle
3. Step into disinfectant foot bath (30 seconds minimum)
4. Spray vehicle tires and undercarriage
5. Present livestock movement permits if carrying animals
6. Wait for clearance from station officer

DISINFECTANT: 2% Virkon S solution, changed every 4 hours''',
        'operating_hours': '24/7',
        'contact_person': 'Officer Dlamini',
        'contact_phone': '+268 7601 2345',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=1),
    },
    {
        'name': 'Hhohho Border Checkpoint',
        'region': 'hhohho',
        'road_name': 'Border Road A1',
        'road_type': 'border_crossing',
        'latitude': -26.1600,
        'longitude': 31.1100,
        'instructions': '''BORDER CROSSING PROTOCOL:
1. Present passport and vehicle documents
2. Declare any livestock or animal products
3. Mandatory foot wash for all persons
4. Vehicle disinfection (wheels, floor mats, cargo area)
5. Health certificate inspection for animals
6. 15-minute waiting period for disinfectant to work

SPECIAL REQUIREMENTS: International travelers must complete FMD declaration form''',
        'operating_hours': '06:00 - 22:00',
        'contact_person': 'Border Control Unit',
        'contact_phone': '+268 7602 3456',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=3),
    },
    {
        'name': 'Shiselweni Farm Access Point',
        'region': 'shiselweni',
        'road_name': 'Farm Access Road',
        'road_type': 'secondary_road',
        'latitude': -26.9900,
        'longitude': 31.3900,
        'instructions': '''FARM AREA ACCESS CONTROL:
1. Authorized personnel only beyond this point
2. Complete foot wash procedure (minimum 1 minute)
3. Change into provided protective clothing
4. Disinfect all equipment and tools
5. Log entry time and purpose of visit
6. Follow designated routes only

EMERGENCY CONTACT: District Veterinary Officer''',
        'operating_hours': '07:00 - 17:00',
        'contact_person': 'Farm Security',
        'contact_phone': '+268 7603 4567',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=2),
    },
    {
        'name': 'Lubombo Main Road Station',
        'region': 'lubombo',
        'road_name': 'MR8 Main Road',
        'road_type': 'main_road',
        'latitude': -26.2200,
        'longitude': 31.9200,
        'instructions': '''STANDARD DISINFECTION PROCEDURE:
1. Reduce speed and stop at station
2. All occupants step into foot wash basin
3. Spray vehicle exterior focusing on tires
4. Present movement permits if transporting livestock
5. Allow 5-minute drying time
6. Proceed when cleared by officer

NOTE: This area has been cleared but precautionary measures remain in place''',
        'operating_hours': '06:00 - 18:00',
        'contact_person': 'Officer Nkambule',
        'contact_phone': '+268 7604 5678',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=1),
    },
    {
        'name': 'Manzini West Checkpoint',
        'region': 'manzini',
        'road_name': 'MR5 Secondary Road',
        'road_type': 'secondary_road',
        'latitude': -26.5100,
        'longitude': 31.2400,
        'instructions': '''SECONDARY ROAD CHECKPOINT:
1. Mandatory stop for all vehicles
2. Quick foot wash (30 seconds minimum)
3. Vehicle tire spray
4. Brief health questionnaire
5. Temperature check for livestock if present
6. Continue with caution

ADVISORY: Avoid unnecessary travel through affected areas''',
        'operating_hours': '08:00 - 16:00',
        'contact_person': 'Checkpoint Team',
        'contact_phone': '+268 7605 6789',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=4),
    },
    {
        'name': 'Hhohho Central Station',
        'region': 'hhohho',
        'road_name': 'MR1 Main Road',
        'road_type': 'main_road',
        'latitude': -26.3100,
        'longitude': 31.2100,
        'instructions': '''PREVENTIVE DISINFECTION STATION:
1. Voluntary but recommended stop
2. Step into disinfectant solution
3. Spray footwear and vehicle tires
4. Take information leaflet on FMD prevention
5. Report any suspicious animal symptoms
6. Continue journey

INFORMATION: This is a clear area - station operates for prevention only''',
        'operating_hours': '07:00 - 19:00',
        'contact_person': 'Prevention Team',
        'contact_phone': '+268 7606 7890',
        'is_operational': True,
        'last_maintenance': timezone.now() - timedelta(days=2),
    },
]

print("\nCreating foot wash stations...")
for data in footwash_stations_data:
    station, created = FootWashStation.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        status = "Operational" if station.is_operational else "Not Operational"
        print(f"  ✓ Created: {station.name} - {status}")
    else:
        print(f"  - Already exists: {station.name}")

print("\n" + "="*50)
print("Sample data loading complete!")
print("="*50)
print(f"\nCreated:")
print(f"  - {Outbreak.objects.count()} outbreaks")
print(f"  - {Update.objects.count()} updates")
print(f"  - {DipTank.objects.count()} dip tanks")
print(f"  - {DipTank.objects.filter(is_affected=True).count()} affected dip tank areas")
print(f"  - {CordonLine.objects.count()} cordon lines")
print(f"  - {CordonLine.objects.filter(status='active').count()} active cordon lines")
print(f"  - {FootWashStation.objects.count()} foot wash stations")
print(f"  - {FootWashStation.objects.filter(is_operational=True).count()} operational stations")
print("\nYou can now:")
print("  1. Visit http://127.0.0.1:8000/ to see the map with all features")
print("  2. Visit http://127.0.0.1:8000/admin/ to manage data")
print("  3. Visit http://127.0.0.1:8000/api/outbreaks/ to test the API")
print("  4. Visit http://127.0.0.1:8000/api/diptanks/ to see dip tank data")
print("  5. Visit http://127.0.0.1:8000/api/cordon-lines/ to see cordon line data")
print("  6. Visit http://127.0.0.1:8000/api/footwash-stations/ to see station data")
print("\nThe map uses OpenStreetMap tiles and doesn't require any API keys!")
print("\nNew Features Added:")
print("  • Cordon lines showing movement control boundaries")
print("  • Foot wash stations with detailed procedures")
print("  • Enhanced outbreak control visualization")