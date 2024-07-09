# <div align="center">Javascript File Cache</div>

These scripts are the core of this application. Python is the framework holding together a handful of Javascript scripts that do the bulk of the heavy lifting.  These scripts are as discreet as possible and separated by category -- c (create), r (read), u (update) and d (delete), in reference to traditional CRUD operations.  This structure may be subject to change as the project changes.  Scripts that fall outside of these definitions such as utilities are kept outside the c/r/u/d folders.  When Banner gets updated, these scripts will likely have to be updated, although their inputs and outputs must remain the same to avoid changing the Python code.  Files:

* **c**
    * **create.js**: script that does a thing 
* **r**
    * **read.js**: script that does a thing
    * **read2.js**: script that does a thing
* **u**
    * **update.js**: script that does a thing
    * **update2.js**: script that does a thing
    * **update3.js**: script that does a thing
* **d**
    * **delete.js**: script that does a thing
    * **delete2.js**: script that does a thing
