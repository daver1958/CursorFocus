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
        rules['project'].update({
            'type': project_info.get('type', 'generic'),
            'language': project_info.get('language', 'unknown'),
            'framework': project_info.get('framework', 'none'),
            'description': project_info.get('description', 'Generic Project')
        })
        
        # Add framework-specific rules
        if project_info.get('framework') != 'none':
            framework_rules = self._get_framework_rules(project_info['framework'])
            rules['ai_behavior']['code_generation']['style']['prefer'].extend(framework_rules)
        
        # Add language-specific rules
        language_rules = self._get_language_rules(project_info.get('language', 'unknown'))
        rules['ai_behavior']['code_generation']['style']['prefer'].extend(language_rules)
        
        # Add project-type specific rules
        self._add_project_type_rules(rules, project_info.get('type', 'generic'))
        
        # Update testing frameworks
        rules['ai_behavior']['testing']['frameworks'] = self._detect_testing_frameworks()
        
        # Add Focus.md information
        rules = self._update_rules_with_focus_info(rules)
        
        # Add project configuration
        project_config = self._get_project_config()
        if project_config:
            rules['project'].update(project_config)
        
        # Add new AI behavior rules
        rules['ai_behavior'].update({
            'code_review': {
                'focus_areas': [
                    'security vulnerabilities',
                    'performance bottlenecks',
                    'code maintainability',
                    'test coverage',
                    'documentation quality'
                ],
                'review_checklist': [
                    'check for proper error handling',
                    'verify input validation',
                    'assess code complexity',
                    'review naming conventions',
                    'evaluate test quality'
                ]
            },
            'documentation': {
                'required_sections': [
                    'overview',
                    'installation',
                    'usage',
                    'api reference',
                    'contributing guidelines'
                ],
                'code_comments': {
                    'require_docstrings': True,
                    'require_type_hints': True,
                    'require_examples': True
                }
            },
            'refactoring': {
                'triggers': [
                    'code duplication',
                    'complex conditionals',
                    'long methods',
                    'large classes',
                    'tight coupling'
                ],
                'strategies': [
                    'extract method',
                    'extract class',
                    'introduce parameter object',
                    'replace conditional with polymorphism',
                    'introduce interface'
                ]
            },
            'optimization': {
                'metrics': [
                    'execution time',
                    'memory usage',
                    'network latency',
                    'database performance',
                    'resource utilization'
                ],
                'strategies': [
                    'caching',
                    'lazy loading',
                    'connection pooling',
                    'query optimization',
                    'asynchronous processing'
                ]
            }
        })
        
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
                'follow component composition patterns',
                'implement proper error boundaries',
                'use proper state management patterns',
                'follow React performance best practices',
                'implement proper form handling',
                'use proper routing strategies',
                'follow proper security practices'
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
            ],
            'fastapi': [
                'use proper dependency injection',
                'implement async/await patterns',
                'use proper path operations',
                'implement proper security middleware',
                'use proper response models',
                'follow FastAPI best practices',
                'implement proper error handling'
            ],
            'express': [
                'use proper middleware patterns',
                'implement proper route handlers',
                'use proper error handling',
                'implement proper authentication',
                'follow Express.js best practices',
                'use proper database integration',
                'implement proper API versioning'
            ],
            'nest': [
                'use proper decorators',
                'implement proper dependency injection',
                'use proper module structure',
                'follow NestJS architecture patterns',
                'implement proper guards and interceptors',
                'use proper exception filters',
                'follow proper testing practices'
            ],
            'nuxt': [
                'use proper Nuxt.js modules',
                'implement proper SSR strategies',
                'use proper routing patterns',
                'follow Nuxt.js directory structure',
                'implement proper state management',
                'use proper middleware',
                'follow Nuxt.js best practices'
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
                'implement proper exception hierarchies',
                'use proper async/await patterns',
                'follow proper package structure',
                'implement proper logging',
                'use proper dependency management',
                'follow proper testing practices',
                'implement proper configuration management'
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
                'implement proper error handling',
                'use proper trait implementations',
                'follow memory safety guidelines',
                'use proper macro patterns',
                'implement proper async patterns'
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
                'use proper null safety',
                'implement proper coroutines',
                'use proper extension functions',
                'follow Kotlin idioms',
                'implement proper data classes',
                'use proper scope functions',
                'follow proper functional programming patterns'
            ],
            'swift': [
                'use proper optionals',
                'implement proper protocols',
                'use proper value types',
                'follow Swift idioms',
                'implement proper error handling',
                'use proper memory management',
                'follow proper concurrency patterns'
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
        """Get project structure information from Focus.md."""
        try:
            with open(os.path.join(self.project_path, 'Focus.md'), 'r', encoding='utf-8') as f:
                content = f.read()
                
            structure = {
                'components': [],
                'component_explanations': {},
                'metrics': {
                    'total_files': 0,
                    'total_lines': 0
                },
                'code_quality': {
                    'alerts': []
                },
                'key_files': [],
                'architecture': {
                    'layers': [],
                    'dependencies': [],
                    'patterns': []
                },
                'documentation': {
                    'coverage': 0,
                    'quality_score': 0,
                    'missing_sections': []
                },
                'testing': {
                    'coverage': 0,
                    'passing_rate': 0,
                    'critical_paths': []
                }
            }
                
            # Extract components section
            components_match = re.search(r'\*\*Key Components:\*\*\n(.*?)\n\n', content, re.DOTALL)
            if components_match:
                components = components_match.group(1).strip().split('\n')
                structure["components"] = [c.strip('├─ └─ │ ').strip() for c in components]
                
            # Extract metrics
            metrics_match = re.search(r'# Project Metrics Summary\n(.*?)\n\n', content, re.DOTALL)
            if metrics_match:
                metrics_text = metrics_match.group(1)
                total_files = re.search(r'Total Files: (\d+)', metrics_text)
                total_lines = re.search(r'Total Lines: ([\d,]+)', metrics_text)
                if total_files:
                    structure["metrics"]["total_files"] = int(total_files.group(1))
                if total_lines:
                    structure["metrics"]["total_lines"] = int(total_lines.group(1).replace(',', ''))
                    
            # Extract code quality alerts
            quality_match = re.search(r'\*\*Code Quality Alerts:\*\*(.*?)\n\n', content, re.DOTALL)
            if quality_match:
                alerts = quality_match.group(1).strip().split('\n')
                structure["code_quality"]["alerts"] = [a.strip('- ').strip() for a in alerts]
                
            # Extract key files with their responsibilities
            files_section = re.findall(r'`([^`]+)`.*?\n\*\*Main Responsibilities:\*\* ([^\n]+)', content)
            structure["key_files"] = [{"name": f[0], "responsibility": f[1]} for f in files_section]
                
            # Extract architecture section
            architecture_match = re.search(r'\*\*Architecture:\*\*\n(.*?)\n\n', content, re.DOTALL)
            if architecture_match:
                architecture_text = architecture_match.group(1)
                layers_match = re.search(r'Layers:\n(.*?)\n\n', architecture_text)
                if layers_match:
                    layers = layers_match.group(1).strip().split('\n')
                    structure["architecture"]["layers"] = [l.strip() for l in layers]
                
                dependencies_match = re.search(r'Dependencies:\n(.*?)\n\n', architecture_text)
                if dependencies_match:
                    dependencies = dependencies_match.group(1).strip().split('\n')
                    structure["architecture"]["dependencies"] = [d.strip() for d in dependencies]
                
                patterns_match = re.search(r'Patterns:\n(.*?)\n\n', architecture_text)
                if patterns_match:
                    patterns = patterns_match.group(1).strip().split('\n')
                    structure["architecture"]["patterns"] = [p.strip() for p in patterns]
                
            # Extract documentation section
            documentation_match = re.search(r'\*\*Documentation:\*\*\n(.*?)\n\n', content, re.DOTALL)
            if documentation_match:
                documentation_text = documentation_match.group(1)
                coverage_match = re.search(r'Coverage: (\d+)%', documentation_text)
                if coverage_match:
                    structure["documentation"]["coverage"] = int(coverage_match.group(1))
                
                quality_score_match = re.search(r'Quality Score: (\d+)', documentation_text)
                if quality_score_match:
                    structure["documentation"]["quality_score"] = int(quality_score_match.group(1))
                
                missing_sections_match = re.findall(r'- (.*)', documentation_text)
                if missing_sections_match:
                    structure["documentation"]["missing_sections"] = [s.strip() for s in missing_sections_match]
                
            # Extract testing section
            testing_match = re.search(r'\*\*Testing:\*\*\n(.*?)\n\n', content, re.DOTALL)
            if testing_match:
                testing_text = testing_match.group(1)
                coverage_match = re.search(r'Coverage: (\d+)%', testing_text)
                if coverage_match:
                    structure["testing"]["coverage"] = int(coverage_match.group(1))
                
                passing_rate_match = re.search(r'Passing Rate: (\d+)%', testing_text)
                if passing_rate_match:
                    structure["testing"]["passing_rate"] = int(passing_rate_match.group(1))
                
                critical_paths_match = re.findall(r'- (.*)', testing_text)
                if critical_paths_match:
                    structure["testing"]["critical_paths"] = [p.strip() for p in critical_paths_match]
                
            return structure
        except Exception as e:
            print(f"Error reading Focus.md: {e}")
            return {}

    def _generate_component_explanations(self, components: List[str]) -> Dict[str, str]:
        """Generate natural language explanations for each component based on its role and purpose."""
        explanations = {}
        
        # Common file type patterns and their explanations
        file_patterns = {
            # Configuration files
            r'.*\.json$': "A JSON configuration file that defines application settings, dependencies, and project metadata in a structured format",
            r'.*\.ya?ml$': "A YAML configuration file that defines application settings and infrastructure configurations in a human-readable format",
            r'.*\.toml$': "A TOML configuration file that defines project settings, dependencies, and build configurations with strong typing",
            r'.*\.ini$': "An initialization file that stores application configuration settings in a simple key-value format",
            r'.*\.env.*': "An environment configuration file that securely stores sensitive settings, API keys, and environment-specific variables",
            r'.*\.config.*': "A configuration file that defines application settings, build options, and runtime parameters",
            
            # Documentation files
            r'.*\.md$': "A Markdown documentation file providing project information, guides, and technical documentation in a readable format",
            r'.*\.rst$': "A reStructuredText documentation file offering detailed technical documentation with advanced formatting features",
            r'.*\.txt$': "A plain text file containing project documentation, notes, or general information in a simple format",
            r'.*LICENSE.*': "A license file specifying the terms of use, distribution, and legal requirements for the project",
            r'.*README.*': "A comprehensive documentation file providing project overview, setup instructions, and usage guidelines",
            r'.*CHANGELOG.*': "A detailed log file tracking version history, feature additions, bug fixes, and breaking changes",
            r'.*CONTRIBUTING.*': "A guide outlining contribution guidelines, coding standards, and development workflow for contributors",
            r'.*CODE_OF_CONDUCT.*': "A document defining community standards, expected behavior, and guidelines for project participation",
            
            # Source code files by language
            r'.*\.py$': "A Python source code file implementing application logic, classes, and functions with type hints and documentation",
            r'.*\.pyi$': "A Python interface file defining type hints and function signatures for improved type checking",
            r'.*\.js$': "A JavaScript source code file implementing client-side or server-side functionality with modern ES features",
            r'.*\.ts$': "A TypeScript source code file providing type-safe implementations with interfaces and advanced type features",
            r'.*\.jsx?$': "A React component file implementing UI components with JSX syntax and component lifecycle management",
            r'.*\.tsx?$': "A TypeScript React component providing type-safe UI implementations with proper prop typing",
            r'.*\.vue$': "A Vue.js component file implementing self-contained components with template, script, and style sections",
            r'.*\.go$': "A Go source code file implementing efficient and concurrent functionality with strong type safety",
            r'.*\.rs$': "A Rust source code file providing memory-safe implementations with ownership system and zero-cost abstractions",
            r'.*\.java$': "A Java source code file implementing object-oriented functionality with strong typing and platform independence",
            r'.*\.kt$': "A Kotlin source code file offering modern language features with Java interoperability and null safety",
            r'.*\.swift$': "A Swift source code file implementing iOS/macOS functionality with modern syntax and strong type safety",
            r'.*\.c$': "A C source code file implementing low-level system functionality with manual memory management",
            r'.*\.cpp$': "A C++ source code file providing object-oriented implementations with modern C++ features and STL",
            r'.*\.cs$': "A C# source code file implementing .NET functionality with modern language features and type safety",
            r'.*\.rb$': "A Ruby source code file offering dynamic programming with elegant syntax and metaprogramming features",
            r'.*\.php$': "A PHP source code file implementing server-side functionality with modern PHP features and type declarations",
            
            # Build and dependency files
            r'.*requirements.*\.txt$': "A Python dependency specification file listing required packages with version constraints",
            r'.*Pipfile$': "A modern Python dependency management file using Pipenv for deterministic dependencies",
            r'.*poetry\.toml$': "A Poetry configuration file for Python dependency management with advanced features",
            r'.*Gemfile$': "A Ruby dependency specification file managing gem dependencies with Bundler",
            r'.*package\.json$': "A Node.js project configuration file managing dependencies, scripts, and project metadata",
            r'.*package-lock\.json$': "A detailed dependency lock file ensuring consistent installations across environments",
            r'.*yarn\.lock$': "A Yarn dependency lock file providing deterministic dependency resolution",
            r'.*Cargo\.toml$': "A Rust project configuration file managing dependencies and build settings",
            r'.*Cargo\.lock$': "A Rust dependency lock file ensuring reproducible builds across environments",
            r'.*pom\.xml$': "A Maven project configuration file managing Java dependencies and build lifecycle",
            r'.*build\.gradle.*$': "A Gradle build configuration file defining build logic and dependencies with Groovy/Kotlin DSL",
            r'.*CMakeLists\.txt$': "A CMake build configuration file defining build system generation for C/C++ projects",
            r'.*Makefile$': "A Make build configuration file defining build rules and dependencies",
            
            # Test files
            r'.*test.*\.py$': "A Python test file containing unit tests, integration tests, and test fixtures",
            r'.*conftest\.py$': "A pytest configuration file defining shared test fixtures and configuration",
            r'.*spec.*\.js$': "A JavaScript test specification file using behavior-driven development patterns",
            r'.*test.*\.js$': "A JavaScript test file implementing unit and integration tests",
            r'.*test.*\.ts$': "A TypeScript test file with type-safe test implementations",
            r'.*Test\.java$': "A Java test file implementing JUnit tests with assertions and test lifecycle",
            r'.*_test\.go$': "A Go test file implementing table-driven tests and benchmarks",
            r'.*\.spec\.ts$': "A TypeScript test specification file with type-safe test implementations",
            
            # Script files
            r'.*\.sh$': "A shell script automating system tasks and deployment processes",
            r'.*\.bat$': "A Windows batch script automating Windows-specific tasks",
            r'.*\.ps1$': "A PowerShell script implementing advanced Windows automation",
            r'.*\.bash.*$': "A Bash script providing Unix shell automation with advanced features",
            r'.*\.zsh.*$': "A Zsh script implementing shell automation with extended features",
            
            # Web files
            r'.*\.html?$': "A HTML file defining web page structure and content with semantic markup",
            r'.*\.css$': "A CSS file implementing styles and responsive layouts with modern features",
            r'.*\.scss$': "A SASS stylesheet implementing modular styles with variables and mixins",
            r'.*\.less$': "A LESS stylesheet providing dynamic styles with variables and functions",
            r'.*\.styl$': "A Stylus stylesheet offering expressive styling with advanced features",
            r'.*\.svg$': "A scalable vector graphics file defining resolution-independent graphics",
            
            # Data files
            r'.*\.sql$': "A SQL file containing database schema definitions and complex queries",
            r'.*\.csv$': "A comma-separated values file storing tabular data in a text format",
            r'.*\.json$': "A JSON data file storing structured data with nested objects and arrays",
            r'.*\.xml$': "An XML data file storing hierarchical data with schema validation",
            r'.*\.proto$': "A Protocol Buffers definition file for efficient data serialization",
            r'.*\.graphql$': "A GraphQL schema file defining API types and operations",
            r'.*\.avro$': "An Apache Avro data file for efficient data serialization",
            r'.*\.parquet$': "A Parquet columnar storage file optimized for big data processing"
        }
        
        # Directory role patterns
        directory_patterns = {
            r'.*src.*': "Source code directory containing the main application implementation files",
            r'.*test.*': "Test directory containing unit tests, integration tests, and test resources",
            r'.*docs?.*': "Documentation directory storing project documentation, guides, and API references",
            r'.*config.*': "Configuration directory containing various application and environment configurations",
            r'.*scripts?.*': "Scripts directory containing automation scripts and development tools",
            r'.*tools?.*': "Development tools directory containing utilities and helper scripts",
            r'.*assets?.*': "Assets directory storing static resources like images, fonts, and media files",
            r'.*templates?.*': "Templates directory containing reusable template files and code generators",
            r'.*public.*': "Public directory containing publicly accessible static files and resources",
            r'.*private.*': "Private directory storing sensitive resources and internal configurations",
            r'.*dist.*': "Distribution directory containing built and optimized production files",
            r'.*build.*': "Build directory containing compilation outputs and build artifacts",
            r'.*vendor.*': "Third-party dependencies directory managed by package managers",
            r'.*node_modules.*': "Node.js dependencies directory containing installed npm packages",
            r'.*venv.*': "Python virtual environment directory isolating project dependencies",
            r'.*bin.*': "Binary directory containing executable files and compiled outputs",
            r'.*lib.*': "Library directory containing shared code libraries and modules",
            r'.*api.*': "API directory implementing backend services and API endpoints",
            r'.*ui.*': "User interface directory containing frontend components and layouts",
            r'.*utils?.*': "Utilities directory containing helper functions and shared code",
            r'.*helpers?.*': "Helpers directory providing utility functions and common operations",
            r'.*models?.*': "Models directory containing data models and database schemas",
            r'.*controllers?.*': "Controllers directory implementing business logic and request handling",
            r'.*views?.*': "Views directory containing UI templates and view components",
            r'.*services?.*': "Services directory implementing business logic and external integrations",
            r'.*middleware.*': "Middleware directory containing request/response processing components",
            r'.*migrations?.*': "Migrations directory managing database schema changes and data migrations",
            r'.*static.*': "Static files directory containing unchanging assets and resources",
            r'.*media.*': "Media directory storing user-uploaded files and media content",
            r'.*logs?.*': "Logs directory containing application logs and error tracking",
            r'.*cache.*': "Cache directory storing temporary data for performance optimization",
            r'.*backup.*': "Backup directory containing data backups and recovery files",
            r'.*hooks?.*': "Hooks directory containing Git hooks and event handlers",
            r'.*plugins?.*': "Plugins directory containing extensible plugin implementations",
            r'.*packages?.*': "Packages directory managing multiple related packages in a monorepo",
            r'.*modules?.*': "Modules directory containing modular application components",
            r'.*components?.*': "Components directory storing reusable UI components",
            r'.*layouts?.*': "Layouts directory containing page layouts and templates",
            r'.*pages?.*': "Pages directory implementing route-based page components",
            r'.*styles?.*': "Styles directory containing CSS and styling resources",
            r'.*themes?.*': "Themes directory managing different visual themes",
            r'.*locales?.*': "Locales directory containing internationalization resources",
            r'.*constants?.*': "Constants directory defining shared constant values",
            r'.*types?.*': "Types directory containing TypeScript type definitions",
            r'.*interfaces?.*': "Interfaces directory defining TypeScript interfaces",
            r'.*contexts?.*': "Contexts directory implementing React context providers",
            r'.*reducers?.*': "Reducers directory containing state management logic",
            r'.*actions?.*': "Actions directory defining state management actions",
            r'.*store.*': "Store directory implementing state management configuration",
            r'.*fixtures?.*': "Fixtures directory containing test data and mock objects",
            r'.*mocks?.*': "Mocks directory containing mock implementations for testing",
            r'.*coverage.*': "Coverage directory containing test coverage reports",
            r'.*reports?.*': "Reports directory storing various analysis reports",
            r'.*examples?.*': "Examples directory containing sample code and usage examples",
            r'.*tutorials?.*': "Tutorials directory providing learning resources and guides"
        }
        
        for component in components:
            clean_name = component.strip().split(' ')[-1]  # Remove emoji and get last part
            
            # Check if it's a directory
            if '\ud83d\udcc1' in component:  # Folder emoji
                explanation = "Project directory containing related files and resources"
                for pattern, desc in directory_patterns.items():
                    if re.search(pattern, clean_name, re.IGNORECASE):
                        explanation = desc
                        break
                explanations[clean_name] = explanation
                continue
            
            # Check file patterns
            explanation = "Project file containing application code or resources"
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