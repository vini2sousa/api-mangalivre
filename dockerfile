FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation libnss3 libxss1 libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 xdg-utils libdbus-glib-1-2 libxtst6 libxrandr2 libxcomposite1 \
    libxcursor1 libxi6 libpango1.0-0 libpangocairo-1.0-0 libatspi2.0-0 libdrm2 libgbm1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome (última versão estável)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb || apt-get -f install -y && \
    rm google-chrome-stable_current_amd64.deb

WORKDIR /app

COPY requirements.txt .
# Inclui o webdriver-manager nas dependências
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "scrap.py"]
