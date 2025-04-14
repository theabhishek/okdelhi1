from django.db import migrations
from django.utils.text import slugify

def add_metro_data(apps, schema_editor):
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')

    # Create Metro Lines
    lines = [
        {'name': 'Red Line', 'color': '#FF0000', 'description': 'Dilshad Garden to Rithala'},
        {'name': 'Yellow Line', 'color': '#FFFF00', 'description': 'Samaypur Badli to HUDA City Centre'},
        {'name': 'Blue Line', 'color': '#0000FF', 'description': 'Dwarka Sector 21 to Noida Electronic City'},
        {'name': 'Green Line', 'color': '#008000', 'description': 'Inderlok to Brigadier Hoshiar Singh'},
        {'name': 'Violet Line', 'color': '#800080', 'description': 'Kashmere Gate to Raja Nahar Singh'},
        {'name': 'Pink Line', 'color': '#FFC0CB', 'description': 'Majlis Park to Shiv Vihar'},
        {'name': 'Magenta Line', 'color': '#FF00FF', 'description': 'Janakpuri West to Botanical Garden'},
        {'name': 'Grey Line', 'color': '#808080', 'description': 'Dwarka to Najafgarh'},
        {'name': 'Orange Line', 'color': '#FFA500', 'description': 'New Delhi to Dwarka Sector 21'},
        {'name': 'Rapid Metro', 'color': '#00FF00', 'description': 'Sector 55-56 to Phase 3'},
    ]

    metro_lines = {}
    for line_data in lines:
        line = MetroLine.objects.create(
            name=line_data['name'],
            color=line_data['color'],
            description=line_data['description'],
            slug=slugify(line_data['name'])
        )
        metro_lines[line_data['name']] = line

    # Create Metro Stations
    stations = [
        # Red Line
        {'name': 'Dilshad Garden', 'lines': ['Red Line'], 'latitude': 28.6705, 'longitude': 77.3189},
        {'name': 'Jhilmil', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Mansarovar Park', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Shahdara', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Welcome', 'lines': ['Red Line', 'Pink Line'], 'latitude': 28.6667, 'longitude': 77.3167, 'is_interchange': True},
        {'name': 'Seelampur', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Shastri Park', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Kashmere Gate', 'lines': ['Red Line', 'Yellow Line', 'Violet Line'], 'latitude': 28.6667, 'longitude': 77.3167, 'is_interchange': True},
        {'name': 'Tis Hazari', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Pul Bangash', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Pratap Nagar', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Shastri Nagar', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Inderlok', 'lines': ['Red Line', 'Green Line'], 'latitude': 28.6667, 'longitude': 77.3167, 'is_interchange': True},
        {'name': 'Kanhaiya Nagar', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Keshav Puram', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Netaji Subhash Place', 'lines': ['Red Line', 'Pink Line'], 'latitude': 28.6667, 'longitude': 77.3167, 'is_interchange': True},
        {'name': 'Kohat Enclave', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Pitampura', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Rohini East', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Rohini West', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},
        {'name': 'Rithala', 'lines': ['Red Line'], 'latitude': 28.6667, 'longitude': 77.3167},

        # Yellow Line
        {'name': 'Samaypur Badli', 'lines': ['Yellow Line'], 'latitude': 28.7485, 'longitude': 77.1714},
        {'name': 'Rohini Sector 18,19', 'lines': ['Yellow Line'], 'latitude': 28.7397, 'longitude': 77.1714},
        {'name': 'Haiderpur Badli Mor', 'lines': ['Yellow Line'], 'latitude': 28.7309, 'longitude': 77.1714},
        {'name': 'Jahangirpuri', 'lines': ['Yellow Line'], 'latitude': 28.7251, 'longitude': 77.1714},
        {'name': 'Adarsh Nagar', 'lines': ['Yellow Line'], 'latitude': 28.7164, 'longitude': 77.1714},
        {'name': 'Azadpur', 'lines': ['Yellow Line', 'Pink Line'], 'latitude': 28.7076, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'Model Town', 'lines': ['Yellow Line'], 'latitude': 28.6988, 'longitude': 77.1714},
        {'name': 'GTB Nagar', 'lines': ['Yellow Line'], 'latitude': 28.6901, 'longitude': 77.1714},
        {'name': 'Vishwavidyalaya', 'lines': ['Yellow Line'], 'latitude': 28.6813, 'longitude': 77.1714},
        {'name': 'Vidhan Sabha', 'lines': ['Yellow Line'], 'latitude': 28.6726, 'longitude': 77.1714},
        {'name': 'Civil Lines', 'lines': ['Yellow Line'], 'latitude': 28.6638, 'longitude': 77.1714},
        {'name': 'Chandni Chowk', 'lines': ['Yellow Line'], 'latitude': 28.6551, 'longitude': 77.1714},
        {'name': 'Chawri Bazar', 'lines': ['Yellow Line'], 'latitude': 28.6463, 'longitude': 77.1714},
        {'name': 'New Delhi', 'lines': ['Yellow Line', 'Orange Line'], 'latitude': 28.6376, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'Rajiv Chowk', 'lines': ['Yellow Line', 'Blue Line'], 'latitude': 28.6288, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'Patel Chowk', 'lines': ['Yellow Line'], 'latitude': 28.6201, 'longitude': 77.1714},
        {'name': 'Central Secretariat', 'lines': ['Yellow Line', 'Violet Line'], 'latitude': 28.6113, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'Udyog Bhawan', 'lines': ['Yellow Line'], 'latitude': 28.6026, 'longitude': 77.1714},
        {'name': 'Lok Kalyan Marg', 'lines': ['Yellow Line'], 'latitude': 28.5938, 'longitude': 77.1714},
        {'name': 'Jor Bagh', 'lines': ['Yellow Line'], 'latitude': 28.5851, 'longitude': 77.1714},
        {'name': 'INA', 'lines': ['Yellow Line', 'Pink Line'], 'latitude': 28.5763, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'AIIMS', 'lines': ['Yellow Line'], 'latitude': 28.5676, 'longitude': 77.1714},
        {'name': 'Green Park', 'lines': ['Yellow Line'], 'latitude': 28.5588, 'longitude': 77.1714},
        {'name': 'Hauz Khas', 'lines': ['Yellow Line', 'Magenta Line'], 'latitude': 28.5501, 'longitude': 77.1714, 'is_interchange': True},
        {'name': 'Malviya Nagar', 'lines': ['Yellow Line'], 'latitude': 28.5413, 'longitude': 77.1714},
        {'name': 'Saket', 'lines': ['Yellow Line'], 'latitude': 28.5326, 'longitude': 77.1714},
        {'name': 'Qutab Minar', 'lines': ['Yellow Line'], 'latitude': 28.5238, 'longitude': 77.1714},
        {'name': 'Chhatarpur', 'lines': ['Yellow Line'], 'latitude': 28.5151, 'longitude': 77.1714},
        {'name': 'Sultanpur', 'lines': ['Yellow Line'], 'latitude': 28.5063, 'longitude': 77.1714},
        {'name': 'Ghitorni', 'lines': ['Yellow Line'], 'latitude': 28.4976, 'longitude': 77.1714},
        {'name': 'Arjan Garh', 'lines': ['Yellow Line'], 'latitude': 28.4888, 'longitude': 77.1714},
        {'name': 'Guru Dronacharya', 'lines': ['Yellow Line'], 'latitude': 28.4801, 'longitude': 77.1714},
        {'name': 'Sikandarpur', 'lines': ['Yellow Line'], 'latitude': 28.4713, 'longitude': 77.1714},
        {'name': 'MG Road', 'lines': ['Yellow Line'], 'latitude': 28.4626, 'longitude': 77.1714},
        {'name': 'IFFCO Chowk', 'lines': ['Yellow Line'], 'latitude': 28.4538, 'longitude': 77.1714},
        {'name': 'HUDA City Centre', 'lines': ['Yellow Line'], 'latitude': 28.4451, 'longitude': 77.1714},
    ]

    for station_data in stations:
        lines = station_data.pop('lines')
        station = MetroStation.objects.create(
            name=station_data['name'],
            slug=slugify(station_data['name']),
            latitude=station_data['latitude'],
            longitude=station_data['longitude'],
            is_interchange=station_data.get('is_interchange', False)
        )
        for line_name in lines:
            station.lines.add(metro_lines[line_name])

def remove_metro_data(apps, schema_editor):
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')
    
    MetroStation.objects.all().delete()
    MetroLine.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('delhi_wiki', '0006_metroroute_time_alter_metroroute_distance_and_more'),
    ]

    operations = [
        migrations.RunPython(add_metro_data, remove_metro_data),
    ] 