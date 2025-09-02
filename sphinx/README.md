# RAG Search Flow Documentation

This directory contains the comprehensive documentation for the RAG Search Flow project, built using Sphinx.

## Overview

The documentation covers:

- **Getting Started**: Installation and quick start guides
- **Core Components**: Search flow architecture, crews, and tools
- **Configuration**: How to customize agents, tasks, and system behavior
- **API Reference**: Detailed API documentation for all modules
- **Examples**: Practical usage examples and use cases
- **Development**: Guide for extending and contributing to the system
- **Contributing**: Guidelines for contributors

## Building the Documentation

### Prerequisites

- Python 3.10+
- Sphinx and sphinx-rtd-theme

### Quick Build

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the documentation**:
   ```bash
   # On Windows
   .\make.bat html
   
   # On Unix-like systems
   make html
   
   # Or use the Python script
   python build_docs.py
   ```

3. **View the documentation**:
   Open `_build/html/index.html` in your web browser.

### Build Options

- **HTML**: `make html` - Build HTML documentation
- **PDF**: `make latexpdf` - Build PDF documentation (requires LaTeX)
- **Clean**: `make clean` - Remove build artifacts
- **Help**: `make help` - Show all available build targets

## Documentation Structure

```
sphinx/
├── index.rst              # Main documentation index
├── installation.rst        # Installation guide
├── quickstart.rst          # Quick start tutorial
├── search_flow.rst         # Search flow architecture
├── crews.rst              # Crews system documentation
├── tools.rst              # Tools system documentation
├── configuration.rst       # Configuration guide
├── api/                   # API reference
│   └── modules.rst        # Module documentation
├── examples.rst            # Usage examples
├── development.rst         # Development guide
├── contributing.rst        # Contributing guidelines
├── conf.py                # Sphinx configuration
├── requirements.txt        # Documentation dependencies
├── build_docs.py          # Build script
├── Makefile               # Make targets (Unix)
└── make.bat               # Make targets (Windows)
```

## Customization

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory
2. Add it to the relevant `toctree` in `index.rst`
3. Rebuild the documentation

### Modifying the Theme

The documentation uses the `sphinx-rtd-theme`. You can customize it by modifying the `html_theme_options` in `conf.py`.

### Adding Extensions

Sphinx extensions can be added to the `extensions` list in `conf.py`. Some useful extensions include:

- `sphinx.ext.autodoc` - Auto-generate documentation from docstrings
- `sphinx.ext.napoleon` - Support for Google and NumPy docstring formats
- `sphinx.ext.viewcode` - Link to source code
- `sphinx.ext.intersphinx` - Link to other documentation

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure the source code is in the Python path
2. **Build failures**: Check that all dependencies are installed
3. **Missing modules**: Verify that the module paths in `conf.py` are correct

### Getting Help

- Check the Sphinx documentation: https://www.sphinx-doc.org/
- Review the build output for specific error messages
- Ensure all required packages are installed

## Contributing to Documentation

When contributing to the documentation:

1. Follow the existing style and structure
2. Use clear, concise language
3. Include practical examples
4. Update the table of contents when adding new pages
5. Test that the documentation builds successfully

## Deployment

The built documentation can be deployed to:

- **GitHub Pages**: Push the `_build/html` directory to a `gh-pages` branch
- **Read the Docs**: Connect your repository to Read the Docs for automatic builds
- **Web Server**: Copy the `_build/html` directory to your web server

## License

This documentation is part of the RAG Search Flow project and follows the same license terms.
