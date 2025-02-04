def create_codemagic_config(
    project_name,
    instance_type='mac_mini_m2',
    distribution_type='development',
    xcode_version='latest'
):
    """
    Creates the Codemagic configuration dictionary.
    
    Args:
        project_name (str): The name of the iOS project
        instance_type (str, optional): The Codemagic instance type. Defaults to 'mac_mini_m2'
        distribution_type (str, optional): The iOS distribution type. Defaults to 'development'
        xcode_version (str, optional): The Xcode version to use. Defaults to 'latest'
    
    Returns:
        dict: The Codemagic configuration dictionary
        
    Raises:
        ValueError: If project_name is None or empty
    """
    if not project_name:
        raise ValueError("Project name is required")
        
    return {
        'workflows': {
            'ios-workflow': {
                'name': 'iOS Workflow',
                'instance_type': instance_type,
                'environment': {
                    'xcode': xcode_version,
                    'ios_signing': {
                        'distribution_type': distribution_type,
                        'bundle_identifier': f'com.example.{project_name.lower()}'
                    },
                    'groups': ['ios_credentials']  # For storing certificates and profiles
                },
                'scripts': [
                    {
                        'name': 'Install dependencies',
                        'script': 'xcode-project use-profiles'
                    },
                    {
                        'name': 'Generate Xcode project',
                        'script': 'xcodegen generate'
                    },
                    {
                        'name': 'Build iOS app',
                        'script': f'''
                            xcode-project build-ipa \\
                              --project "$CM_BUILD_DIR/*.xcodeproj" \\
                              --scheme "{project_name}" \\
                              --config Release
                        '''
                    }
                ],
                'artifacts': [
                    'build/ios/ipa/*.ipa',
                    '$HOME/Library/Developer/Xcode/DerivedData/**/Build/**/*.app',
                    '$HOME/Library/Developer/Xcode/DerivedData/**/Build/**/*.dSYM'
                ],
                'publishing': {
                    'email': {
                        'recipients': ['${NOTIFICATION_EMAIL}']
                    }
                }
            }
        }
    } 