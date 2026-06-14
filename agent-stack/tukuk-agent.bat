@echo off
setlocal
set ROOT=%~dp0
cd /d "%ROOT%"
set MODEL=%TUKUK_AGENT_MODEL%
if "%MODEL%"=="" set MODEL=llama3.2
if "%1"=="" set CMD=kilo
if "%1"=="agent" (
  if "%2"=="" (
    py cli.py agent "Build a student web app" --model %MODEL%
  ) else (
    py cli.py agent %2 --model %MODEL%
  )
) else if "%1"=="terminal" (
  py cli.py terminal
) else if "%1"=="console" (
  py cli.py terminal
) else if "%1"=="mcp" (
  py cli.py mcp
) else if "%1"=="pipeline" (
  py cli.py pipeline
) else if "%1"=="diagnostic" (
  py cli.py diagnostic --url %2
) else if "%1"=="security" (
  py cli.py diagnostic --url %2
) else if "%1"=="web" (
  py cli.py web --open
) else if "%1"=="website" (
  py cli.py web --open
) else if "%1"=="docker" (
  docker compose up --build
) else (
  py cli.py %*
)
endlocal
