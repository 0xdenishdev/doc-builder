# Simle doc-builder
Simple module that builds the documentation from file that contains doc blocks which is surrounded with symbols /* */ and contains descriptor tags (Ex. @author)

---
## Usage
To build the documentation from file simply do these steps:
###### 1. add doc area surrounded with symbols """ and """
###### 2. add tag descriptor starting from '@' (Ex. @author)
###### 3. run next commands:
```python
>>> import builder
>>> builder.run( 'your_file.extension' )
```
