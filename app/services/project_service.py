import os
import yaml
from app.exceptions import FileSystemError
from .templates.xcodegen_template import create_xcodegen_config
from .templates.codemagic_template import create_codemagic_config
from .templates.swiftui_template import create_swiftui_files

class ProjectService:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir

    def create_project(self, project_name):
        """
        Creates the project structure and all necessary files.
        
        Args:
            project_name (str): The name of the iOS project
            
        Returns:
            str: The path to the created project
            
        Raises:
            FileSystemError: If project creation fails
            ValueError: If project_name is None or empty
        """
        if not project_name:
            raise ValueError("Project name is required")
            
        try:
            project_path = os.path.join(self.workspace_dir, project_name)
            os.makedirs(project_path, exist_ok=True)

            # Create project.yml for XcodeGen
            self._create_xcodegen_config(project_path, project_name)

            # Create SwiftUI files
            create_swiftui_files(project_path, project_name)

            # Create codemagic.yaml
            self._create_codemagic_config(project_path, project_name)

            return project_path
            
        except OSError as e:
            raise FileSystemError(f"Failed to create project: {str(e)}")

    def _create_xcodegen_config(self, project_path, project_name):
        """Creates the XcodeGen configuration file."""
        config = create_xcodegen_config(project_name)
        self._write_yaml(os.path.join(project_path, 'project.yml'), config)

    def _create_codemagic_config(self, project_path, project_name):
        """Creates the Codemagic configuration file."""
        config = create_codemagic_config(project_name)
        self._write_yaml(os.path.join(project_path, 'codemagic.yaml'), config)

    def _write_yaml(self, path, data):
        """Helper function to write YAML data to a file."""
        try:
            with open(path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        except OSError as e:
            raise FileSystemError(f"Failed to write file {path}: {str(e)}") 