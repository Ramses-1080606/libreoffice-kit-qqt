# LibreOffice for Windows Toolkit Documentation

## Quick Start

```python
from libreoffice_toolkit import LibreofficeForClient

client = LibreofficeForClient()
if client.is_installed():
    client.connect()
    print(f"Version: {client.get_version()}")
```

## API Reference

See individual module documentation.
