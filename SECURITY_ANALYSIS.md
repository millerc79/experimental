# Security Analysis - PDF Automation Tool

This document provides a comprehensive security analysis of the PDF automation tool.

## Executive Summary

**Overall Security Rating: MEDIUM** ⚠️

The tool is **safe for personal use** in trusted environments but has some vulnerabilities that should be addressed before use in multi-user or untrusted environments.

## Security Strengths ✅

### 1. No Command Injection Vulnerabilities
- ✅ **No shell commands executed** - All operations use Python APIs
- ✅ **No `os.system()`, `subprocess`, or `exec()`** calls
- ✅ **No eval() or similar dynamic code execution**

### 2. Filename Sanitization
- ✅ Invalid characters removed/replaced
- ✅ Path separators (`/`, `\`) are sanitized
- ✅ Control characters removed
- ✅ Length limits enforced

### 3. Error Handling
- ✅ Permission errors caught and handled
- ✅ File operation errors don't crash the tool
- ✅ No sensitive information in error messages

### 4. Read-Only PDF Processing
- ✅ PDFs are only read, never modified
- ✅ Text extraction doesn't execute code
- ✅ PyPDF2 is a well-established library

### 5. Local Processing Only
- ✅ No network requests
- ✅ No data sent to external services
- ✅ All processing happens locally

## Security Vulnerabilities ⚠️

### 1. Path Traversal Vulnerability (HIGH RISK)

**Location:** `pdf_automation.py` line 374

**Problem:**
```python
dest_folder = Path(source_folder) / move_to_path
```

If `move_to_path` contains `../`, files can be moved outside the intended directory.

**Attack Scenario:**
An attacker who can modify `pdf_rules.json` could add:
```json
{
  "move_to": "../../../etc/important_file"
}
```

This would move PDFs to `/Users/chadmiller/etc/important_file` or even further up.

**Severity:** HIGH (but requires attacker to modify rules file)

**Mitigation:** The rules file is user-controlled, so this requires local file access. For personal use, this is acceptable. For shared environments, path validation should be added.

**Recommended Fix:**
```python
# Resolve and validate the path
dest_folder = (Path(source_folder) / move_to_path).resolve()
# Ensure it's under the source folder or a safe base directory
if not str(dest_folder).startswith(str(Path(source_folder).resolve())):
    # For absolute paths, could check against allowlist
    pass
```

### 2. Symlink Following (MEDIUM RISK)

**Location:** File operations throughout

**Problem:**
- `Path.mkdir()` follows symlinks
- `shutil.move()` follows symlinks
- An attacker could create a symlink in the source folder

**Attack Scenario:**
1. Attacker creates: `Incoming Scans/malicious.pdf` → symlink to `/etc/passwd`
2. Tool reads the "PDF" (actually reads /etc/passwd)
3. Tool moves it based on rules

**Severity:** MEDIUM (requires local file access to create symlinks)

**Mitigation for your use:** You control the Incoming Scans folder, so this isn't a concern.

**Recommended Fix:**
```python
# Check for symlinks before processing
if Path(pdf_path).is_symlink():
    print(f"   ⚠️  Skipping symlink: {pdf_path}")
    return False
```

### 3. Unrestricted File Reading (LOW RISK)

**Location:** `extract_text_from_pdf()`

**Problem:**
The tool will read any PDF file it finds, regardless of size.

**Attack Scenario:**
A malicious PDF could be crafted to:
- Be extremely large (causing memory exhaustion)
- Contain malicious JavaScript (though PyPDF2 doesn't execute it)
- Exploit a vulnerability in PyPDF2

**Severity:** LOW (PyPDF2 is mature, large files would just slow processing)

**Mitigation:**
- PyPDF2 doesn't execute JavaScript or embedded code
- Large files will just take time to process

**Recommended Fix:**
```python
# Check file size before processing
max_size = 100 * 1024 * 1024  # 100 MB
if os.path.getsize(pdf_path) > max_size:
    print(f"   ⚠️  File too large, skipping: {pdf_path}")
    return False
```

### 4. JSON Injection (LOW RISK)

**Location:** `load_rules()`

**Problem:**
The rules file is loaded with `json.load()` without validation.

**Attack Scenario:**
If an attacker can modify `pdf_rules.json`, they can:
- Change where files go (path traversal above)
- Crash the tool with malformed JSON
- Potentially exploit JSON parsing vulnerabilities

**Severity:** LOW (requires local file access to modify rules)

**Mitigation:** The user controls the rules file. For personal use, this is fine.

**Recommended Fix:**
```python
# Validate rules structure after loading
def validate_rules(rules):
    for rule in rules:
        if 'name' not in rule or 'conditions' not in rule:
            raise ValueError(f"Invalid rule: {rule}")
    return rules
```

### 5. No Input Validation on Paths (MEDIUM RISK)

**Location:** Command-line argument parsing

**Problem:**
User-provided folder paths aren't validated before use.

**Attack Scenario:**
```bash
python3 pdf_automation.py --folder "/etc"
```

This would try to process PDFs in /etc (would fail on permissions, but shouldn't be attempted).

**Severity:** MEDIUM (user shoots themselves in the foot)

**Mitigation:** User is expected to provide correct paths. Error handling prevents damage.

**Recommended Fix:**
```python
# Warn user if processing system folders
dangerous_paths = ['/etc', '/usr', '/var', '/System']
if any(folder_path.startswith(p) for p in dangerous_paths):
    response = input(f"⚠️  Processing {folder_path} is dangerous. Continue? (yes/no): ")
    if response.lower() != 'yes':
        return
```

## Dependency Security

### PyPDF2

**Version:** Latest (3.0.1 as of creation)

**Known Issues:**
- PyPDF2 has had security vulnerabilities in the past (mostly DoS via malformed PDFs)
- Current version is maintained and patched

**Recommendations:**
- ✅ Keep PyPDF2 updated: `pip install --upgrade PyPDF2`
- ✅ Monitor security advisories: https://github.com/py-pdf/pypdf/security
- Consider switching to `pypdf` (the maintained fork) in the future

**Check for updates:**
```bash
pip list --outdated | grep PyPDF2
```

## Threat Model

### Who might attack this tool?

1. **Malicious PDF sender** - Sends crafted PDFs to be scanned
   - Risk: LOW - PyPDF2 only reads text, doesn't execute code

2. **Local attacker with file access** - Can modify rules file
   - Risk: MEDIUM - Can use path traversal to move files anywhere
   - Mitigation: Secure your Mac with FileVault, user password

3. **Malware on your system** - Could modify rules or create malicious PDFs
   - Risk: HIGH - If malware is running, it can do anything anyway
   - Mitigation: Keep macOS updated, use antivirus

### What are the assets being protected?

1. **PDF documents** - Could contain sensitive financial/medical info
   - Protected by: File permissions, local processing only

2. **Filing Cabinet structure** - Organization of sensitive documents
   - Protected by: File permissions

3. **System integrity** - Ensuring tool doesn't damage OS
   - Protected by: No shell commands, permission checks

## Security Best Practices for Users

### 1. File Permissions ✅

Your setup already follows best practices:
- Both folders in your home directory
- You own both folders
- Standard user permissions (not root)

### 2. Rules File Security

**Recommendations:**
```bash
# Ensure rules file is not world-writable
chmod 644 pdf_rules_filing_cabinet.json

# Check ownership
ls -l pdf_rules_filing_cabinet.json
# Should show: -rw-r--r--  chadmiller  staff
```

### 3. Keep Dependencies Updated

```bash
# Check for updates
pip list --outdated

# Update PyPDF2
pip install --upgrade PyPDF2
```

### 4. Monitor Processed Files

Periodically check your Filing Cabinet to ensure files are going to expected locations.

### 5. Use Dry Run First

Always test rules with `--dry-run` before processing:
```bash
./run_incoming_scans.sh dry-run
```

### 6. Backup Important Files

Before running the tool on important documents:
```bash
# Backup your Filing Cabinet
tar -czf filing_cabinet_backup.tar.gz ~/Documents/Filing\ Cabinet
```

## Comparison to Hazel

### Security Advantages over Hazel:

✅ **Open source** - You can audit the code (Hazel is closed source)
✅ **No sudo required** - Runs as regular user
✅ **Local only** - No network access
✅ **Simple codebase** - Easy to understand and verify

### Security Disadvantages:

⚠️ **Less mature** - Hazel has been tested by thousands of users
⚠️ **No sandboxing** - Hazel runs in macOS sandbox
⚠️ **Python dependency** - Requires Python runtime

## Recommendations

### For Personal Use (Your Current Setup): SAFE ✅

Your setup is **safe for personal use** because:
- You control both folders
- You control the rules file
- You're the only user
- No untrusted input

**No changes needed** for your use case.

### For Shared/Production Use: NEEDS HARDENING ⚠️

If deploying in a shared environment, implement:

1. **Path Validation**
   ```python
   # Validate move_to paths don't escape
   # Check for ../ patterns
   # Allowlist permitted destination folders
   ```

2. **Symlink Protection**
   ```python
   # Skip symlinks
   if Path(pdf_path).is_symlink():
       skip_file()
   ```

3. **File Size Limits**
   ```python
   # Reject files over 100MB
   max_size = 100 * 1024 * 1024
   ```

4. **Rules Validation**
   ```python
   # Validate rules structure
   # Reject rules with suspicious patterns
   ```

## Security Checklist

- [x] No command injection vulnerabilities
- [x] No code execution vulnerabilities
- [x] Filename sanitization implemented
- [x] Error handling prevents information disclosure
- [x] Local processing only (no network)
- [x] No sudo/elevated privileges required
- [ ] Path traversal protection (not needed for personal use)
- [ ] Symlink following protection (not needed for personal use)
- [ ] File size limits (not needed for personal use)
- [ ] Rules validation (not needed for personal use)

## Conclusion

**For your personal use on your Mac: The code is SECURE. ✅**

The identified vulnerabilities require:
1. Local file access to your Mac
2. Ability to modify rules file or source folder
3. You to run the modified rules

Since you control all of these, the risk is **LOW**.

**If you were to deploy this for multiple users or in an untrusted environment, additional hardening would be recommended.**

## Security Contacts

If you discover a security issue:
1. Do not publish it publicly
2. Create a private issue on GitHub
3. Or contact: security@your-repo.com

---

Last Updated: 2025-01-25
Risk Assessment: LOW for personal use, MEDIUM for shared environments
