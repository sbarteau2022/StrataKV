import re

with open('/Users/stewartbarteau/Desktop/stratakv/benchmarks/generate_multitier_suite.py', 'r') as f:
    content = f.read()

# Replace the unescaped JS template literal:
# document.getElementById('telemetryStats').textContent = `File: ${fileKey} • Size: ${sizeKb} KB • Top-level keys: ${keysCount}`;
# with plain string concatenation:
# document.getElementById('telemetryStats').textContent = "File: " + fileKey + " • Size: " + sizeKb + " KB • Top-level keys: " + keysCount;

old_str = "document.getElementById('telemetryStats').textContent = `File: ${fileKey} • Size: ${sizeKb} KB • Top-level keys: ${keysCount}`;"
new_str = 'document.getElementById(\'telemetryStats\').textContent = "File: " + fileKey + " • Size: " + sizeKb + " KB • Top-level keys: " + keysCount;'

if old_str in content:
    content = content.replace(old_str, new_str)
    print("Replaced template literal successfully.")
else:
    # search for fileKey in content
    matches = [line for line in content.split('\n') if 'fileKey' in line]
    print("Lines containing fileKey:", matches)

with open('/Users/stewartbarteau/Desktop/stratakv/benchmarks/generate_multitier_suite.py', 'w') as f:
    f.write(content)

print("Updated generate_multitier_suite.py")
