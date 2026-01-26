# Experimental - Learning & Practice Space

## Project Overview
This is Chad's beginner-friendly learning environment for exploring programming, experimenting with code, and building skills. Chad is new to coding and learning the fundamentals, with a particular interest in automation.

## Communication Style
- **Explain clearly**: Use simple language and avoid jargon when possible
- **Be patient**: This is a learning space - explain concepts step-by-step
- **Teach good practices**: Introduce best practices gradually as skills develop
- **Encourage questions**: No question is too basic
- **Provide context**: Explain not just "how" but also "why"

## Environment
- **Purpose**: Learning, experimentation, and skill-building
- **Languages**: Open to any language - Python, JavaScript, HTML/CSS, or others as learning progresses
- **Project Types**: Small projects, exercises, experiments, and practice code

## Guidelines for Claude
1. **Educational Focus**: Prioritize learning over perfection
2. **Incremental Complexity**: Start simple, add complexity gradually
3. **Explain Your Work**: Comment code clearly and explain what you're doing
4. **Suggest Resources**: Recommend learning resources when appropriate
5. **Celebrate Progress**: Learning to code is a journey - acknowledge milestones
6. **Safety First**: Teach secure coding practices from the beginning

## Code Quality Standards

Apply these standards to ALL code created in this repository:

### Security & Safety
- **Always check for security vulnerabilities** before delivering code
- No `eval()`, `exec()`, `os.system()`, or `subprocess` with user input
- No SQL string concatenation (use parameterized queries)
- Sanitize all user input and file paths
- Validate dependencies are from trusted sources
- No hardcoded credentials or secrets

### Data Loss Prevention (CRITICAL for file operations)
- **Never delete files without explicit confirmation**
- Use safe operations (`shutil.move()` over `os.remove()`)
- Always provide **dry-run/preview mode** for file operations
- Recommend **backups before first use** of any file-operation tool
- Handle crashes gracefully (no partial/corrupted states)
- Make operations idempotent (safe to re-run)

### Error Handling
- Wrap file operations in try/except blocks
- Catch specific exceptions (PermissionError, OSError, etc.)
- Provide helpful error messages
- Never let errors corrupt data
- Log what went wrong for debugging

### Testing & Validation
- Provide ways to test code safely (dry-run, test mode)
- Include example usage in documentation
- Test with edge cases (empty input, huge files, special characters)
- Verify code works before claiming it does

### Documentation
- Code comments explain WHY, not just WHAT
- README/docs must match actual code behavior
- Include examples that actually work
- Explain limitations and caveats
- Keep docs updated when code changes

### Dependencies
- Minimize external dependencies
- Only use well-maintained, trusted libraries
- Document all dependencies in requirements.txt
- Explain what each dependency does
- Check for known vulnerabilities

### File Operations (Extra Scrutiny)
- Validate paths to prevent traversal attacks
- Check for symlinks before processing
- Handle files-in-use gracefully
- Preserve file metadata when moving/copying
- Never follow untrusted symlinks
- Set reasonable file size limits

### Repository Privacy & Sensitive Information (CRITICAL)

**NEVER commit sensitive or personal information to git repositories.**

#### What is Sensitive Information?

**Always protect:**
- API keys, tokens, passwords, credentials
- Database connection strings with passwords
- Private keys, certificates, SSH keys
- Personal paths with usernames (e.g., `/Users/chadmiller/`)
- Email addresses, phone numbers
- Personal configuration files with custom paths
- Sample data with real information
- `.env` files with secrets

**Generally safe to commit:**
- Generic code without personal info
- Example configurations with placeholders (e.g., `YOUR_USERNAME`)
- Documentation with generic examples
- Template files for others to customize

#### How to Protect Sensitive Information

**1. Use .gitignore (Always)**

Before first commit, create `.gitignore` with:
```
# Personal configuration files
config_personal.json
*_personal.*
.env
.env.local

# Files with custom paths
run_script.sh  # If it contains personal paths

# Secrets and credentials
*.pem
*.key
secrets/
credentials.json

# Output that might contain sensitive data
*.log
*.pdf
output/
```

**2. Create Template Files**

Instead of committing personal files, create generic templates:

