# run_tests.ps1 - Joining Hands Automated Test Infrastructure Task Runner
# Usage:
#   .\run_tests.ps1         - Runs all 46 test cases
#   .\run_tests.ps1 google  - Runs only the Google OAuth OIDC suite
#   .\run_tests.ps1 jwt     - Runs only the JWT cryptographic session suite

param (
    [string]$suite = "all"
)

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "   JOINING HANDS - AUTOMATED TEST RUNNER CLI   " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if ($suite -eq "google") {
    Write-Host "Launching Google OAuth Test Suite..." -ForegroundColor Yellow
    python -m unittest tests/test_real_google_oauth.py
}
elseif ($suite -eq "jwt") {
    Write-Host "Launching JWT & Backend Solid Suite..." -ForegroundColor Yellow
    python -m unittest tests/test_jwt_and_backend_solid.py
}
elseif ($suite -eq "profile") {
    Write-Host "Launching Profile Photo Lifecycle Suite..." -ForegroundColor Yellow
    python -m unittest tests/test_profile_photo_lifecycle.py
}
elseif ($suite -eq "hashtag") {
    Write-Host "Launching Hashtag and Product Upgrade Suite..." -ForegroundColor Yellow
    python -m unittest tests/test_hashtag_and_product_upgrade.py
}
elseif ($suite -eq "master") {
    Write-Host "Launching Master Presentation Suite..." -ForegroundColor Yellow
    python -m unittest tests/master_presentation_test.py
}
else {
    Write-Host "Running FULL 46 test case regression matrix..." -ForegroundColor Yellow
    python -m unittest discover -s tests -p "*.py"
}

Write-Host "==================================================`n" -ForegroundColor Cyan
