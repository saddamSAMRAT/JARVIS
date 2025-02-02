import os
import re
import subprocess
import sys

def check_hardcoded_secrets(directory):
    """
    Scan for potential hardcoded secrets
    """
    secret_patterns = [
        r'(api_key|password|secret|token)\s*=\s*[\'"][^\'"]+[\'"]\s*',  # Basic secret detection
        r'(https?://[^:]+:[^@]+@)',  # URL with credentials
    ]
    
    findings = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.json', '.yml', '.yaml', '.env')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            findings.append({
                                'file': filepath,
                                'matches': matches
                            })
    
    return findings

def check_dependency_vulnerabilities():
    """
    Check for known vulnerabilities in dependencies
    """
    try:
        result = subprocess.run(
            ['safety', 'check', '-r', 'requirements-prod.txt'], 
            capture_output=True, 
            text=True
        )
        return result.stdout
    except Exception as e:
        print(f"Error running safety check: {e}")
        return None

def main():
    print("🔒 Security Scan Starting...")
    
    # Secret scanning
    print("\n🕵️ Scanning for potential hardcoded secrets...")
    secret_findings = check_hardcoded_secrets('.')
    if secret_findings:
        print("⚠️ Potential secrets found:")
        for finding in secret_findings:
            print(f" - {finding['file']}: {finding['matches']}")
        sys.exit(1)
    else:
        print("✅ No hardcoded secrets detected")
    
    # Dependency vulnerability check
    print("\n🛡️ Checking dependency vulnerabilities...")
    vulnerabilities = check_dependency_vulnerabilities()
    if vulnerabilities:
        print("⚠️ Vulnerabilities found:")
        print(vulnerabilities)
        sys.exit(1)
    else:
        print("✅ No known vulnerabilities in dependencies")
    
    print("\n🎉 Security Scan Completed Successfully!")

if __name__ == "__main__":
    main()
