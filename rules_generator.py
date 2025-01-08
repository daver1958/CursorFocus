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
                'follow proper security practices',
                'use proper data fetching patterns',
                'implement proper authentication flow',
                'use proper caching strategies',
                'follow proper testing practices',
                'implement proper SEO practices',
                'use proper accessibility patterns',
                'follow proper deployment practices'
            ],
            'react-ts': [
                'use proper TypeScript interfaces for props',
                'leverage generic components',
                'use strict prop types with TypeScript',
                'implement proper type guards',
                'use discriminated unions for state',
                'leverage TypeScript utility types',
                'use proper type assertions',
                'implement proper error type handling',
                'use proper async type patterns',
                'follow TypeScript best practices',
                'use proper module declarations',
                'implement proper type testing',
                'use proper type inference',
                'follow proper type organization',
                'implement proper type documentation'
            ],
            'next': [
                'use proper page routing',
                'implement server-side rendering',
                'use proper data fetching methods',
                'leverage Next.js Image component',
                'implement proper dynamic imports',
                'use API routes effectively',
                'follow Next.js project structure',
                'implement proper middleware',
                'use proper caching strategies',
                'follow proper deployment practices',
                'implement proper authentication',
                'use proper environment variables',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper SEO practices'
            ],
            'next-ts': [
                'use TypeScript path aliases',
                'implement proper type-safe API routes',
                'use GetStaticProps/GetServerSideProps types',
                'leverage Next.js TypeScript utilities',
                'implement proper type-safe routing',
                'use proper TypeScript configuration',
                'follow Next.js TypeScript best practices',
                'implement proper type testing',
                'use proper type inference',
                'follow proper type organization',
                'implement proper type documentation',
                'use proper module declarations',
                'follow proper type safety practices'
            ],
            'vue': [
                'use composition API',
                'prefer ref/reactive for state management',
                'use script setup syntax',
                'implement proper component lifecycle',
                'use proper event handling',
                'leverage Vue directives',
                'follow Vue.js style guide',
                'implement proper routing',
                'use proper state management',
                'follow proper testing practices',
                'implement proper form handling',
                'use proper component communication',
                'follow proper security practices',
                'implement proper error handling',
                'use proper performance optimization'
            ],
            'vue-ts': [
                'use proper TypeScript decorators',
                'implement type-safe props',
                'use composition API with TypeScript',
                'leverage Vue class components',
                'use proper TypeScript configuration',
                'implement proper type guards',
                'follow Vue.js TypeScript best practices',
                'use proper type inference',
                'implement proper type testing',
                'follow proper type organization',
                'use proper module declarations',
                'implement proper type documentation',
                'follow proper type safety practices'
            ],
            'angular': [
                'follow angular style guide',
                'use observables for async operations',
                'implement lifecycle hooks properly',
                'use proper dependency injection',
                'implement proper routing',
                'use proper form handling',
                'follow Angular project structure',
                'implement proper services',
                'use proper component communication',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper state management',
                'follow proper security practices',
                'implement proper performance optimization',
                'use proper lazy loading'
            ],
            'django': [
                'follow Django best practices',
                'use class-based views when appropriate',
                'implement proper model relationships',
                'use proper form handling',
                'implement proper authentication',
                'use proper middleware',
                'follow proper security practices',
                'implement proper caching',
                'use proper database optimization',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper static files handling',
                'follow proper deployment practices',
                'implement proper API design',
                'use proper template inheritance'
            ],
            'flask': [
                'use Flask blueprints for organization',
                'implement proper error handling',
                'use Flask-SQLAlchemy for database operations',
                'implement proper authentication',
                'use proper request handling',
                'follow proper security practices',
                'implement proper caching',
                'use proper configuration management',
                'follow proper testing practices',
                'implement proper logging',
                'use proper database migration',
                'follow proper deployment practices',
                'implement proper API design',
                'use proper template organization'
            ],
            'laravel': [
                'follow Laravel best practices',
                'use Laravel naming conventions',
                'implement proper model relationships',
                'use proper middleware',
                'implement proper authentication',
                'use proper request validation',
                'follow proper security practices',
                'implement proper caching',
                'use proper database optimization',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper queue management',
                'follow proper deployment practices',
                'implement proper API design',
                'use proper blade templates'
            ],
            'symfony': [
                'follow Symfony best practices',
                'use dependency injection',
                'implement proper service architecture',
                'use proper routing',
                'implement proper authentication',
                'use proper form handling',
                'follow proper security practices',
                'implement proper caching',
                'use proper database optimization',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper event handling',
                'follow proper deployment practices',
                'implement proper API design',
                'use proper twig templates'
            ],
            'wordpress': [
                'follow WordPress coding standards',
                'use WordPress hooks properly',
                'implement proper plugin/theme structure',
                'use proper database queries',
                'implement proper security measures',
                'use proper template hierarchy',
                'follow proper performance practices',
                'implement proper error handling',
                'use proper internationalization',
                'follow proper testing practices',
                'implement proper caching',
                'use proper asset management',
                'follow proper deployment practices',
                'implement proper custom post types',
                'use proper taxonomies'
            ],
            'swiftui': [
                'use SwiftUI view modifiers',
                'implement proper state management',
                'follow SwiftUI lifecycle',
                'use proper data flow',
                'implement proper navigation',
                'use proper animations',
                'follow proper performance practices',
                'implement proper error handling',
                'use proper accessibility',
                'follow proper testing practices',
                'implement proper localization',
                'use proper asset management',
                'follow proper deployment practices',
                'implement proper custom views',
                'use proper gestures'
            ],
            'jetpack compose': [
                'use Compose best practices',
                'implement proper state hoisting',
                'follow Compose lifecycle',
                'use proper composables',
                'implement proper navigation',
                'use proper animations',
                'follow proper performance practices',
                'implement proper error handling',
                'use proper accessibility',
                'follow proper testing practices',
                'implement proper theming',
                'use proper asset management',
                'follow proper deployment practices',
                'implement proper custom layouts',
                'use proper gestures'
            ],
            'spring boot': [
                'follow Spring Boot conventions',
                'use dependency injection',
                'implement proper service architecture',
                'use proper repository pattern',
                'implement proper security',
                'use proper validation',
                'follow proper testing practices',
                'implement proper error handling',
                'use proper caching',
                'follow proper deployment practices',
                'implement proper logging',
                'use proper configuration',
                'follow proper documentation practices',
                'implement proper API design',
                'use proper database migration'
            ],
            'fastapi': [
                'use proper dependency injection',
                'implement async/await patterns',
                'use proper path operations',
                'implement proper security middleware',
                'use proper response models',
                'follow FastAPI best practices',
                'implement proper error handling',
                'use proper validation',
                'follow proper testing practices',
                'implement proper documentation',
                'use proper database integration',
                'follow proper deployment practices',
                'implement proper API versioning',
                'use proper background tasks',
                'follow proper logging practices'
            ],
            'express': [
                'use proper middleware patterns',
                'implement proper route handlers',
                'use proper error handling',
                'implement proper authentication',
                'follow Express.js best practices',
                'use proper database integration',
                'implement proper API versioning',
                'use proper validation',
                'follow proper testing practices',
                'implement proper logging',
                'use proper security measures',
                'follow proper deployment practices',
                'implement proper rate limiting',
                'use proper caching strategies',
                'follow proper documentation practices'
            ],
            'nest': [
                'use proper decorators',
                'implement proper dependency injection',
                'use proper module structure',
                'follow NestJS architecture patterns',
                'implement proper guards and interceptors',
                'use proper exception filters',
                'follow proper testing practices',
                'implement proper validation',
                'use proper database integration',
                'follow proper documentation practices',
                'implement proper caching',
                'use proper security measures',
                'follow proper deployment practices',
                'implement proper microservices',
                'use proper logging'
            ],
            'nuxt': [
                'use proper Nuxt.js modules',
                'implement proper SSR strategies',
                'use proper routing patterns',
                'follow Nuxt.js directory structure',
                'implement proper state management',
                'use proper middleware',
                'follow Nuxt.js best practices',
                'implement proper error handling',
                'use proper SEO practices',
                'follow proper testing practices',
                'implement proper authentication',
                'use proper caching strategies',
                'follow proper deployment practices',
                'implement proper internationalization',
                'use proper asset optimization'
            ],
            'gatsby': [
                'use proper Gatsby plugins',
                'implement proper data sourcing',
                'use proper GraphQL queries',
                'follow Gatsby project structure',
                'implement proper image optimization',
                'use proper SEO practices',
                'follow proper performance practices',
                'implement proper routing',
                'use proper state management',
                'follow proper testing practices',
                'implement proper authentication',
                'use proper build optimization',
                'follow proper deployment practices',
                'implement proper internationalization',
                'use proper asset management'
            ],
            'svelte': [
                'use proper component structure',
                'implement proper state management',
                'use proper reactivity patterns',
                'follow Svelte best practices',
                'implement proper transitions',
                'use proper stores',
                'follow proper testing practices',
                'implement proper routing',
                'use proper form handling',
                'follow proper performance practices',
                'implement proper error handling',
                'use proper TypeScript integration',
                'follow proper deployment practices',
                'implement proper accessibility',
                'use proper animation patterns'
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
                'implement proper configuration management',
                'use proper docstring format',
                'follow proper import organization',
                'implement proper class inheritance',
                'use proper property decorators',
                'follow proper metaclass usage',
                'implement proper iterator patterns',
                'use proper generator patterns',
                'follow proper memory management',
                'implement proper concurrency patterns',
                'use proper serialization methods',
                'follow proper database access patterns',
                'implement proper CLI interfaces'
            ],
            'javascript': [
                'use modern ES features',
                'prefer arrow functions',
                'use optional chaining',
                'leverage async/await',
                'use destructuring assignment',
                'implement proper error boundaries',
                'use modern module imports',
                'follow proper promise patterns',
                'implement proper event handling',
                'use proper closure patterns',
                'follow proper prototype usage',
                'implement proper memory management',
                'use proper regex patterns',
                'follow proper DOM manipulation',
                'implement proper web APIs usage',
                'use proper data structures',
                'follow proper security practices',
                'implement proper error handling',
                'use proper debugging techniques',
                'follow proper performance optimization'
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
                'use proper async/await types',
                'follow proper type organization',
                'implement proper decorator patterns',
                'use proper namespace organization',
                'follow proper type inheritance',
                'implement proper conditional types',
                'use proper index types'
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
                'implement proper API types',
                'follow proper component organization',
                'use proper state management types',
                'implement proper test typing',
                'use proper animation typing',
                'follow proper accessibility typing',
                'implement proper error boundary types'
            ],
            'java': [
                'follow Java code conventions',
                'use proper access modifiers',
                'implement interface segregation',
                'use builder pattern for complex objects',
                'leverage streams and lambdas',
                'implement proper exception handling',
                'use dependency injection',
                'follow proper package organization',
                'implement proper generics usage',
                'use proper collection frameworks',
                'follow proper thread safety',
                'implement proper serialization',
                'use proper logging frameworks',
                'follow proper testing practices',
                'implement proper resource management',
                'use proper annotation processing',
                'follow proper memory management',
                'implement proper IO handling',
                'use proper security practices',
                'follow proper documentation'
            ],
            'go': [
                'follow Go idioms',
                'use proper error handling',
                'implement interfaces implicitly',
                'use goroutines appropriately',
                'leverage channels for communication',
                'follow standard project layout',
                'use context for cancellation',
                'implement proper package organization',
                'use proper pointer semantics',
                'follow proper concurrency patterns',
                'implement proper testing practices',
                'use proper logging patterns',
                'follow proper error wrapping',
                'implement proper dependency management',
                'use proper interface design',
                'follow proper documentation',
                'implement proper middleware patterns',
                'use proper struct composition',
                'follow proper memory management',
                'implement proper HTTP handlers'
            ],
            'rust': [
                'follow Rust idioms',
                'use proper ownership patterns',
                'implement proper error handling',
                'use proper trait implementations',
                'follow memory safety guidelines',
                'use proper macro patterns',
                'implement proper async patterns',
                'follow proper module organization',
                'use proper lifetime annotations',
                'implement proper generic constraints',
                'use proper smart pointers',
                'follow proper testing practices',
                'implement proper concurrency patterns',
                'use proper type system features',
                'follow proper documentation',
                'implement proper FFI interfaces',
                'use proper unsafe blocks',
                'follow proper error propagation',
                'implement proper serialization',
                'use proper dependency management'
            ],
            'php': [
                'follow PSR standards',
                'use type declarations',
                'implement proper error handling',
                'use modern PHP features',
                'leverage dependency injection',
                'implement interfaces properly',
                'use namespaces effectively',
                'follow proper autoloading',
                'implement proper testing practices',
                'use proper database abstraction',
                'follow proper security practices',
                'implement proper session handling',
                'use proper caching strategies',
                'follow proper logging practices',
                'implement proper validation',
                'use proper configuration management',
                'follow proper documentation',
                'implement proper middleware',
                'use proper composer management',
                'follow proper deployment practices'
            ],
            'cpp': [
                'follow modern C++ guidelines',
                'use RAII principles',
                'prefer smart pointers over raw pointers',
                'use const correctness',
                'leverage STL containers and algorithms',
                'implement move semantics',
                'use proper memory management',
                'follow proper template usage',
                'implement proper exception handling',
                'use proper operator overloading',
                'follow proper inheritance patterns',
                'implement proper copy/move operations',
                'use proper namespace organization',
                'follow proper compilation practices',
                'implement proper testing strategies',
                'use proper build systems',
                'follow proper optimization practices',
                'implement proper multithreading',
                'use proper type traits',
                'follow proper documentation'
            ],
            'csharp': [
                'follow C# coding conventions',
                'use LINQ when appropriate',
                'implement IDisposable pattern when needed',
                'use async/await for asynchronous operations',
                'prefer properties over public fields',
                'leverage dependency injection',
                'use proper exception handling',
                'follow proper namespace organization',
                'implement proper interface usage',
                'use proper attribute decoration',
                'follow proper event handling',
                'implement proper generic constraints',
                'use proper collection types',
                'follow proper memory management',
                'implement proper serialization',
                'use proper reflection patterns',
                'follow proper documentation',
                'implement proper testing practices',
                'use proper logging patterns',
                'follow proper security guidelines'
            ],
            'ruby': [
                'follow Ruby style guide',
                'use proper block syntax',
                'leverage metaprogramming features',
                'implement proper error handling',
                'use modules for code organization',
                'follow Ruby idioms',
                'use proper gem structure',
                'implement proper testing practices',
                'use proper database access',
                'follow proper documentation',
                'implement proper validation',
                'use proper configuration management',
                'follow proper security practices',
                'implement proper logging',
                'use proper dependency management',
                'follow proper deployment practices',
                'implement proper API design',
                'use proper caching strategies',
                'follow proper performance optimization',
                'implement proper background jobs'
            ],
            'kotlin': [
                'use proper null safety',
                'implement proper coroutines',
                'use proper extension functions',
                'follow Kotlin idioms',
                'implement proper data classes',
                'use proper scope functions',
                'follow proper functional programming patterns',
                'implement proper testing practices',
                'use proper collection operations',
                'follow proper documentation',
                'implement proper serialization',
                'use proper dependency injection',
                'follow proper concurrency patterns',
                'implement proper DSL design',
                'use proper delegation pattern',
                'follow proper multiplatform practices',
                'implement proper type-safe builders',
                'use proper property delegation',
                'follow proper interop with Java',
                'implement proper Android patterns'
            ],
            'swift': [
                'use proper optionals',
                'implement proper protocols',
                'use proper value types',
                'follow Swift idioms',
                'implement proper error handling',
                'use proper memory management',
                'follow proper concurrency patterns',
                'implement proper testing practices',
                'use proper collection types',
                'follow proper documentation',
                'implement proper dependency management',
                'use proper access control',
                'follow proper initialization patterns',
                'implement proper generics usage',
                'use proper property observers',
                'follow proper extension usage',
                'implement proper codable conformance',
                'use proper result builders',
                'follow proper SwiftUI integration',
                'implement proper async/await patterns'
            ],
            'lua': [
                'follow Lua style guide',
                'use proper table management',
                'implement proper metatables',
                'use proper module patterns',
                'leverage coroutines appropriately',
                'implement proper error handling',
                'use proper scope management',
                'follow proper OOP patterns',
                'use proper garbage collection practices',
                'implement proper state management',
                'use proper string manipulation',
                'follow proper debugging practices',
                'use proper package management',
                'implement proper testing patterns',
                'use proper performance optimization',
                'follow proper security practices',
                'implement proper sandboxing',
                'use proper C API integration',
                'follow proper game development patterns',
                'implement proper data serialization'
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
                'accessibility': {
                    'required': True,
                    'standards': ['WCAG 2.1', 'WAI-ARIA 1.2'],
                    'features': [
                        'keyboard navigation',
                        'screen reader support',
                        'color contrast compliance',
                        'focus management',
                        'semantic HTML',
                        'ARIA labels',
                        'responsive design',
                        'font scaling'
                    ]
                },
                'performance': {
                    'metrics': [
                        'First Contentful Paint < 1.8s',
                        'Time to Interactive < 3.8s',
                        'Total Blocking Time < 200ms',
                        'Cumulative Layout Shift < 0.1',
                        'Largest Contentful Paint < 2.5s'
                    ],
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
                        'optimized type checking',
                        'image optimization',
                        'resource preloading',
                        'service worker implementation',
                        'efficient data fetching',
                        'proper CDN usage'
                    ]
                },
                'security': {
                    'required': [
                        'CSRF protection',
                        'XSS prevention',
                        'SQL injection prevention',
                        'secure session handling',
                        'input validation',
                        'proper authentication',
                        'secure password storage',
                        'rate limiting',
                        'secure headers',
                        'CORS configuration',
                        'content security policy',
                        'secure cookie handling',
                        'proper error handling',
                        'secure file uploads',
                        'dependency scanning'
                    ]
                },
                'testing': {
                    'coverage_threshold': 80,
                    'types': [
                        'unit tests',
                        'integration tests',
                        'end-to-end tests',
                        'performance tests',
                        'accessibility tests',
                        'security tests',
                        'visual regression tests',
                        'load tests'
                    ]
                }
            },
            'mobile application': {
                'performance': {
                    'metrics': [
                        'app size < 50MB',
                        'startup time < 2s',
                        'frame rate > 60fps',
                        'memory usage < 200MB'
                    ],
                    'prefer': [
                        'offline first',
                        'battery optimization',
                        'responsive design',
                        'efficient data caching',
                        'lazy image loading',
                        'background task optimization',
                        'proper memory management',
                        'efficient network usage',
                        'proper state persistence',
                        'optimized animations'
                    ]
                },
                'security': {
                    'required': [
                        'secure data storage',
                        'certificate pinning',
                        'biometric authentication',
                        'app signing',
                        'secure network calls',
                        'anti-tampering measures',
                        'secure key storage',
                        'proper permissions handling',
                        'secure deep linking',
                        'proper encryption'
                    ]
                },
                'user_experience': {
                    'required': [
                        'offline support',
                        'proper error states',
                        'loading indicators',
                        'proper navigation patterns',
                        'gesture support',
                        'haptic feedback',
                        'proper keyboard handling',
                        'accessibility support'
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
                        'contribution guidelines',
                        'type definitions',
                        'versioning policy',
                        'migration guides',
                        'performance considerations',
                        'security considerations',
                        'troubleshooting guide'
                    ]
                },
                'testing': {
                    'coverage_threshold': 95,
                    'required': [
                        'unit tests',
                        'integration tests',
                        'performance benchmarks',
                        'backwards compatibility tests',
                        'type checking',
                        'documentation tests',
                        'example tests',
                        'cross-platform tests'
                    ]
                },
                'packaging': {
                    'required': [
                        'proper versioning',
                        'minimal dependencies',
                        'tree-shaking support',
                        'source maps',
                        'type definitions',
                        'proper exports',
                        'proper peer dependencies'
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
                        'consistent interface',
                        'proper exit codes',
                        'proper signal handling',
                        'interactive mode support',
                        'proper terminal handling',
                        'color support'
                    ]
                },
                'performance': {
                    'prefer': [
                        'minimal dependencies',
                        'efficient resource usage',
                        'fast startup time',
                        'proper caching',
                        'efficient file operations',
                        'proper memory management',
                        'efficient process handling'
                    ]
                },
                'security': {
                    'required': [
                        'proper file permissions',
                        'secure credential handling',
                        'input sanitization',
                        'proper environment handling',
                        'secure temp file usage'
                    ]
                }
            },
            'api service': {
                'documentation': {
                    'required': [
                        'API specifications',
                        'endpoint documentation',
                        'authentication guide',
                        'rate limiting details',
                        'error responses',
                        'example requests/responses',
                        'versioning policy',
                        'migration guides'
                    ]
                },
                'security': {
                    'required': [
                        'authentication',
                        'authorization',
                        'input validation',
                        'rate limiting',
                        'logging and monitoring',
                        'proper error handling',
                        'secure headers',
                        'API key management',
                        'request validation',
                        'proper CORS configuration'
                    ]
                },
                'performance': {
                    'metrics': [
                        'response time < 100ms',
                        'throughput > 1000 rps',
                        'error rate < 0.1%'
                    ],
                    'required': [
                        'proper caching',
                        'connection pooling',
                        'query optimization',
                        'proper indexing',
                        'efficient serialization',
                        'proper load balancing'
                    ]
                }
            },
            'data science': {
                'code_organization': {
                    'prefer': [
                        'modular pipeline structure',
                        'reproducible experiments',
                        'version controlled datasets',
                        'documented preprocessing steps',
                        'proper model versioning',
                        'experiment tracking',
                        'proper feature engineering',
                        'proper model evaluation'
                    ]
                },
                'documentation': {
                    'required': [
                        'methodology documentation',
                        'data dictionaries',
                        'model evaluation metrics',
                        'experiment tracking',
                        'feature documentation',
                        'model architecture',
                        'training procedures',
                        'validation methods'
                    ]
                },
                'reproducibility': {
                    'required': [
                        'environment management',
                        'seed setting',
                        'data versioning',
                        'model versioning',
                        'parameter logging',
                        'experiment tracking'
                    ]
                }
            },
            'game': {
                'performance': {
                    'metrics': [
                        'frame rate > 60fps',
                        'load time < 5s',
                        'memory usage < 1GB'
                    ],
                    'prefer': [
                        'efficient resource loading',
                        'frame rate optimization',
                        'memory management',
                        'asset optimization',
                        'proper batching',
                        'efficient rendering',
                        'proper physics optimization',
                        'proper audio management'
                    ]
                },
                'architecture': {
                    'prefer': [
                        'component-based design',
                        'event-driven systems',
                        'efficient state management',
                        'modular systems',
                        'proper scene management',
                        'proper resource management',
                        'efficient input handling',
                        'proper save system'
                    ]
                },
                'user_experience': {
                    'required': [
                        'consistent frame rate',
                        'responsive controls',
                        'proper feedback',
                        'proper saving system',
                        'proper error handling',
                        'accessibility options'
                    ]
                }
            },
            'desktop application': {
                'performance': {
                    'metrics': [
                        'startup time < 3s',
                        'memory usage < 500MB',
                        'response time < 50ms'
                    ],
                    'prefer': [
                        'efficient resource usage',
                        'proper caching',
                        'background processing',
                        'proper memory management',
                        'efficient file operations'
                    ]
                },
                'user_experience': {
                    'required': [
                        'responsive interface',
                        'proper error handling',
                        'proper state persistence',
                        'keyboard shortcuts',
                        'system integration',
                        'proper updates',
                        'accessibility support'
                    ]
                },
                'security': {
                    'required': [
                        'secure file operations',
                        'proper permission handling',
                        'secure data storage',
                        'proper update mechanism',
                        'secure IPC'
                    ]
                }
            },
            'blockchain': {
                'security': {
                    'required': [
                        'secure key management',
                        'proper transaction handling',
                        'secure smart contracts',
                        'proper consensus implementation',
                        'secure networking',
                        'proper cryptography usage'
                    ]
                },
                'performance': {
                    'prefer': [
                        'efficient consensus',
                        'proper transaction batching',
                        'efficient state management',
                        'proper network optimization',
                        'efficient storage'
                    ]
                },
                'reliability': {
                    'required': [
                        'proper error handling',
                        'transaction validation',
                        'state consistency',
                        'proper synchronization',
                        'proper backup mechanisms'
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
        
        # Load patterns from JSON file
        patterns_file = os.path.join(os.path.dirname(__file__), 'templates', 'component_explanations.json')
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
                file_patterns = patterns.get('file_patterns', {})
                directory_patterns = patterns.get('directory_patterns', {})
        except Exception as e:
            print(f"Error loading component explanations: {e}")
            return {}
        
        for component in components:
            clean_name = component.strip().split(' ')[-1]  # Remove emoji and get last part
            
            # Check if it's a directory
            if '\ud83d\udcc1' in component:  # Folder emoji
                explanation = None
                for pattern, desc in directory_patterns.items():
                    if re.search(pattern, clean_name, re.IGNORECASE):
                        explanation = desc
                        break
                if explanation is None:
                    explanation = "Project directory containing related files and resources"
                explanations[clean_name] = explanation
                continue
            
            # Check file patterns
            explanation = None
            for pattern, desc in file_patterns.items():
                if re.search(pattern, clean_name, re.IGNORECASE):
                    explanation = desc
                    break
            if explanation is None:
                explanation = "Project file containing application code or resources"
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