import os
import sys
import importlib.util

def run_sit_audit():
    print("====================================================")
    print("👾 AURA APP ARCHITECTURE SYSTEM INTEGRATION TEST (SIT)")
    print("====================================================\n")

    EXPECTED_STRUCTURE = {
        "core_backend": ["database.py", "auth_service.py", "task_service.py", "app_service.py"],
        "desktop_frontend": ["paint_engine.py", "system_tray.py", "dashboard_hud.py", "main_client.py"],
        "web_storefront": ["marketplace.js"]
    }

    # 1. Structural Checklist Integrity Check
    print("[STAGE 1] Running Directory Tree Check...")
    missing_elements = 0
    for folder, files in EXPECTED_STRUCTURE.items():
        if not os.path.exists(folder):
            print(f"❌ CRITICAL FAILURE: Missing directory root -> '{folder}'")
            missing_elements += 1
            continue
        for file in files:
            path = os.path.join(folder, file)
            if not os.path.exists(path):
                print(f"❌ COMPONENT MISMATCH: Missing file asset -> '{path}'")
                missing_elements += 1
            else:
                print(f"  ✓ Found component: {path}")

    if missing_elements > 0:
        print(f"\n🛑 SIT AUDIT ABORTED: {missing_elements} structural components missing.")
        sys.exit(1)

    # 2. Syntax Validation Testing Pass
    print("\n[STAGE 2] Checking Python Code Syntax & Structural References...")
    python_files = [
        "core_backend/database.py", "core_backend/auth_service.py", 
        "core_backend/task_service.py", "core_backend/app_service.py",
        "desktop_frontend/paint_engine.py", "desktop_frontend/system_tray.py", 
        "desktop_frontend/dashboard_hud.py", "desktop_frontend/main_client.py"
    ]

    for pf in python_files:
        try:
            with open(pf, "r") as source:
                compile(source.read(), pf, "exec")
            print(f"  ✓ Code compilation syntax verified clean: {pf}")
        except Exception as e:
            print(f"❌ SYNTAX EXCEPTION inside file '{pf}': {str(e)}")
            sys.exit(1)

    #     # 3. Database Engine Isolation Checks
    print("\n[STAGE 3] Checking Relational Isolation Memory Pipelines...")
    try:
        sys.path.append(os.path.abspath("core_backend"))
        from database import CloudDatabase
        
        db = CloudDatabase(":memory:")
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # FIXED: Grabbing row[0] properly flattens the list into clean strings like ['users', 'tasks']
            tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ["users", "tasks", "configurations", "owned_marketplace_skins"]
        for t in expected_tables:
            if t not in tables:
                raise ValueError(f"Missing schema registration table configuration layout: '{t}'")
                
        print("  ✓ Relational engine schemas verified clean inside isolated RAM partition.")
    except Exception as e:
        print(f"❌ RECOIL PIPELINE FAILURE: SQLite test sandbox initialization crashed: {str(e)}")
        sys.exit(1)

    print("\n====================================================")
    print("✅ SIT COMPLETE: AURA ecosystem components fully verified!")
    print("====================================================")

if __name__ == "__main__":
    run_sit_audit()
