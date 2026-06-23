# PayShield Disputes

## English

### Overview

PayShield Disputes is a chargeback and dispute management service within the PayShield Platform. It provides endpoints to search transactions by ID, view the chargeback history of a transaction, calculate a fraud risk score, and record evidence for disputes. The goal is to simulate the workflows around chargebacks and disputes in a payment ecosystem.

### Architecture

```text
Client -> GET /disputes/{id}             -> DisputeService      -> Transaction details
Client -> GET /disputes/{id}/history     -> HistoryService      -> Chargeback history
Client -> POST /disputes/{id}/score      -> RiskScoreEngine     -> Risk score
Client -> POST /disputes/{id}/evidence    -> EvidenceStore       -> Acknowledgment
```

The service orchestrates different components: a search module to query transactions, a chargeback history module, a simple risk scoring engine, and an evidence repository.

### OpenAPI / Swagger Docs

After running the API (e.g. `uvicorn main:app --reload`), visit `/docs` to view the interactive Swagger UI generated from the FastAPI application. The API includes:

- **GET /disputes/{transaction_id}** – Returns information about a given transaction and any associated disputes.
- **GET /disputes/{transaction_id}/history** – Returns the chargeback history for a transaction.
- **POST /disputes/{transaction_id}/score** – Calculates and returns a fraud risk score based on basic heuristics (amount, country, velocity).
- **POST /disputes/{transaction_id}/evidence** – Accepts evidence documents or notes for a dispute and records them.

### Use Cases

- Investigate suspicious transactions and view prior chargebacks.
- Assess the risk of a new dispute by generating a score.
- Collect and store evidence (notes, documents) for a potential chargeback.
- Learn the typical workflow of dispute management without using real payment data.

### Roadmap

- Implement more sophisticated risk scoring leveraging past dispute data.
- Add support for uploading and storing files as evidence (e.g. receipts, screenshots).
- Integrate with an email or notification system for dispute status updates.
- Expand the data model to include merchants, issuers, and acquirers.

### Screenshots

Add screenshots of the Swagger UI and example dispute search/score responses to illustrate how the service works.

### Disclaimer

This is an educational project. It uses simulated data only and does not handle real cardholder information or connect to any payment processors. It is not intended for production use.

---

## Português

### Visão Geral

PayShield Disputes é um serviço de gerenciamento de chargebacks e disputas dentro da plataforma PayShield. Ele oferece endpoints para pesquisar transações pelo identificador, visualizar o histórico de chargebacks de uma transação, calcular uma pontuação de risco de fraude e registrar evidências para disputas. O objetivo é simular os fluxos de trabalho de chargebacks e disputas em um ecossistema de pagamentos.

### Arquitetura

```text
Cliente -> GET /disputes/{id}             -> Serviço de Disputas        -> Detalhes da transação
Cliente -> GET /disputes/{id}/history     -> Serviço de Histórico       -> Histórico de chargebacks
Cliente -> POST /disputes/{id}/score      -> Motor de Risco             -> Pontuação de risco
Cliente -> POST /disputes/{id}/evidence    -> Repositório de Evidências   -> Confirmação
```

O serviço orquestra diferentes componentes: um módulo de busca de transações, um módulo de histórico de chargebacks, um modelo simples de pontuação de risco e um repositório de evidências.

### Documentação (Swagger / OpenAPI)

Após executar a API (por exemplo, `uvicorn main:app --reload`), acesse `/docs` para interagir com a documentação gerada automaticamente. A API inclui:

- **GET /disputes/{transaction_id}** – Retorna informações sobre uma transação e quaisquer disputas associadas.
- **GET /disputes/{transaction_id}/history** – Retorna o histórico de chargebacks de uma transação.
- **POST /disputes/{transaction_id}/score** – Calcula e retorna uma pontuação de risco de fraude com base em heurísticas básicas (ex.: valor, país, velocidade).
- **POST /disputes/{transaction_id}/evidence** – Aceita documentos ou notas de evidência para uma disputa e os registra.

### Casos de Uso

- Investigar transações suspeitas e ver chargebacks anteriores.
- Avaliar o risco de uma nova disputa gerando uma pontuação.
- Coletar e armazenar evidências (notas, documentos) para um potencial chargeback.
- Aprender o fluxo típico de gerenciamento de disputas sem usar dados de pagamento reais.

### Roadmap

- Implementar pontuação de risco mais sofisticada usando dados de disputas anteriores.
- Adicionar suporte para upload e armazenamento de arquivos como evidência (ex.: recibos, capturas de tela).
- Integrar com um sistema de e-mail ou notificações para atualizações de status de disputa.
- Expandir o modelo de dados para incluir comerciantes, emissores e adquirentes.

### Capturas de Tela

Adicione capturas de tela da interface Swagger e de respostas de busca/pontuação de disputas para ilustrar como o serviço funciona.

### Disclaimer

Este é um projeto educacional. Ele usa apenas dados simulados e não lida com informações reais de portadores de cartão nem se conecta a processadores de pagamento. Não se destina ao uso em produção.
