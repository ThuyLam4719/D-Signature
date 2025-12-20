# about-the-project

This project uses PySide6 to create a desktop app simulating the process of key generration by RSA/ECDSA algorithms, creating/verifying digital signature, generating Certificate Signing Request (CSR) and validating digital certificate. Additonally, there is a web app (using Flask) simulating CA Server to issue digital certificates and manage them.

## run desktop app 

*! before running app, make sure that you are in the root directory.*

- python -m .modules.ui.mainApp

## run web app

- python -m .modules.web\_ca.app

