@echo off

rd /s/q build_htmlhelp
rd /s/q build_web
rd /s/q build_latex

rem c:\python26\scripts\sphinx-build -E -a -b htmlhelp .\source .\build_htmlhelp
c:\python26\scripts\sphinx-build -E -a -b html .\source .\build_web
rem c:\python26\scripts\sphinx-build -E -a -b latex .\source .\build_latex