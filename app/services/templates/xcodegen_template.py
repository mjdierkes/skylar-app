def create_xcodegen_config(project_name, bundle_id_prefix=None, deployment_target='15.0'):
    """
    Creates the XcodeGen configuration dictionary.
    
    Args:
        project_name (str): The name of the iOS project
        bundle_id_prefix (str, optional): The bundle ID prefix. Defaults to com.example
        deployment_target (str, optional): The minimum iOS version. Defaults to '15.0'
    
    Returns:
        dict: The XcodeGen configuration dictionary
    """
    if not project_name:
        raise ValueError("Project name is required")
        
    bundle_id_prefix = bundle_id_prefix or f'com.example'
    
    return {
        'name': project_name,
        'options': {
            'bundleIdPrefix': f'{bundle_id_prefix}.{project_name.lower()}'
        },
        'targets': {
            project_name: {
                'type': 'application',
                'platform': 'iOS',
                'deploymentTarget': deployment_target,
                'sources': ['Sources'],
                'info': {
                    'path': 'Info.plist',
                    'properties': {
                        'CFBundleShortVersionString': '1.0.0',
                        'CFBundleVersion': '1',
                        'UIMainStoryboardFile': '',
                        'UILaunchStoryboardName': 'LaunchScreen',
                        'UIApplicationSceneManifest': {
                            'UIApplicationSupportsMultipleScenes': False,
                            'UISceneConfigurations': {}
                        }
                    }
                }
            }
        }
    } 