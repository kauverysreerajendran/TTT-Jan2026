#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

# Total batches
total = ModelMasterCreation.objects.count()
print(f"Total ModelMasterCreation records: {total}")

# Moved_to_D_Picker = True
dp = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True).count()
print(f"Moved_to_D_Picker=True: {dp}")

# Draft_Saved = True
drafted = ModelMasterCreation.objects.filter(Draft_Saved=True).count()
print(f"Draft_Saved=True: {drafted}")

# release_lot = True
released = ModelMasterCreation.objects.filter(release_lot=True).count()
print(f"release_lot=True: {released}")

# Yet to start (Moved_to_D_Picker=True but Draft_Saved=False)
yet_to_start = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True, Draft_Saved=False).count()
print(f"Yet to Start (Moved_to_D_Picker=True, Draft_Saved=False): {yet_to_start}")

# For Day Planning (Moved_to_D_Picker=True)
dp_total = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True).count()
dp_drafted = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True, Draft_Saved=True).count()
dp_released = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True, release_lot=True).count()
dp_yet_to_start = ModelMasterCreation.objects.filter(Moved_to_D_Picker=True, Draft_Saved=False).count()

print(f"\nDay Planning Module:")
print(f"  Total Lots (Moved_to_D_Picker=True): {dp_total}")
print(f"  Yet to Start: {dp_yet_to_start}")
print(f"  Drafted: {dp_drafted}")
print(f"  Released/Processed: {dp_released}")
print(f"  In Progress: {dp_total - dp_released}")

if dp_total > 0:
    print(f"\nPercentages:")
    print(f"  Yet to Start: {int((dp_yet_to_start / dp_total) * 100)}%")
    print(f"  Drafted: {int((dp_drafted / dp_total) * 100)}%")
    print(f"  Released: {int((dp_released / dp_total) * 100)}%")
    print(f"  In Progress: {int(((dp_total - dp_released) / dp_total) * 100)}%")
