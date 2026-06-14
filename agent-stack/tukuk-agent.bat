@echo off
setlocal
set ROOT=%~dp0
cd /d "%ROOT%"
set MODEL=%TUKUK_AGENT_MODEL%
if "%MODEL%"=="" set MODEL=llama3.2
if "%1"=="agent" (
  if "%2"=="" (
    py cli.py agent "Help me learn and build a student web app" --model %MODEL%
  ) else (
    py cli.py agent %2 --model %MODEL%
  )
) else if "%1"=="diagnostic" (
  py cli.py diagnostic --url %2
) else if "%1"=="docker" (
  docker compose up --build
) else (
  py cli.py %*
)
endlocal
