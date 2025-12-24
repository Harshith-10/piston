import requests
import json
import time

URL = "http://localhost:2000/api/v3/execute"

def test_whitespace_mismatch():
    print("Testing Whitespace Mismatch...")
    payload = {
        "language": "python",
        "version": "3.12.0",
        "files": [
            {
                "name": "main.py",
                "content": "print([0, 1])"
            }
        ],
        "testcases": [
            {
                "id": "1",
                "input": "",
                "expectedOutput": "[0,1]"
            }
        ]
    }
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print("Response:", json.dumps(data, indent=2))
        
        # Validation
        passed = True
        for tc in data['testcases']:
            if not tc['passed']:
                print(f"Testcase {tc['id']} FAILED. Expected: '{tc['expectedOutput']}', Actual: '{tc['actualOutput']}'")
                passed = False
            else:
                print(f"Testcase {tc['id']} PASSED")
        
        if passed:
            print("Whitespace Mismatch Test PASSED (Unexpectedly)")
        else:
            print("Whitespace Mismatch Test FAILED (As Expected)")

    except Exception as e:
        print(f"Test failed in request: {e}")
        if 'response' in locals():
            print(response.text)

def waitForServer():
    print("Waiting for server to be ready...")
    for i in range(30):
        try:
            requests.get("http://localhost:2000/api/v2/runtimes")
            print("Server is ready!")
            return
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nServer did not become ready in time.")
    exit(1)

if __name__ == "__main__":
    waitForServer()
    test_whitespace_mismatch()
