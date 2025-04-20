DEPLOY_DIR := deploy
CERTS_DIR := $(DEPLOY_DIR)/certs
CERT_PATH := $(CERTS_DIR)/cert.pem
CERT_KEY_PATH := $(CERTS_DIR)/key.pem
CERT_AND_KEY_EXISTENCE_CHECK = $(and $(wildcard $(CERT_PATH)),$(wildcard $(CERT_KEY_PATH)))
CERT_OR_KEY_EXISTENCE_CHECK = $(or $(wildcard $(CERT_PATH)),$(wildcard $(CERT_KEY_PATH)))
KEYS_DIR := keys
KEYS_EXISTENCE_CHECK = $(wildcard $(KEYS_DIR))


all: prod


prod: setup-env prod-certs gen-keys run

dev: setup-env dev-certs gen-keys run


$(DEPLOY_DIR)/.env:
	cp $(DEPLOY_DIR)/.env.example $(DEPLOY_DIR)/.env
	nano $(DEPLOY_DIR)/.env

setup-env: $(DEPLOY_DIR)/.env


$(CERTS_DIR):
	mkdir -p $(CERTS_DIR)

prod-certs: $(CERTS_DIR)
ifeq "$(CERT_AND_KEY_EXISTENCE_CHECK)" ""
	$(error '$(CERT_PATH)' and '$(CERT_KEY_PATH)' should be present)
else
	@echo "Certificates are present"
endif

dev-certs: $(CERTS_DIR)
ifeq "$(CERT_OR_KEY_EXISTENCE_CHECK)" ""
	openssl req -x509 -newkey rsa:4096 -sha256 -noenc -out $(CERT_PATH) -keyout $(CERT_KEY_PATH) -days 365 -batch 2> /dev/null
else
	@echo "Not overwriting existing certificates"
endif


$(KEYS_DIR):
	mkdir -p $(KEYS_DIR)

gen-keys: $(KEYS_DIR)
ifeq "$(KEYS_EXISTENCE_CHECK)" ""
	cd $(KEYS_DIR) && ssh-keygen -t rsa -f id_rsa -N "" > /dev/null
endif


run:
	cd $(DEPLOY_DIR) && docker compose up -d

stop:
	cd $(DEPLOY_DIR) && docker compose down

clean:
	cd $(DEPLOY_DIR) && docker compose down -v

restart: stop run
