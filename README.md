
# Cloth Creator for Maya
This is a Python plugin that allows the user to create cloth in Maya utilizing Maya's nCloth system. Make tablecloth, curtains, and ribbon bows. <br>

## Curtains


<details>

<summary> <h3> Parameters for Curtains </h3>

</summary>

### Curtain Type
Choose to create a single panel, panel pair, or a complete curtain set.

### Tie back
Able to have the curtain tied back. (Works best with width of 5 and height of 10.)

</details>

## Materials
Choose a material to make it: <br>
 - Cotton
 - Velvet
 - Satin
 - Plaid
 - Iridescent <br>

![materials](https://github.com/raefu22/clothCreator/assets/94275037/5fd44c41-9c10-4276-9c55-d048a4d50543)
 
**Materials showcase with settings of elliptic tablecloth*

### Plaid



![plaid](https://github.com/raefu22/clothCreator/assets/94275037/1494f0e4-a93f-4be7-bc9a-9e1d20d019b4)

**Sample plaid materials on rectangular tablecloth*

## FAQ

### Folds in cloth with curve not working?

Enable the following in the Plug-in Manager:<br>
 - sweep.mll

### Bow misaligned?

Delete prefs folder and then open Maya 2022.5. The prefs folder is typically found in: <br>
 - Windows: <drive>:\Documents\maya\<version>\ <br>
 - Mac OS X: /Users/<username>/Library/Preferences/Autodesk/maya/<version>/ <br>
 - Linux: /home/<username>/maya/<version>/

<br>

*Developed in Maya 2022.5*
