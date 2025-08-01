#!/usr/bin/env python3
"""
Fix wagtail.contrib.modeladmin imports for Wagtail 6.0+ compatibility.

This script updates all imports from wagtail.contrib.modeladmin to wagtail_modeladmin
throughout the codebase.
"""

import os
import re
import glob

def fix_modeladmin_imports(filepath):
    """Fix modeladmin imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace import statements
        replacements = [
            # Full module imports
            (r'from wagtail\.contrib\.modeladmin\.options import', 'from wagtail_modeladmin.options import'),
            (r'from wagtail\.contrib\.modeladmin\.helpers import', 'from wagtail_modeladmin.helpers import'),
            (r'from wagtail\.contrib\.modeladmin import', 'from wagtail_modeladmin import'),
            
            # Direct imports
            (r'import wagtail\.contrib\.modeladmin\.options', 'import wagtail_modeladmin.options'),
            (r'import wagtail\.contrib\.modeladmin\.helpers', 'import wagtail_modeladmin.helpers'),
            (r'import wagtail\.contrib\.modeladmin', 'import wagtail_modeladmin'),
        ]
        
        for old_pattern, new_pattern in replacements:
            content = re.sub(old_pattern, new_pattern, content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix all Python files"""
    # Find all Python files in the project
    python_files = []
    
    # Add specific directories to search
    search_dirs = [
        'core',
        'pages', 
        'emails',
        'wagtailpolls',
        'tandem_exams',
        'app',
        'quiz',
        'casetraining',
        'profiles',
        'feedback',
        'dashboard',
        'flashcards'
    ]
    
    for directory in search_dirs:
        if os.path.exists(directory):
            pattern = os.path.join(directory, '**', '*.py')
            python_files.extend(glob.glob(pattern, recursive=True))
    
    # Also check root level Python files
    python_files.extend(glob.glob('*.py'))
    
    print(f"Found {len(python_files)} Python files to check")
    
    updated_files = 0
    for filepath in python_files:
        if fix_modeladmin_imports(filepath):
            updated_files += 1
    
    print(f"\n🎉 Fixed modeladmin imports in {updated_files} files")
    
    if updated_files > 0:
        print("\n📝 Summary of changes:")
        print("- Updated wagtail.contrib.modeladmin imports to wagtail_modeladmin")
        print("- All ModelAdmin functionality should now work with Wagtail 6.0+")
        print("\n⚠️  Next steps:")
        print("1. Test the application to ensure all ModelAdmin functionality works")
        print("2. Run migrations if needed")
        print("3. Update requirements.txt to include wagtail-modeladmin")

if __name__ == "__main__":
    main()
