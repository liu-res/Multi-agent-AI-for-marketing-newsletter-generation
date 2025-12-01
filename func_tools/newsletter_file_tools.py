# newsletter_file_tools.py
# Function tools for newsletter file operations

from google.adk.tools.function_tool import FunctionTool
from pathlib import Path


def write_file(file_path: str, content: str) -> dict:
    """Write content to a file.
    
    Args:
        file_path: Path to the file (relative or absolute)
        content: Content to write to the file
        
    Returns:
        dict: {"success": bool, "file_path": str, "error": str}
    """
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path.cwd() / path
        
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        path.write_text(content, encoding='utf-8')
        return {
            "success": True,
            "file_path": str(path.absolute()),
            "message": f"File written successfully: {path.absolute()}"
        }
    except Exception as e:
        return {
            "success": False,
            "file_path": file_path,
            "error": str(e)
        }


def check_newsletter_content_exists() -> dict:
    """Check if ./output/newsletter_content.txt exists.
    
    Returns:
        dict: {"exists": bool, "file_path": str}
    """
    file_path = Path("./output/newsletter_content.txt")
    exists = file_path.exists() and file_path.is_file()
    return {
        "exists": exists,
        "file_path": str(file_path.absolute())
    }


def read_newsletter_content() -> dict:
    """Read the content from ./output/newsletter_content.txt file.
    
    Returns:
        dict: {"content": str, "file_path": str, "success": bool}
    """
    file_path = Path("./output/newsletter_content.txt")
    try:
        if file_path.exists() and file_path.is_file():
            content = file_path.read_text(encoding='utf-8')
            return {
                "success": True,
                "content": content,
                "file_path": str(file_path.absolute())
            }
        else:
            return {
                "success": False,
                "content": "",
                "file_path": str(file_path.absolute()),
                "error": "File does not exist"
            }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "file_path": str(file_path.absolute()),
            "error": str(e)
        }


# Create FunctionTool instances
write_file_tool = FunctionTool(
    func=write_file
)

check_content_file_tool = FunctionTool(
    func=check_newsletter_content_exists
)

read_content_file_tool = FunctionTool(
    func=read_newsletter_content
)


