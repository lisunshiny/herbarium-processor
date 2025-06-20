Notebook help

Use the poetry virtualenv to run the notebooks so that they have access to the herbarium processor package.

If that doesn't work, add this code to the top of the notebook and it will work too.

```
from utils.notebook_setup import setup_project
setup_project()
```