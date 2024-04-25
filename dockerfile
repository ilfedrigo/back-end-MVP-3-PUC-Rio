
FROM python:3.9


ENV FLASK_APP=main.py

# Copie os arquivos do back-end para o diretório de trabalho no container
COPY back-end-MVP-3-PUC-Rio/ /app

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta do Flask (se necessário)
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0"]