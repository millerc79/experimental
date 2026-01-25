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
