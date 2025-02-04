from flask import Blueprint, request, jsonify, current_app
from .services.github_service import GitHubService
from .services.codemagic_service import CodemagicService
from .services.project_service import ProjectService
from .exceptions import ProjectCreationError

project_creator = Blueprint('project_creator', __name__)

@project_creator.route('/create_project', methods=['POST'])
def create_project():
    """
    Create a new iOS project with GitHub and Codemagic integration.
    
    Expected JSON payload:
    {
        "project_name": "MyAwesomeApp"
    }
    """
    try:
        data = request.get_json()
        project_name = data.get('project_name')
        if not project_name:
            return jsonify({'error': 'Project name is required'}), 400

        # Initialize services
        project_service = ProjectService(current_app.config['WORKSPACE_DIR'])
        github_service = GitHubService(current_app.config['GITHUB_TOKEN'])
        codemagic_service = CodemagicService(current_app.config['CODEMAGIC_API_TOKEN'])

        # Create project files and structure
        project_path = project_service.create_project(project_name)

        # Setup GitHub repository
        repo = github_service.create_and_push_repository(project_name, project_path)

        # Setup Codemagic and start build
        codemagic_app = codemagic_service.setup_project(repo.clone_url)

        return jsonify({
            'message': 'Project created successfully',
            'github_url': repo.html_url,
            'codemagic_app': codemagic_app,
            'build_status': 'Build started automatically. Check Codemagic dashboard for progress.'
        })

    except ProjectCreationError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@project_creator.route('/start_build', methods=['POST'])
def start_build():
    """
    Start a new build for an existing project.
    
    Expected JSON payload:
    {
        "app_id": "codemagic_app_id",  # The Codemagic app ID
        "branch": "main"               # Optional: The branch to build (defaults to main)
    }
    """
    try:
        data = request.get_json()
        app_id = data.get('app_id')
        branch = data.get('branch', 'main')

        if not app_id:
            return jsonify({'error': 'Codemagic app ID is required'}), 400

        # Initialize Codemagic service
        codemagic_service = CodemagicService(current_app.config['CODEMAGIC_API_TOKEN'])

        # Start the build
        build = codemagic_service.start_build(app_id, branch)

        return jsonify({
            'message': 'Build started successfully',
            'build': build
        })

    except Exception as e:
        return jsonify({'error': f'Failed to start build: {str(e)}'}), 500 