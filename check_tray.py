import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from Jig_Loading.models import JigLoadTrayId
from modelmasterapp.models import TrayId

print('Checking JB-A00100 in JigLoadTrayId:')
tray = JigLoadTrayId.objects.filter(tray_id='JB-A00100').first()
print(f'Found: {tray}')
if tray:
    print(f'Delink status: {tray.delink_tray}')
    print(f'Lot ID: {tray.lot_id}')
else:
    print('Tray not found in JigLoadTrayId')

print('\nChecking JB-A00100 in TrayId:')
tray_master = TrayId.objects.filter(tray_id='JB-A00100').first()
print(f'Found: {tray_master}')
if tray_master:
    print(f'Delink status: {tray_master.delink_tray}')
    print(f'Lot ID: {tray_master.lot_id}')
else:
    print('Tray not found in TrayId')