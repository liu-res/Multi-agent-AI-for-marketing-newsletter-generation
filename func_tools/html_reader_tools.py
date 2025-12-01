# html_reader_tools.py
# Function tools for reading HTML files from style_samples directory

from google.adk.tools.function_tool import FunctionTool
from pathlib import Path


    def read_html_file(file_path: str) -> dict:
        """Read HTML content from a file.
        
        Args:
            file_path: Path to the HTML file (relative or absolute)
            
        Returns:
            dict: {"success": bool, "content": str, "file_path": str, "error": str}
        """
        try:
            path = Path(file_path)
            if not path.is_absolute():
                # Try relative to current directory
                path = Path.cwd() / path
            
            if path.exists() and path.is_file():
                content = path.read_text(encoding='utf-8')
                return {
                    "success": True,
                    "content": content,
                    "file_path": str(path.absolute())
                }
            else:
                return {
                    "success": False,
                    "content": "",
                    "file_path": str(path.absolute()),
                    "error": "File does not exist"
                }
        except Exception as e:
            return {
                "success": False,
                "content": "",
                "file_path": file_path,
                "error": str(e)
            }
    

    def list_html_files(directory: str = "./style_samples") -> dict:
        """List HTML files in a directory (recursively searches subdirectories).
        
        Args:
            directory: Directory path to search (default: ./style_samples)
            
        Returns:
            dict: {"success": bool, "files": list, "directory": str, "error": str}
        """
        try:
            dir_path = Path(directory)
            if not dir_path.is_absolute():
                dir_path = Path.cwd() / dir_path
            
            if dir_path.exists() and dir_path.is_dir():
                # Use rglob for recursive search to find HTML files in subdirectories
                html_files = list(dir_path.rglob("*.html")) + list(dir_path.rglob("*.htm"))
                return {
                    "success": True,
                    "files": [str(f.relative_to(Path.cwd())) for f in html_files],
                    "directory": str(dir_path.absolute())
                }
            else:
                return {
                    "success": False,
                    "files": [],
                    "directory": str(dir_path.absolute()),
                    "error": "Directory does not exist"
                }
        except Exception as e:
            return {
                "success": False,
                "files": [],
                "directory": directory,
                "error": str(e)
            }
    

# Create FunctionTool instances
    read_html_tool = FunctionTool(
        func=read_html_file
    )
    
    list_html_files_tool = FunctionTool(
        func=list_html_files
    )
    
# Export tools as a list for easy import
html_reader_tools = [read_html_tool, list_html_files_tool]

print("HTML Reader tools created")
