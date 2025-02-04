class ProjectCreationError(Exception):
    """Base exception for project creation errors."""
    pass

class GitHubError(ProjectCreationError):
    """Raised when GitHub operations fail."""
    pass

class CodemagicError(ProjectCreationError):
    """Raised when Codemagic operations fail."""
    pass

class FileSystemError(ProjectCreationError):
    """Raised when file system operations fail."""
    pass 