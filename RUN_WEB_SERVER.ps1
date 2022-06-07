Write-Host "Please make sure to activate the virtual environment in Scripts or else this will error in 5 seconds."
Start-Sleep -Seconds 5
py manage.py runserver 0.0.0.0:8000
