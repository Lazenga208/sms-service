FROM python:3.12-slim
# # --- NETFREE CERT INSTALL ---
# COPY ca.crt /usr/local/share/ca-certificates/netfree-root-ca.crt
# RUN update-ca-certificates
# ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
# ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# ENV COMPOSER_CAFILE=/etc/ssl/certs/ca-certificates.crt
# # --- END NETFREE CERT INSTALL ---

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
