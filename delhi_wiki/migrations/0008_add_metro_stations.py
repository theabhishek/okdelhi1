from django.db import migrations
from django.utils.text import slugify

def add_metro_stations(apps, schema_editor):
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')

    # Create or get metro lines
    lines = {
        'Red Line': {
            'color': '#FF0000',
            'stations': [
                'Rithala', 'Rohini West', 'Rohini East', 'Pitampura', 'Kohat Enclave',
                'Netaji Subhash Place', 'Keshav Puram', 'Kanhaiya Nagar', 'Inderlok',
                'Shastri Nagar', 'Pratap Nagar', 'Pul Bangash', 'Tis Hazari', 'Kashmere Gate',
                'Shastri Park', 'Seelampur', 'Welcome', 'Shahdara', 'Mansarovar Park',
                'Jhilmil', 'Dilshad Garden', 'Shaheed Nagar', 'Raj Bagh', 'Rajiv Nagar',
                'Shyam Park', 'Mohan Nagar', 'Arthala', 'Hindon River', 'Shaheed Sthal'
            ]
        },
        'Yellow Line': {
            'color': '#FFFF00',
            'stations': [
                'Samaypur Badli', 'Rohini Sector 18,19', 'Haiderpur Badli Mor',
                'Jahangirpuri', 'Adarsh Nagar', 'Azadpur', 'Model Town', 'Guru Teg Bahadur Nagar',
                'Vishwavidyalaya', 'Vidhan Sabha', 'Civil Lines', 'Kashmere Gate', 'Chandni Chowk',
                'Chawri Bazar', 'New Delhi', 'Rajiv Chowk', 'Patel Chowk', 'Central Secretariat',
                'Udyog Bhawan', 'Lok Kalyan Marg', 'Jor Bagh', 'INA', 'AIIMS', 'Green Park',
                'Hauz Khas', 'Malviya Nagar', 'Saket', 'Qutab Minar', 'Chhatarpur',
                'Sultanpur', 'Ghitorni', 'Arjan Garh', 'Guru Dronacharya', 'Sikandarpur',
                'MG Road', 'IFFCO Chowk', 'Huda City Centre'
            ]
        },
        'Blue Line': {
            'color': '#0000FF',
            'stations': [
                'Dwarka Sector 21', 'Dwarka Sector 8', 'Dwarka Sector 9', 'Dwarka Sector 10',
                'Dwarka Sector 11', 'Dwarka Sector 12', 'Dwarka Sector 13', 'Dwarka Sector 14',
                'Dwarka', 'Dwarka Mor', 'Nawada', 'Uttam Nagar West', 'Uttam Nagar East',
                'Janakpuri West', 'Janakpuri East', 'Tilak Nagar', 'Subhash Nagar', 'Tagore Garden',
                'Rajouri Garden', 'Ramesh Nagar', 'Moti Nagar', 'Kirti Nagar', 'Shadipur',
                'Patel Nagar', 'Rajendra Place', 'Karol Bagh', 'Jhandewalan', 'RK Ashram Marg',
                'Rajiv Chowk', 'Barakhamba Road', 'Mandi House', 'Supreme Court', 'Indraprastha',
                'Yamuna Bank', 'Akshardham', 'Mayur Vihar Phase-1', 'Mayur Vihar Extension',
                'New Ashok Nagar', 'Noida Sector 15', 'Noida Sector 16', 'Noida Sector 18',
                'Botanical Garden', 'Golf Course', 'Noida City Centre', 'Noida Sector 34',
                'Noida Sector 52', 'Noida Sector 61', 'Noida Sector 59', 'Noida Sector 62',
                'Noida Electronic City'
            ]
        },
        'Green Line': {
            'color': '#008000',
            'stations': [
                'Inderlok', 'Ashok Park Main', 'Punjabi Bagh', 'Shivaji Park', 'Madipur',
                'Paschim Vihar East', 'Paschim Vihar West', 'Peera Garhi', 'Udyog Nagar',
                'Surajmal Stadium', 'Nangloi', 'Nangloi Railway Station', 'Rajdhani Park',
                'Mundka', 'Mundka Industrial Area', 'Ghevra', 'Tikri Kalan', 'Tikri Border',
                'Pandit Shree Ram Sharma', 'Bahadurgarh City', 'Brigadier Hoshiyar Singh'
            ]
        },
        'Violet Line': {
            'color': '#800080',
            'stations': [
                'Kashmere Gate', 'Lal Quila', 'Jama Masjid', 'Delhi Gate', 'ITO',
                'Mandi House', 'Janpath', 'Central Secretariat', 'Khan Market', 'Jawaharlal Nehru Stadium',
                'Jangpura', 'Lajpat Nagar', 'Moolchand', 'Kailash Colony', 'Nehru Place',
                'Kalkaji Mandir', 'Govind Puri', 'Harkesh Nagar', 'Jasola Apollo', 'Sarita Vihar',
                'Mohan Estate', 'Tughlakabad', 'Badarpur', 'Sarai', 'NHPC Chowk', 'Mewala Maharajpur',
                'Sector 28 Faridabad', 'Badkal Mor', 'Old Faridabad', 'Neelam Chowk Ajronda',
                'Bata Chowk', 'Escorts Mujesar', 'Sant Surdas', 'Raja Nahar Singh'
            ]
        },
        'Pink Line': {
            'color': '#FFC0CB',
            'stations': [
                'Majlis Park', 'Azadpur', 'Shalimar Bagh', 'Netaji Subhash Place',
                'Shakurpur', 'Punjabi Bagh West', 'ESI Hospital', 'Rajouri Garden',
                'Maya Puri', 'Naraina Vihar', 'Delhi Cantonment', 'Durgabai Deshmukh South Campus',
                'Sir Vishweshwaraiah Moti Bagh', 'Bhikaji Cama Place', 'Sarojini Nagar',
                'INA', 'South Extension', 'Lajpat Nagar', 'Vinobapuri', 'Ashram',
                'Hazrat Nizamuddin', 'Mayur Vihar Phase-1', 'Mayur Vihar Pocket 1',
                'Trilokpuri Sanjay Lake', 'East Vinod Nagar', 'Mandawali West Vinod Nagar',
                'IP Extension', 'Anand Vihar', 'Karkarduma', 'Karkarduma Court',
                'Krishna Nagar', 'East Azad Nagar', 'Welcome', 'Jaffrabad',
                'Maujpur', 'Gokulpuri', 'Johri Enclave', 'Shiv Vihar'
            ]
        },
        'Magenta Line': {
            'color': '#FF00FF',
            'stations': [
                'Janakpuri West', 'Dabri Mor', 'Dashrath Puri', 'Palam', 'Sadar Bazaar Cantonment',
                'Terminal 1-IGI Airport', 'Shankar Vihar', 'Vasant Vihar', 'Munirka',
                'RK Puram', 'IIT Delhi', 'Hauz Khas', 'Panchsheel Park', 'Chirag Delhi',
                'Greater Kailash', 'Nehru Enclave', 'Kalkaji Mandir', 'Okhla NSIC',
                'Sukhdev Vihar', 'Jamia Millia Islamia', 'Okhla Vihar', 'Jasola Vihar Shaheen Bagh',
                'Kalindi Kunj', 'Okhla Bird Sanctuary', 'Botanical Garden'
            ]
        },
        'Grey Line': {
            'color': '#808080',
            'stations': [
                'Dwarka', 'Nangli', 'Najafgarh', 'Dhansa Bus Stand'
            ]
        },
        'Rapid Metro': {
            'color': '#FFA500',
            'stations': [
                'Sector 55-56', 'Sector 54 Chowk', 'Sector 53-54', 'Sector 42-43',
                'Phase 1', 'Sikanderpur', 'Phase 2', 'Belvedere Towers', 'Cyber City',
                'Phase 3'
            ]
        },
        'Aqua Line': {
            'color': '#00FFFF',
            'stations': [
                'Noida Sector 51', 'Noida Sector 50', 'Noida Sector 76', 'Noida Sector 101',
                'Noida Sector 81', 'NSEZ', 'Noida Sector 83', 'Noida Sector 137',
                'Noida Sector 142', 'Noida Sector 143', 'Noida Sector 144', 'Noida Sector 145',
                'Noida Sector 146', 'Noida Sector 147', 'Noida Sector 148', 'Knowledge Park II',
                'Pari Chowk', 'Alpha 1', 'Delta 1', 'GNIDA Office', 'Depot'
            ]
        }
    }

    # Create lines and stations
    for line_name, line_data in lines.items():
        line, _ = MetroLine.objects.get_or_create(
            name=line_name,
            defaults={
                'color': line_data['color'],
                'slug': slugify(line_name)
            }
        )

        # Create stations for this line
        for station_name in line_data['stations']:
            base_slug = slugify(station_name)
            counter = 1
            while True:
                try:
                    station, created = MetroStation.objects.get_or_create(
                        name=station_name,
                        defaults={
                            'slug': base_slug if counter == 1 else f"{base_slug}-{counter}",
                            'latitude': 28.6667,  # Default latitude
                            'longitude': 77.3167,  # Default longitude
                            'is_interchange': station_name in ['Kashmere Gate', 'Rajiv Chowk', 'Central Secretariat', 'Mandi House', 'INA', 'Hauz Khas', 'Kalkaji Mandir', 'Botanical Garden', 'Welcome', 'Inderlok', 'Netaji Subhash Place']
                        }
                    )
                    station.lines.add(line)
                    break
                except Exception:
                    counter += 1
                    if counter > 100:  # Safety limit
                        raise

def remove_metro_stations(apps, schema_editor):
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    MetroStation.objects.all().delete()
    MetroLine.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('delhi_wiki', '0007_add_metro_data'),
    ]

    operations = [
        migrations.RunPython(add_metro_stations, remove_metro_stations),
    ] 