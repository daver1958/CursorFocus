import os
import json
from typing import Dict, Any, List
from datetime import datetime
import re

class RulesGenerator:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates', 'default.cursorrules.json')
        self.focus_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'Focus.md')

    def _get_timestamp(self) -> str:
        """Get current timestamp in standard format."""
        return datetime.now().strftime('%B %d, %Y at %I:%M %p')

    def generate_rules_file(self, project_info: Dict[str, Any]) -> str:
        """Generate the .cursorrules file based on project analysis."""
        # Load template
        template = self._load_template()
        
        # Customize template
        rules = self._customize_template(template, project_info)
        
        # Write to file
        rules_file = os.path.join(self.project_path, '.cursorrules')
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2)
            
        return rules_file

    def _load_template(self) -> Dict[str, Any]:
        """Load the default template."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading template: {e}")
            return self._get_default_template()

    def _customize_template(self, template: Dict[str, Any], project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Customize the template based on project analysis."""
        rules = template.copy()
        
        # Add timestamp first
        rules['last_updated'] = self._get_timestamp()
        
        # Update project info
        rules['project'].update(project_info)
        
        # Add framework-specific rules
        if project_info['framework'] != 'none':
            framework_rules = self._get_framework_rules(project_info['framework'])
            rules['ai_behavior']['code_generation']['style']['prefer'].extend(framework_rules)
        
        # Add language-specific rules
        language_rules = self._get_language_rules(project_info['language'])
        rules['ai_behavior']['code_generation']['style']['prefer'].extend(language_rules)
        
        # Add project-type specific rules
        self._add_project_type_rules(rules, project_info['type'])
        
        # Update testing frameworks
        rules['ai_behavior']['testing']['frameworks'] = self._detect_testing_frameworks()
        
        # Add Focus.md information
        rules = self._update_rules_with_focus_info(rules)
        
        # Add project configuration
        project_config = self._get_project_config()
        if project_config:
            rules['project'].update(project_config)
        
        return rules

    def _get_framework_rules(self, framework: str) -> List[str]:
        """Get framework-specific coding rules."""
        framework_rules = {
            'react': [
                'use functional components over class components',
                'prefer hooks for state management',
                'use memo for performance optimization',
                'implement proper prop types',
                'use context API appropriately',
                'leverage React.lazy for code splitting',
                'follow component composition patterns'
            ],
            'react-ts': [
                'use proper TypeScript interfaces for props',
                'leverage generic components',
                'use strict prop types with TypeScript',
                'implement proper type guards',
                'use discriminated unions for state',
                'leverage TypeScript utility types',
                'use proper type assertions'
            ],
            'next': [
                'use proper page routing',
                'implement server-side rendering',
                'use proper data fetching methods',
                'leverage Next.js Image component',
                'implement proper dynamic imports',
                'use API routes effectively',
                'follow Next.js project structure'
            ],
            'next-ts': [
                'use TypeScript path aliases',
                'implement proper type-safe API routes',
                'use GetStaticProps/GetServerSideProps types',
                'leverage Next.js TypeScript utilities',
                'implement proper type-safe routing',
                'use proper TypeScript configuration',
                'follow Next.js TypeScript best practices'
            ],
            'vue': [
                'use composition API',
                'prefer ref/reactive for state management',
                'use script setup syntax',
                'implement proper component lifecycle',
                'use proper event handling',
                'leverage Vue directives',
                'follow Vue.js style guide'
            ],
            'vue-ts': [
                'use proper TypeScript decorators',
                'implement type-safe props',
                'use composition API with TypeScript',
                'leverage Vue class components',
                'use proper TypeScript configuration',
                'implement proper type guards',
                'follow Vue.js TypeScript best practices'
            ],
            'angular': [
                'follow angular style guide',
                'use observables for async operations',
                'implement lifecycle hooks properly',
                'use proper dependency injection',
                'implement proper routing',
                'use proper form handling',
                'follow Angular project structure'
            ],
            'django': [
                'follow Django best practices',
                'use class-based views when appropriate',
                'implement proper model relationships'
            ],
            'flask': [
                'use Flask blueprints for organization',
                'implement proper error handling',
                'use Flask-SQLAlchemy for database operations'
            ],
            'laravel': [
                'follow Laravel best practices',
                'use Laravel naming conventions',
                'implement proper model relationships'
            ],
            'symfony': [
                'follow Symfony best practices',
                'use dependency injection',
                'implement proper service architecture'
            ],
            'wordpress': [
                'follow WordPress coding standards',
                'use WordPress hooks properly',
                'implement proper plugin/theme structure'
            ],
            'swiftui': [
                'use SwiftUI view modifiers',
                'implement proper state management',
                'follow SwiftUI lifecycle'
            ],
            'jetpack compose': [
                'use Compose best practices',
                'implement proper state hoisting',
                'follow Compose lifecycle'
            ],
            'spring boot': [
                'follow Spring Boot conventions',
                'use dependency injection',
                'implement proper service architecture'
            ]
        }
        return framework_rules.get(framework.lower(), [])

    def _get_language_rules(self, language: str) -> List[str]:
        """Get language-specific coding rules."""
        language_rules = {
            'python': [
                'follow PEP 8 guidelines',
                'use type hints',
                'prefer list comprehension when appropriate',
                'use context managers for resource handling',
                'leverage decorators for code reuse',
                'use f-strings for string formatting',
                'implement proper exception hierarchies'
            ],
            'javascript': [
                'use modern ES features',
                'prefer arrow functions',
                'use optional chaining',
                'leverage async/await',
                'use destructuring assignment',
                'implement proper error boundaries',
                'use modern module imports'
            ],
            'typescript': [
                'use strict type checking',
                'leverage type inference',
                'use interface over type when possible',
                'implement proper generics',
                'use discriminated unions',
                'leverage utility types',
                'maintain strict null checks',
                'use proper type assertions',
                'implement proper type guards',
                'use proper module declarations',
                'leverage mapped types',
                'use proper enum patterns',
                'implement proper error types',
                'use proper async/await types'
            ],
            'tsx': [
                'use proper component typing',
                'implement proper event handling types',
                'use proper prop types',
                'leverage React TypeScript utilities',
                'use proper hook typing',
                'implement proper context typing',
                'use proper ref typing',
                'leverage conditional types',
                'use proper children typing',
                'implement proper HOC typing',
                'use proper style typing',
                'leverage type-safe routing',
                'use proper form typing',
                'implement proper API types'
            ],
            'java': [
                'follow Java code conventions',
                'use proper access modifiers',
                'implement interface segregation',
                'use builder pattern for complex objects',
                'leverage streams and lambdas',
                'implement proper exception handling',
                'use dependency injection'
            ],
            'go': [
                'follow Go idioms',
                'use proper error handling',
                'implement interfaces implicitly',
                'use goroutines appropriately',
                'leverage channels for communication',
                'follow standard project layout',
                'use context for cancellation'
            ],
            'rust': [
                'follow Rust idioms',
                'use proper ownership patterns',
                'leverage the type system',
                'implement proper error handling',
                'use traits effectively',
                'follow borrowing rules',
                'use cargo workspace structure'
            ],
            'php': [
                'follow PSR standards',
                'use type declarations',
                'implement proper error handling',
                'use modern PHP features',
                'leverage dependency injection',
                'implement interfaces properly',
                'use namespaces effectively'
            ],
            'cpp': [
                'follow modern C++ guidelines',
                'use RAII principles',
                'prefer smart pointers over raw pointers',
                'use const correctness',
                'leverage STL containers and algorithms',
                'implement move semantics',
                'use proper memory management'
            ],
            'csharp': [
                'follow C# coding conventions',
                'use LINQ when appropriate',
                'implement IDisposable pattern when needed',
                'use async/await for asynchronous operations',
                'prefer properties over public fields',
                'leverage dependency injection',
                'use proper exception handling'
            ],
            'ruby': [
                'follow Ruby style guide',
                'use proper block syntax',
                'leverage metaprogramming features',
                'implement proper error handling',
                'use modules for code organization',
                'follow Ruby idioms',
                'use proper gem structure'
            ],
            'kotlin': [
                'follow Kotlin coding conventions',
                'use null safety features',
                'leverage extension functions',
                'use coroutines for async operations',
                'implement proper error handling',
                'use data classes effectively',
                'leverage sealed classes'
            ],
            'swift': [
                'follow Swift API Design Guidelines',
                'use proper access control',
                'leverage Swift type system',
                'use protocol-oriented programming',
                'implement proper error handling',
                'use optionals effectively',
                'leverage value types'
            ]
        }
        return language_rules.get(language.lower(), [])

    def _detect_testing_frameworks(self) -> List[str]:
        """Detect testing frameworks used in the project."""
        testing_frameworks = []
        
        # Check package.json for JS/TS testing frameworks
        package_json_path = os.path.join(self.project_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    
                    # JavaScript/TypeScript testing frameworks
                    if 'jest' in deps:
                        testing_frameworks.append('jest')
                    if '@jest/types' in deps:
                        testing_frameworks.append('jest-typescript')
                    if 'ts-jest' in deps:
                        testing_frameworks.append('ts-jest')
                    if '@testing-library/react' in deps:
                        testing_frameworks.append('testing-library')
                    if '@testing-library/react-hooks' in deps:
                        testing_frameworks.append('testing-library-hooks')
                    if 'cypress' in deps:
                        testing_frameworks.append('cypress')
                    if '@cypress/react' in deps:
                        testing_frameworks.append('cypress-react')
                    if 'vitest' in deps:
                        testing_frameworks.append('vitest')
                    if '@types/mocha' in deps:
                        testing_frameworks.append('mocha-typescript')
            except:
                pass

        # Check requirements.txt for Python testing frameworks
        requirements_path = os.path.join(self.project_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    content = f.read().lower()
                    if 'pytest' in content:
                        testing_frameworks.append('pytest')
                    if 'unittest' in content:
                        testing_frameworks.append('unittest')
            except:
                pass

        # Check for C++ testing frameworks
        if os.path.exists(os.path.join(self.project_path, 'CMakeLists.txt')):
            try:
                with open(os.path.join(self.project_path, 'CMakeLists.txt'), 'r') as f:
                    content = f.read().lower()
                    if 'gtest' in content:
                        testing_frameworks.append('googletest')
                    if 'catch2' in content:
                        testing_frameworks.append('catch2')
                    if 'boost_test' in content:
                        testing_frameworks.append('boost.test')
            except:
                pass

        # Check for C# testing frameworks
        csproj_files = [f for f in os.listdir(self.project_path) if f.endswith('.csproj')]
        for csproj in csproj_files:
            try:
                with open(os.path.join(self.project_path, csproj), 'r') as f:
                    content = f.read().lower()
                    if 'xunit' in content:
                        testing_frameworks.append('xunit')
                    if 'nunit' in content:
                        testing_frameworks.append('nunit')
                    if 'mstest' in content:
                        testing_frameworks.append('mstest')
            except:
                pass

        return testing_frameworks if testing_frameworks else ['jest']  # Default to jest

    def _get_project_type_rules(self, project_type: str) -> Dict[str, Any]:
        """Get project-type specific rules and configurations."""
        type_rules = {
            'web application': {
                'accessibility': {'required': True},
                'performance': {
                    'prefer': [
                        'code splitting',
                        'lazy loading',
                        'performance monitoring',
                        'caching strategies',
                        'responsive design patterns',
                        'progressive enhancement',
                        'proper bundle optimization',
                        'efficient state management',
                        'proper TypeScript configuration',
                        'optimized type checking'
                    ]
                },
                'typescript': {
                    'required': [
                        'strict type checking',
                        'proper tsconfig setup',
                        'type-safe API calls',
                        'proper error handling types',
                        'proper state management types'
                    ]
                },
                'security': {
                    'required': [
                        'CSRF protection',
                        'XSS prevention',
                        'SQL injection prevention',
                        'secure session handling',
                        'input validation'
                    ]
                }
            },
            'mobile application': {
                'performance': {
                    'prefer': [
                        'offline first',
                        'battery optimization',
                        'responsive design',
                        'efficient data caching',
                        'lazy image loading',
                        'background task optimization'
                    ]
                },
                'security': {
                    'required': [
                        'secure data storage',
                        'certificate pinning',
                        'biometric authentication',
                        'app signing',
                        'secure network calls'
                    ]
                }
            },
            'library': {
                'documentation': {
                    'required': True,
                    'include': [
                        'API documentation',
                        'usage examples',
                        'installation guide',
                        'contribution guidelines'
                    ]
                },
                'testing': {
                    'coverage_threshold': 90,
                    'required': [
                        'unit tests',
                        'integration tests',
                        'performance benchmarks',
                        'backwards compatibility tests'
                    ]
                }
            },
            'cli application': {
                'user_experience': {
                    'required': [
                        'clear error messages',
                        'progress indicators',
                        'help documentation',
                        'command completion',
                        'consistent interface'
                    ]
                },
                'performance': {
                    'prefer': [
                        'minimal dependencies',
                        'efficient resource usage',
                        'fast startup time'
                    ]
                }
            },
            'api service': {
                'documentation': {
                    'required': [
                        'API specifications',
                        'endpoint documentation',
                        'authentication guide',
                        'rate limiting details'
                    ]
                },
                'security': {
                    'required': [
                        'authentication',
                        'authorization',
                        'input validation',
                        'rate limiting',
                        'logging and monitoring'
                    ]
                }
            },
            'data science': {
                'code_organization': {
                    'prefer': [
                        'modular pipeline structure',
                        'reproducible experiments',
                        'version controlled datasets',
                        'documented preprocessing steps'
                    ]
                },
                'documentation': {
                    'required': [
                        'methodology documentation',
                        'data dictionaries',
                        'model evaluation metrics',
                        'experiment tracking'
                    ]
                }
            },
            'game': {
                'performance': {
                    'prefer': [
                        'efficient resource loading',
                        'frame rate optimization',
                        'memory management',
                        'asset optimization'
                    ]
                },
                'architecture': {
                    'prefer': [
                        'component-based design',
                        'event-driven systems',
                        'efficient state management',
                        'modular systems'
                    ]
                }
            }
        }
        return type_rules.get(project_type.lower(), {})

    def _add_project_type_rules(self, rules: Dict[str, Any], project_type: str):
        """Add project-type specific rules."""
        specific_rules = self._get_project_type_rules(project_type)
        if specific_rules:
            # Merge with existing rules
            for category, category_rules in specific_rules.items():
                if category in rules['ai_behavior']:
                    # Update existing category
                    rules['ai_behavior'][category].update(category_rules)
                else:
                    # Add new category
                    rules['ai_behavior'][category] = category_rules

    def _get_default_template(self) -> Dict[str, Any]:
        """Get a default template if the template file cannot be loaded."""
        return {
            "version": "1.0",
            "last_updated": self._get_timestamp(),
            "project": {
                "name": "Unknown Project",
                "version": "1.0.0",
                "language": "javascript",
                "framework": "none",
                "type": "application"
            },
            "ai_behavior": {
                "code_generation": {
                    "style": {
                        "prefer": [],
                        "avoid": [
                            "magic numbers",
                            "nested callbacks",
                            "hard-coded values"
                        ]
                    }
                },
                "testing": {
                    "required": True,
                    "frameworks": ["jest"],
                    "coverage_threshold": 80
                }
            }
        } 

    def _get_project_structure_from_focus(self) -> Dict[str, Any]:
        """Extract project structure information from Focus.md."""
        focus_md_path = os.path.join(self.project_path, 'Focus.md')
        if not os.path.exists(focus_md_path):
            return {}
            
        structure_info = {
            "components": [],
            "metrics": {},
            "code_quality": {},
            "key_files": []
        }
        
        try:
            with open(focus_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract components section
            components_match = re.search(r'\*\*Key Components:\*\*\n(.*?)\n\n', content, re.DOTALL)
            if components_match:
                components = components_match.group(1).strip().split('\n')
                structure_info["components"] = [c.strip('├─ └─ │ ').strip() for c in components]
                
            # Extract metrics
            metrics_match = re.search(r'# Project Metrics Summary\n(.*?)\n\n', content, re.DOTALL)
            if metrics_match:
                metrics_text = metrics_match.group(1)
                total_files = re.search(r'Total Files: (\d+)', metrics_text)
                total_lines = re.search(r'Total Lines: ([\d,]+)', metrics_text)
                if total_files:
                    structure_info["metrics"]["total_files"] = int(total_files.group(1))
                if total_lines:
                    structure_info["metrics"]["total_lines"] = int(total_lines.group(1).replace(',', ''))
                    
            # Extract code quality alerts
            quality_match = re.search(r'\*\*Code Quality Alerts:\*\*(.*?)\n\n', content, re.DOTALL)
            if quality_match:
                alerts = quality_match.group(1).strip().split('\n')
                structure_info["code_quality"]["alerts"] = [a.strip('- ').strip() for a in alerts]
                
            # Extract key files with their responsibilities
            files_section = re.findall(r'`([^`]+)`.*?\n\*\*Main Responsibilities:\*\* ([^\n]+)', content)
            structure_info["key_files"] = [{"name": f[0], "responsibility": f[1]} for f in files_section]
                
        except Exception as e:
            print(f"Error parsing Focus.md: {e}")
            
        return structure_info

    def _generate_component_explanations(self, components: List[str]) -> Dict[str, str]:
        """Generate natural language explanations for each component based on its role and purpose."""
        explanations = {}
        
        # Common file type patterns and their explanations
        file_patterns = {
            # Configuration files
            r'.*\.json$': "A configuration file that defines settings and parameters",
            r'.*\.ya?ml$': "A YAML configuration file that defines settings in a human-readable format",
            r'.*\.toml$': "A TOML configuration file that defines project settings and metadata",
            r'.*\.ini$': "An initialization file that stores configuration settings",
            r'.*\.env.*': "An environment configuration file that stores sensitive settings and keys",
            
            # Documentation files
            r'.*\.md$': "A documentation file written in Markdown format",
            r'.*\.rst$': "A documentation file written in reStructuredText format",
            r'.*\.txt$': "A plain text file containing documentation or information",
            r'.*LICENSE.*': "A license file specifying terms of use and distribution",
            r'.*README.*': "A documentation file providing project overview and setup instructions",
            r'.*CHANGELOG.*': "A file tracking version history and changes",
            
            # Source code files by language
            r'.*\.py$': "A Python source code file",
            r'.*\.js$': "A JavaScript source code file",
            r'.*\.ts$': "A TypeScript source code file with type-safe implementations",
            r'.*\.jsx?$': "A React component file",
            r'.*\.tsx?$': "A TypeScript React component",
            r'.*\.vue$': "A Vue.js component file",
            r'.*\.go$': "A Go source code file",
            r'.*\.rs$': "A Rust source code file",
            r'.*\.java$': "A Java source code file",
            r'.*\.kt$': "A Kotlin source code file",
            r'.*\.swift$': "A Swift source code file",
            r'.*\.c$': "A C source code file",
            r'.*\.cpp$': "A C++ source code file",
            r'.*\.cs$': "A C# source code file",
            r'.*\.rb$': "A Ruby source code file",
            r'.*\.php$': "A PHP source code file",
            
            # Build and dependency files
            r'.*requirements.*\.txt$': "A Python dependency specification file",
            r'.*Gemfile$': "A Ruby dependency specification file",
            r'.*package\.json$': "A Node.js project and dependency configuration file",
            r'.*Cargo\.toml$': "A Rust project and dependency configuration file",
            r'.*pom\.xml$': "A Maven project configuration file for Java",
            r'.*build\.gradle.*$': "A Gradle build configuration file",
            r'.*CMakeLists\.txt$': "A CMake build configuration file",
            r'.*Makefile$': "A Make build configuration file",
            
            # Test files
            r'.*test.*\.py$': "A Python test file",
            r'.*spec.*\.js$': "A JavaScript test specification file",
            r'.*test.*\.js$': "A JavaScript test file",
            r'.*test.*\.ts$': "A TypeScript test file",
            r'.*Test\.java$': "A Java test file",
            r'.*_test\.go$': "A Go test file",
            
            # Script files
            r'.*\.sh$': "A shell script for automation and system tasks",
            r'.*\.bat$': "A Windows batch script for automation tasks",
            r'.*\.ps1$': "A PowerShell script for Windows automation",
            
            # Web files
            r'.*\.html?$': "A HTML file defining web page structure",
            r'.*\.css$': "A CSS file defining styles and layouts",
            r'.*\.scss$': "A SASS stylesheet with extended CSS features",
            r'.*\.less$': "A LESS stylesheet with extended CSS features",
            
            # Data files
            r'.*\.sql$': "A SQL file containing database queries and schema",
            r'.*\.csv$': "A comma-separated values data file",
            r'.*\.json$': "A JSON data file storing structured information",
            r'.*\.xml$': "An XML data file storing structured information"
        }
        
        # Directory role patterns
        directory_patterns = {
            r'.*src.*': "Source code directory",
            r'.*test.*': "Test files directory",
            r'.*docs?.*': "Documentation directory",
            r'.*config.*': "Configuration directory",
            r'.*scripts?.*': "Scripts directory",
            r'.*tools?.*': "Development tools directory",
            r'.*assets?.*': "Static assets directory",
            r'.*templates?.*': "Templates directory",
            r'.*public.*': "Public files directory",
            r'.*private.*': "Private resources directory",
            r'.*dist.*': "Distribution directory",
            r'.*build.*': "Build output directory",
            r'.*vendor.*': "Third-party dependencies directory",
            r'.*node_modules.*': "Node.js dependencies directory",
            r'.*venv.*': "Python virtual environment directory",
            r'.*bin.*': "Binary files directory",
            r'.*lib.*': "Library files directory",
            r'.*api.*': "API implementations directory",
            r'.*ui.*': "User interface components directory",
            r'.*utils?.*': "Utility functions directory",
            r'.*helpers?.*': "Helper functions directory",
            r'.*models?.*': "Data models directory",
            r'.*controllers?.*': "Controller logic directory",
            r'.*views?.*': "View components directory",
            r'.*services?.*': "Service implementations directory",
            r'.*middleware.*': "Middleware components directory",
            r'.*migrations?.*': "Database migrations directory",
            r'.*static.*': "Static files directory",
            r'.*media.*': "Media files directory",
            r'.*logs?.*': "Log files directory",
            r'.*cache.*': "Cache directory",
            r'.*backup.*': "Backup files directory"
        }
        
        for component in components:
            clean_name = component.strip().split(' ')[-1]  # Remove emoji and get last part
            
            # Check if it's a directory
            if '\ud83d\udcc1' in component:  # Folder emoji
                explanation = "Project files directory"
                for pattern, desc in directory_patterns.items():
                    if re.search(pattern, clean_name, re.IGNORECASE):
                        explanation = desc
                        break
                explanations[clean_name] = explanation
                continue
            
            # Check file patterns
            explanation = "Project file"
            for pattern, desc in file_patterns.items():
                if re.search(pattern, clean_name, re.IGNORECASE):
                    explanation = desc
                    break
            explanations[clean_name] = explanation
                
        return explanations

    def _update_rules_with_focus_info(self, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Update rules with information from Focus.md."""
        focus_info = self._get_project_structure_from_focus()
        
        if not focus_info:
            return rules
            
        # Generate explanations for components
        component_explanations = self._generate_component_explanations(focus_info.get("components", []))
            
        # Add project structure information with explanations
        rules["project_structure"] = {
            "components": focus_info.get("components", []),
            "component_explanations": component_explanations,
            "metrics": focus_info.get("metrics", {}),
            "code_quality": focus_info.get("code_quality", {}),
            "key_files": focus_info.get("key_files", [])
        }
        
        return rules 

    def _get_project_config(self) -> Dict[str, Any]:
        """Get project configuration from config.json."""
        config_path = os.path.join(self.project_path, 'config.json')
        if not os.path.exists(config_path):
            return {}
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Find current project in config
            current_project = None
            for project in config.get('projects', []):
                if os.path.normpath(project.get('project_path', '')) == os.path.normpath(self.project_path):
                    current_project = project
                    break
                    
            if current_project:
                return {
                    "config": {
                        "update_interval": current_project.get('update_interval', 60),
                        "max_depth": current_project.get('max_depth', 3),
                        "ignored_directories": config.get('ignored_directories', []),
                        "ignored_files": config.get('ignored_files', [])
                    }
                }
                
        except Exception as e:
            print(f"Error reading config.json: {e}")
            
        return {} 