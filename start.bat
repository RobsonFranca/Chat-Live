@echo off
echo [INFO] Iniciando o script...

:: Verifica se o Git está instalado e faz o pull
where git >nul 2>nul
if errorlevel 1 (
    echo [AVISO] Git nao encontrado no sistema. Pulando atualizacao do codigo.
) else (
    :: Verifica se a pasta atual é um repositório Git
    if exist .git (
        echo [INFO] Atualizando o codigo com Git Pull...
        git pull
    ) else (
        echo [AVISO] Esta pasta nao e um repositorio Git. Pulando pull.
    )
)

:: Verifica se a pasta venv existe
if not exist venv (
    echo [INFO] Pasta venv nao encontrada. Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 goto erro
) else (
    echo [INFO] Ambiente virtual venv ja existe. Pulando criacao.
)

:: Ativando o venv
echo [INFO] Ativando ambiente virtual...
call .\venv\Scripts\activate

:: Instalando  
echo [INFO] Instalando dependencias do requirements.txt...
.\venv\Scripts\pip install -r requirements.txt
if errorlevel 1 goto erro

:: Roda o script principal do Python
echo [INFO] Rodando o main.py...
start "" ".\venv\Scripts\pythonw.exe" main.py
if errorlevel 1 goto erro

echo [INFO] Processo finalizado com sucesso!
exit

:erro
echo [ERRO] Ocorreu uma falha no processo. Verifique as mensagens acima.
pause