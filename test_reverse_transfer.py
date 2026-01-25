#!/usr/bin/env python3
"""
Quick test script to verify the reverse transfer functionality.
This script can be run to test the new send_brass_audit_back_to_brass_qc function.
"""

import os
import sys
import django
from django.contrib.auth.models import User

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import TotalStockModel
from Brass_QC.models import BrassTrayId
from BrassAudit.models import BrassAuditTrayId
from Brass_QC.views import send_brass_audit_back_to_brass_qc

def test_reverse_transfer():
    """
    Test the reverse transfer function with a sample lot.
    """
    print("🧪 [TEST] Testing reverse transfer functionality...")
    
    # Find a test lot that has brass audit rejection
    test_lots = TotalStockModel.objects.filter(
        brass_audit_rejection=True,
        send_brass_audit_to_qc=True
    ).order_by('-id')[:1]
    
    if not test_lots.exists():
        print("❌ [TEST] No test lots found with brass_audit_rejection=True and send_brass_audit_to_qc=True")
        print("   Please create test data or run this on a lot that has been rejected in Brass Audit")
        return False
    
    test_lot = test_lots.first()
    lot_id = test_lot.lot_id
    
    print(f"📦 [TEST] Testing with lot_id: {lot_id}")
    
    # Get a test user
    test_user = User.objects.filter(is_active=True).first()
    if not test_user:
        print("❌ [TEST] No active users found")
        return False
    
    print(f"👤 [TEST] Using test user: {test_user.username}")
    
    # Show before state
    print("\n📊 [TEST] BEFORE state:")
    print(f"   TotalStockModel flags: brass_audit_rejection={test_lot.brass_audit_rejection}, send_brass_audit_to_qc={test_lot.send_brass_audit_to_qc}")
    
    brass_trays_before = BrassTrayId.objects.filter(lot_id=lot_id).count()
    audit_trays_before = BrassAuditTrayId.objects.filter(lot_id=lot_id).count()
    print(f"   BrassTrayId records: {brass_trays_before}")
    print(f"   BrassAuditTrayId records: {audit_trays_before}")
    
    # Test the reverse transfer function
    print("\n🔄 [TEST] Running reverse transfer...")
    result = send_brass_audit_back_to_brass_qc(lot_id, test_user)
    
    # Refresh the lot data
    test_lot.refresh_from_db()
    
    # Show after state
    print("\n📊 [TEST] AFTER state:")
    print(f"   TotalStockModel flags: brass_audit_rejection={test_lot.brass_audit_rejection}, send_brass_audit_to_qc={test_lot.send_brass_audit_to_qc}")
    
    brass_trays_after = BrassTrayId.objects.filter(lot_id=lot_id).count()
    audit_trays_after = BrassAuditTrayId.objects.filter(lot_id=lot_id).count()
    print(f"   BrassTrayId records: {brass_trays_after}")
    print(f"   BrassAuditTrayId records: {audit_trays_after}")
    
    # Check results
    print(f"\n✅ [TEST] Reverse transfer function returned: {result}")
    
    if result:
        print("✅ [TEST] SUCCESS: Reverse transfer completed")
        
        # Verify expected changes
        if audit_trays_after == 0:
            print("✅ [TEST] VERIFIED: Brass Audit tray records cleared")
        else:
            print(f"⚠️ [TEST] WARNING: Expected 0 Brass Audit trays, found {audit_trays_after}")
            
        if brass_trays_after > 0:
            print(f"✅ [TEST] VERIFIED: Brass QC tray records exist ({brass_trays_after})")
            
            # Check top tray
            top_tray = BrassTrayId.objects.filter(lot_id=lot_id, top_tray=True).first()
            if top_tray:
                print(f"✅ [TEST] VERIFIED: Top tray found: {top_tray.tray_id} (qty: {top_tray.tray_quantity})")
            else:
                print("⚠️ [TEST] WARNING: No top tray found")
        else:
            print("⚠️ [TEST] WARNING: No Brass QC tray records found")
            
        if not test_lot.send_brass_audit_to_qc:
            print("✅ [TEST] VERIFIED: send_brass_audit_to_qc flag reset")
        else:
            print("⚠️ [TEST] WARNING: send_brass_audit_to_qc flag still True")
            
    else:
        print("❌ [TEST] FAILED: Reverse transfer returned False")
    
    return result

if __name__ == "__main__":
    try:
        test_reverse_transfer()
    except Exception as e:
        print(f"❌ [TEST] Error running test: {e}")
        import traceback
        traceback.print_exc()