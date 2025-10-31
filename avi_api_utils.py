import yaml
import requests
import time
from typing import Dict, Any


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """Parses the YAML configuration file and validates required sections."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        if 'api' not in config or 'test_cases' not in config:
            raise ValueError("config.yaml must contain 'api' and 'test_cases' sections.")

        print(f"Configuration loaded successfully from {config_path}.")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        raise
    except yaml.YAMLError as e:
        print(f" Error parsing YAML: {e}")
        raise
    except ValueError as e:
        print(f"Error in config structure: {e}")
        raise


def mock_ssh(host: str = "target_host") -> None:
    """MOCK_SSH: Placeholder for SSH connection."""
    print(f"    [MOCK_SSH] Connecting to host: {host}...")
    time.sleep(0.5)
    print(f"    [MOCK_SSH] Successfully connected (mock).")


def mock_rdp(host: str = "target_host") -> None:
    """MOCK_RDP: Placeholder for RDP validation."""
    print(f"    [MOCK_RDP] Validating remote connection for host: {host}...")
    time.sleep(0.5)
    print(f"    [MOCK_RDP] Remote connection validated (mock).")


def api_call(config: Dict[str, Any], method: str, endpoint: str, payload: Dict[str, Any] = None, target_uuid: str = None):
    """
    Generic function to make authenticated API calls.
    Replaces {uuid} in endpoint if target_uuid is provided.
    Returns requests.Response on success or None on failure.
    """
    base_url = config['api'].get('base_url', '').rstrip('/')
    headers = config['api'].get('headers', {})

    if isinstance(endpoint, str) and endpoint.startswith('http'):
        url = endpoint
    else:
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = f"{base_url}{endpoint}"

    if target_uuid:
        url = url.replace("{uuid}", target_uuid)

    print(f"  -> API Call: {method} {url}")

    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=15)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=payload, timeout=15)
        else:
            print(f"  [Error] Unsupported API method: {method}")
            return None

        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as e:
        body = getattr(e.response, 'text', None) if hasattr(e, 'response') else None
        print(f"  HTTP Error for {method} {url}: {e}")
        if body:
            print(f"  Response Body: {body}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Connection Error for {method} {url}: {e}")
        return None


def execute_test_workflow(config: Dict[str, Any], test_case: Dict[str, Any], target_uuid: str) -> Dict[str, str]:
    """
    Executes the workflow defined for a single test case.

    Returns a mapping of stage name -> status string. Status values used by main.py
    are: 'PASS', 'CONTENT_PASS', 'MOCK_SUCCESS', 'FAIL', 'CONTENT_FAIL', 'SKIPPED'.
    """
    results: Dict[str, str] = {}

    test_id = test_case.get('id', 'UNKNOWN')
    print()
    print(f"Starting Test Case: {test_id}")
    print()

    workflow = test_case.get('workflow', [])
    for step in workflow:
        stage = step.get('stage', 'unnamed_stage')
        step_type = step.get('type', '').upper()

        print(f"Stage: {stage} ({step_type}) -")

        if step_type == 'MOCK_SSH':
            mock_ssh(test_case.get('target_vs_name', 'target_host'))
            results[stage] = 'MOCK_SUCCESS'

        elif step_type == 'MOCK_RDP':
            mock_rdp(test_case.get('target_vs_name', 'target_host'))
            results[stage] = 'MOCK_SUCCESS'

        elif step_type in ('GET', 'PUT'):
            endpoint = step.get('endpoint', '')
            payload = step.get('payload')
            expected_status = step.get('expected_status', 200)

            resp = api_call(config, step_type, endpoint, payload=payload, target_uuid=target_uuid)
            if resp is None:
                print(f"  [FAIL] HTTP request failed for stage: {stage}")
                results[stage] = 'FAIL'
                print('')
                continue

            if resp.status_code == expected_status:
                print(f"  [PASS] Status Code: {resp.status_code} matches expected {expected_status}.")
                results[stage] = 'PASS'
            else:
                print(f"  [FAIL] Status Code: {resp.status_code} does not match expected {expected_status}.")
                results[stage] = 'FAIL'
                print('')
                continue

            validation = step.get('validation_check')
            if validation:
                try:
                    data = resp.json()
                except ValueError:
                    print(f"  [FAIL] Could not parse JSON response for validation in stage: {stage}")
                    results[stage] = 'FAIL'
                    print('')
                    continue

                for key, expected_value in validation.items():
                    actual_value = data
                    for part in str(key).split('.'):
                        if isinstance(actual_value, dict) and part in actual_value:
                            actual_value = actual_value[part]
                        else:
                            actual_value = None
                            break

                    if actual_value == expected_value:
                        print(f"    [PASS] Validation: Found '{key}': {actual_value}")
                    else:
                        print(f"    [FAIL] Validation: For '{key}' expected '{expected_value}', got '{actual_value}'")
                        results[stage] = 'CONTENT_FAIL'

        else:
            print(f"  [WARN] Unknown workflow step type '{step_type}' for stage '{stage}', skipping.")
            results[stage] = 'SKIPPED'

        print('')

    return results
