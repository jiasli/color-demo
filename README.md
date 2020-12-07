# Color Demo

A demo showing how to use ANSI control sequence with [Virtual Terminal](https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences).


## Run

Simply use python to run it. [colorama](https://github.com/tartley/colorama) is not required.

```sh
# We need numpy to provide a count-down range
pip install numpy==1.19.3
python color_demo.py
```


## Result

### Windows Terminal running PowerShell Core
![](img/windows-terminal.png)

### VS Code Terminal running PowerShell Core
![](img/vscode.png)

### Default PowerShell Core terminal
![](img/pwsh-core.png)

### Default Windows PowerShell terminal
![](img/windows-powershell.png)

### Default Windows Command Prompt
![](img/windows-cmd.png)


## References

- https://stackoverflow.com/questions/16755142/how-to-make-win32-console-recognize-ansi-vt100-escape-sequences
- https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences?redirectedfrom=MSDN
- https://bugs.python.org/issue30075

ℹ NumPy 1.19.4 doesn't work on Windows. See

- https://stackoverflow.com/questions/64654805/how-do-you-fix-runtimeerror-package-fails-to-pass-a-sanity-check-for-numpy-an
- https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html
