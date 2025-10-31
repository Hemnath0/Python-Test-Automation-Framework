import sys
import os
from avi_api_utils import load_config, api_call, execute_test_workflow
from concurrent.futures import ThreadPoolExecutor


class Tee:
    """Duplicates standard output to multiple file-like objects (e.g., console and a log file)."""
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)

    def flush(self):
        for f in self.files:
            try:
                f.flush()
            except Exception:
                pass

def run_framework():
    # 1. Load Configuration
    config = load_config()
    print('DEBUG: config loaded, keys=', list(config.keys()))
    sys.stdout.flush()
 
    if not config.get('test_cases'):
        print("Fatal Error: 'test_cases' section is empty in config.yaml. Exiting.")
        return

    target_vs_name = config['test_cases'][0]['target_vs_name']
    
    # 2. Pre-Fetcher Stage (Executed Once)
    print("# 1. PRE-FETCHER STAGE (Global Setup) #")
    
    # a) Fetch all Virtual Services
    print('DEBUG: calling /api/virtualservice')
    sys.stdout.flush()
    vs_response = api_call(config, 'GET', '/api/virtualservice')
    if not vs_response:
        print("Fatal Error: Could not fetch Virtual Services. Exiting.")
        return
        
    vs_json = vs_response.json()
    if isinstance(vs_json, dict) and 'results' in vs_json:
        raw_vs_list = vs_json['results']
    else:
        raw_vs_list = vs_json

    normalized_vs_list = []
    for item in raw_vs_list:
        if isinstance(item, str) and item.startswith('http'):
            resp = api_call(config, 'GET', item)
            if resp:
                try:
                    normalized_vs_list.append(resp.json())
                except ValueError:
                    pass
        elif isinstance(item, dict):
            normalized_vs_list.append(item)
    
    vs_list = normalized_vs_list if normalized_vs_list else raw_vs_list

    print(f"Pre-Fetcher: Found {len(vs_list)} Virtual Services.")
    
    # b) Fetch all Service Engines
    print('DEBUG: calling /api/serviceengine')
    sys.stdout.flush()
    se_response = api_call(config, 'GET', '/api/serviceengine')
    if not se_response:
        print("Warning: Could not fetch Service Engines.")
        se_count = "N/A"
    else:
        se_count = len(se_response.json())
        print(f"Pre-Fetcher: Found {se_count} Service Engines.")

    # c) Fetch all Tenants
    print('DEBUG: calling /api/tenant')
    sys.stdout.flush()
    tenant_response = api_call(config, 'GET', '/api/tenant')
    if not tenant_response:
        print("Warning: Could not fetch Tenants.")
        tenant_count = "N/A"
    else:
        tenant_count = len(tenant_response.json())
        print(f"Pre-Fetcher: Found {tenant_count} Tenants.")

    print(f"\nPre-Fetcher Summary")
    print(f"VS Count: {len(vs_list)}, SE Count: {se_count}, Tenant Count: {tenant_count}")
    
    # 3. Identify Target Virtual Service and UUID
    target_vs = next((vs for vs in vs_list if vs.get("name") == target_vs_name), None)
    
    if not target_vs:
        print(f"Fatal Error: Target Virtual Service '{target_vs_name}' not found. Exiting.")
        return

    target_uuid = target_vs.get('url', '').split('/')[-1]
    
    if not target_uuid:
        print(f"Fatal Error: Could not extract UUID from target VS '{target_vs_name}'. Exiting.")
        return

    print(f"Identified Target VS: '{target_vs_name}' with UUID: {target_uuid}")
    sys.stdout.flush()
    
    # 4. Parallel Task Execution
    print("# 2. PARALLEL TASK EXECUTION #")

    test_cases = config['test_cases']
    parallel_count = config['settings'].get('parallel_execution_count', 2)

    with ThreadPoolExecutor(max_workers=parallel_count) as executor:
        print('DEBUG: starting ThreadPoolExecutor with', parallel_count, 'workers')
        sys.stdout.flush()
        future_results = executor.map(
            lambda tc: execute_test_workflow(config, tc, target_uuid), 
            test_cases
        )

        final_results = list(future_results)
        
    print("# 3. FINAL RESULTS SUMMARY #")
    
    for i, result in enumerate(final_results):
        test_id = test_cases[i]['id']
        overall_status = "SUCCESS" if all(s in ["PASS", "CONTENT_PASS", "MOCK_SUCCESS", "SKIPPED"] for s in result.values()) else "FAILURE"
        print(f"Test Case ID: {test_id} | Status: {overall_status}")
        for stage, status in result.items():
            print(f"  - {stage}: {status}")

if __name__ == '__main__':
    log_path = os.path.join(os.getcwd(), 'output.log')

    old_stdout = sys.stdout

    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            tee = Tee(old_stdout, f)
            sys.stdout = tee
            
            run_framework()
            
    except Exception as e:
        if sys.stdout != old_stdout:
            sys.stdout = old_stdout 
        print(f"\n\n FATAL EXCEPTION DURING EXECUTION: {e}", file=sys.stderr)
        
    finally:
        if sys.stdout != old_stdout:
            sys.stdout = old_stdout
            
    print(f"\nWrote full run output to: {log_path}")
