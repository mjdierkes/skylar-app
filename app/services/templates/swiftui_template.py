import os
from app.exceptions import FileSystemError

def create_swiftui_files(project_path, project_name):
    """
    Creates the SwiftUI source files for the project.
    
    Args:
        project_path (str): The root path of the project
        project_name (str): The name of the iOS project
        
    Raises:
        ValueError: If project_path or project_name is None or empty
        FileSystemError: If file creation fails
    """
    if not project_path or not project_name:
        raise ValueError("Project path and name are required")
        
    try:
        sources_dir = os.path.join(project_path, 'Sources')
        os.makedirs(sources_dir, exist_ok=True)
        
        _create_app_file(sources_dir, project_name)
        _create_content_view_file(sources_dir)
        _create_models_directory(sources_dir)
        _create_views_directory(sources_dir)
    except OSError as e:
        raise FileSystemError(f"Failed to create SwiftUI files: {str(e)}")

def _create_app_file(sources_dir, project_name):
    """Creates the main App.swift file."""
    app_content = f'''import SwiftUI

@main
struct {project_name}App: App {{
    var body: some Scene {{
        WindowGroup {{
            ContentView()
        }}
    }}
}}
'''
    _write_file(os.path.join(sources_dir, 'App.swift'), app_content)

def _create_content_view_file(sources_dir):
    """Creates the ContentView.swift file with a modern SwiftUI interface."""
    view_content = '''import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Image(systemName: "swift")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 100, height: 100)
                    .foregroundColor(.blue)
                
                Text("Welcome to SwiftUI!")
                    .font(.title)
                    .fontWeight(.bold)
                
                Text("Start building something amazing")
                    .foregroundColor(.secondary)
            }
            .padding()
            .navigationTitle("My App")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
'''
    _write_file(os.path.join(sources_dir, 'ContentView.swift'), view_content)

def _create_models_directory(sources_dir):
    """Creates a directory for model files with a sample model."""
    models_dir = os.path.join(sources_dir, 'Models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_content = '''import Foundation

struct Item: Identifiable {
    let id = UUID()
    var title: String
    var description: String
}
'''
    _write_file(os.path.join(models_dir, 'Item.swift'), model_content)

def _create_views_directory(sources_dir):
    """Creates a directory for view components."""
    views_dir = os.path.join(sources_dir, 'Views')
    os.makedirs(views_dir, exist_ok=True)

def _write_file(path, content):
    """Helper function to write content to a file."""
    try:
        with open(path, 'w') as f:
            f.write(content)
    except OSError as e:
        raise FileSystemError(f"Failed to write file {path}: {str(e)}") 