❌ **DON'T commit:**
```bash
# run_script.sh (with personal paths)
USER_PATH="/Users/chadmiller/Documents"
API_KEY="sk_live_abc123"
```

✅ **DO commit a template:**
```bash
# run_script_template.sh (generic)
USER_PATH="/Users/YOUR_USERNAME/Documents"
API_KEY="your_api_key_here"
# Instructions: Copy this to run_script.sh and customize
```

**3. Use Environment Variables for Secrets**

❌ **DON'T hardcode:**
```python
api_key = "sk_live_abc123"
```

✅ **DO use environment variables:**
```python
import os
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY not set. See setup instructions.")
```

**4. Document Setup Without Exposing Secrets**

In README.md, provide instructions:
```markdown
## Setup

1. Copy the template: `cp config_template.json config.json`
2. Edit `config.json` with your API key
3. The file is gitignored and won't be committed
```

#### Before Making a Repository Public

**Checklist:**

1. **Audit all files:**
   ```bash
   # Check what's tracked in git
   git ls-files

   # Search for potential secrets
   git grep -i "password\|api_key\|secret"
   git grep -E "/Users/[a-z]+"  # Personal paths
   ```

2. **Review file contents:**
   - Configuration files (*.json, *.yaml, *.sh)
   - Documentation (*.md)
   - Example files

3. **Check git history:**
   - Even deleted files remain in git history!
   - If secrets were previously committed, history must be cleaned
   - Consider starting fresh repo if secrets were committed

4. **Create templates for personal files:**
   - Replace usernames with `YOUR_USERNAME`
   - Replace paths with placeholders
   - Replace API keys with `your_api_key_here`
   - Add to `.gitignore`

5. **Test with fresh clone:**
   ```bash
   cd /tmp
   git clone <your-repo-url>
   cd <repo-name>
   # Can you use it without your personal files?
   # Are setup instructions clear?
   ```

#### What to Do If You Accidentally Commit Secrets

**If not yet pushed to GitHub:**
```bash
# Remove from last commit
git reset HEAD~1
# Add to .gitignore
echo "secrets.json" >> .gitignore
git add .gitignore
git commit -m "Add gitignore"
```

**If already pushed to GitHub:**
1. **Immediately rotate/revoke the exposed secret** (change password, regenerate API key)
2. Remove from git history (requires force push - dangerous)
3. Consider creating new repo if history is complex
4. Never rely on "just deleting" - it stays in git history

#### Examples from This Project

**Personal files (NOT in git):**
- `pdf_rules_filing_cabinet.json` - Contains `/Users/chadmiller/` paths
- `run_incoming_scans.sh` - Contains personal folder locations

**Template files (IN git):**
- `pdf_rules_example.json` - Generic example with placeholders
- `run_incoming_scans_template.sh` - Generic with `YOUR_USERNAME`

**How users set up:**
```bash
cp run_incoming_scans_template.sh run_incoming_scans.sh
cp pdf_rules_example.json pdf_rules_filing_cabinet.json
# Edit both files with personal paths
# These files are gitignored and stay local
```

#### Key Principles

1. **Default to privacy** - When in doubt, don't commit it
2. **Templates over examples** - Provide templates users can customize
3. **Educate users** - Document why files are gitignored
4. **Test assumptions** - Clone and verify nothing personal is exposed
5. **Plan for public** - Write code as if it will be public someday

### When to Proactively Provide
Without being asked, always provide:
- **Security analysis** for any code that handles files, runs commands, or processes user input
- **Backup recommendations** before first use of file-operation tools
- **Dry-run mode** for any destructive operations
- **Error handling** for all file/network operations
- **Clear warnings** about risks or limitations

### Red Flags to Avoid
Never include in code without explicit discussion:
- Command execution with user-controlled input
- File deletion without confirmation
- Database queries via string concatenation
- Downloading and executing code
- Requests for unnecessary permissions
- Crypto/encryption without established libraries

## Current Learning Goals
- Building foundational programming skills
- Understanding how code works
- Experimenting with different languages and tools
- Learning by doing

## Notes
- This repository is a safe space to experiment and make mistakes
- Code doesn't need to be production-ready - it's for learning
- Feel free to ask "why" or for explanations at any time
