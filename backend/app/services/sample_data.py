SAMPLE_DOCUMENTS = [
    {
        "id": "doc-invoice-001",
        "filename": "INV-2026-8842-Nvidia-Compute.pdf",
        "file_type": "pdf",
        "file_size": 48200,
        "classification": "invoice",
        "classification_confidence": 0.98,
        "classification_reason": "Contains invoice header, line items, monetary totals, customer addresses, and Net 30 payment covenants.",
        "classification_metadata": {
            "vendor": "Apex Cloud Systems Inc.",
            "currency": "USD",
            "invoice_no": "INV-2026-8842"
        },
        "raw_text": """APEX CLOUD SYSTEMS INC.
400 Mission Street, Suite 2400
San Francisco, CA 94105
Tax ID: US-84-2910394

INVOICE
Invoice Number: INV-2026-8842
Invoice Date: October 12, 2026
Payment Due Date: November 12, 2026
Payment Terms: Net 30 Days via ACH or Fedwire
Currency: USD

BILL TO:
Global Logistics Corp
Attn: Accounts Payable & AI Infrastructure
1200 Broadway, 14th Floor
New York, NY 10001
Account ID: GLC-99214

DESCRIPTION OF SERVICES:
1. Dedicated GPU Compute Cluster (NVIDIA H100 SXM5 x 4 Nodes)
   Billing Period: Sept 15, 2026 - Oct 14, 2026
   Quantity: 1.0 Month
   Unit Price: $4,800.00
   Line Total: $4,800.00

2. Enterprise OpenRouter Gateway Egress & High-Bandwidth Routing
   Billing Period: 1,250,000 API Transactions
   Quantity: 1,250,000.0
   Unit Price: $0.0008
   Line Total: $1,000.00

3. Tier-1 High-Availability 24/7 Enterprise Engineering Support
   Quantity: 1.0 Month
   Unit Price: $1,200.00
   Line Total: $1,200.00

FINANCIAL SUMMARY:
Subtotal: $7,000.00
State Sales Tax (8.5%): $595.00
Total Amount Due: $7,595.00

Remittance Advice:
Bank Name: Silicon Reserve Bank
Routing Number: 121000358
Account Number: 84930219481
For billing inquiries, contact: billing@apexcloud.io""",
        "extracted_data": {
            "invoice_number": "INV-2026-8842",
            "date": "2026-10-12",
            "due_date": "2026-11-12",
            "vendor_name": "Apex Cloud Systems Inc.",
            "vendor_address": "400 Mission Street, Suite 2400, San Francisco, CA 94105",
            "customer_name": "Global Logistics Corp",
            "customer_address": "1200 Broadway, 14th Floor, New York, NY 10001",
            "line_items": [
                {"description": "Dedicated GPU Compute Cluster (NVIDIA H100 SXM5 x 4 Nodes)", "quantity": 1.0, "unit_price": 4800.0, "total": 4800.0},
                {"description": "Enterprise OpenRouter Gateway Egress & Routing", "quantity": 1250000.0, "unit_price": 0.0008, "total": 1000.0},
                {"description": "Tier-1 High-Availability 24/7 Enterprise Support", "quantity": 1.0, "unit_price": 1200.0, "total": 1200.0}
            ],
            "subtotal": 7000.0,
            "tax": 595.0,
            "total_amount": 7595.0,
            "currency": "USD",
            "payment_terms": "Net 30 Days via ACH or Fedwire"
        },
        "summary": {
            "executive": "Monthly enterprise cloud infrastructure billing from Apex Cloud Systems for dedicated H100 GPU compute, OpenRouter routing egress, and 24/7 support totaling $7,595.00.",
            "bullets": [
                "NVIDIA H100 GPU compute monthly allocation: $4,800.00.",
                "1.25M OpenRouter gateway transactions billed at $1,000.00.",
                "Net 30 payment due by November 12, 2026."
            ],
            "tldr": "NVIDIA H100 & OpenRouter compute invoice for $7,595.00 due Nov 12, 2026.",
            "action_items": ["Submit ACH transfer of $7,595.00 to Silicon Reserve Bank prior to Nov 12, 2026."]
        }
    },
    {
        "id": "doc-contract-v1",
        "filename": "MSA-2025-Standard-v1.docx",
        "file_type": "docx",
        "file_size": 32400,
        "classification": "contract",
        "classification_confidence": 0.99,
        "classification_reason": "Master Services Agreement containing standard terms, covenants, SLA thresholds, and liability limitations.",
        "classification_metadata": {
            "jurisdiction": "State of California",
            "parties": ["Apex Cloud Systems Inc.", "Global Logistics Corp"],
            "version": "1.0"
        },
        "raw_text": """MASTER SERVICES AGREEMENT (VERSION 1.0 - 2025)

This Master Services Agreement ("Agreement") is entered into as of January 15, 2025, by and between Apex Cloud Systems Inc. ("Provider"), and Global Logistics Corp ("Customer").

1. SCOPE OF SERVICES
Provider agrees to deliver managed cloud infrastructure, AI model hosting, and document ingestion services as specified in applicable Statements of Work.

2. SERVICE LEVEL AGREEMENT (SLA)
Provider will use commercially reasonable efforts to make the AI endpoints available with an uptime percentage of at least 99.0% during any monthly billing cycle. In the event of unscheduled downtime exceeding 1.0%, Customer's sole remedy shall be a 5% credit on the monthly service fee.

3. FEES AND PAYMENT
Customer shall pay all undisputed fees within thirty (30) days from the date of each invoice ("Net 30"). Overdue payments shall accrue interest at 1.0% per month.

4. DATA OWNERSHIP AND PRIVACY
Customer retains all right, title, and interest in and to Customer Data. Provider may utilize anonymized, aggregated query metrics solely to tune backend load balancing and system optimization.

5. LIMITATION OF LIABILITY
TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT EXCEED THE TOTAL AMOUNT ACTUALLY PAID BY CUSTOMER UNDER THIS AGREEMENT IN THE SIX (6) MONTHS PRECEDING THE EVENT GIVING RISE TO LIABILITY ($45,000 USD).

6. TERM AND TERMINATION
This Agreement shall commence on the Effective Date and continue for an initial period of one (1) year. Either party may terminate for convenience upon ninety (90) days prior written notice.

7. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to conflict of laws principles.""",
        "extracted_data": {
            "title": "Master Services Agreement (Version 1.0 - 2025)",
            "parties": ["Apex Cloud Systems Inc. (Provider)", "Global Logistics Corp (Customer)"],
            "effective_date": "2025-01-15",
            "expiration_date": "2026-01-14",
            "governing_law": "State of California",
            "key_obligations": [
                "Deliver managed cloud infrastructure and document ingestion.",
                "Maintain 99.0% monthly uptime with 5% credit remedy on breach.",
                "Customer must settle invoices within Net 30 days."
            ],
            "payment_terms": "Net 30 Days, 1.0% late interest",
            "termination_clause": "90 days written notice for convenience",
            "liability_cap": "Fees paid in prior 6 months ($45,000 USD)",
            "confidentiality_period": "Standard business confidentiality",
            "auto_renewal": False
        },
        "summary": {
            "executive": "Standard MSA 2025 agreement establishing 99.0% service availability, Net 30 payment schedule, California governing law, and a 6-month liability cap ($45,000).",
            "bullets": [
                "99.0% availability SLA target with 5% service credit remedy.",
                "Liability strictly capped at 6 months of historical fees.",
                "90-day notification period required for termination for convenience."
            ],
            "tldr": "Baseline 2025 MSA with 99.0% SLA and 6-month liability cap under California law.",
            "action_items": ["Monitor renewal milestones 90 days before January 15 expiration."]
        }
    },
    {
        "id": "doc-contract-v2",
        "filename": "MSA-2026-Amended-v2.docx",
        "file_type": "docx",
        "file_size": 34100,
        "classification": "contract",
        "classification_confidence": 0.99,
        "classification_reason": "Updated 2026 Master Services Agreement with enhanced enterprise SLA, stricter zero-training privacy covenants, and doubled liability cap.",
        "classification_metadata": {
            "jurisdiction": "State of Delaware",
            "parties": ["Apex Cloud Systems Inc.", "Global Logistics Corp"],
            "version": "2.0 (Amended)"
        },
        "raw_text": """MASTER SERVICES AGREEMENT (VERSION 2.0 - AMENDED 2026)

This Amended Master Services Agreement ("Agreement") is entered into as of October 15, 2026, by and between Apex Cloud Systems Inc. ("Provider"), and Global Logistics Corp ("Customer").

1. SCOPE OF SERVICES
Provider agrees to deliver managed cloud infrastructure, OpenRouter AI multi-model gateway inference, and pgvector semantic document ingestion pipelines.

2. SERVICE LEVEL AGREEMENT (SLA)
Provider formally guarantees that the AI gateway and inference endpoints shall maintain an uptime percentage of at least 99.95% during each monthly billing cycle. In the event of unscheduled downtime exceeding 0.05%, Customer shall receive a 10% credit for each 0.1% breach, capped at 100% of the monthly invoice.

3. FEES AND PAYMENT
Customer shall pay all undisputed fees within thirty (30) days from invoice receipt ("Net 30"). Overdue payments shall accrue interest at 1.5% per month.

4. DATA OWNERSHIP AND ZERO-RETENTION PRIVACY
Customer retains sole and exclusive ownership of all Customer Data, uploaded files, and vector embeddings. Provider guarantees ZERO data retention for foundation model training. No customer inputs or inference completions shall ever be transmitted or used for retraining third-party models.

5. LIMITATION OF LIABILITY
TO THE MAXIMUM EXTENT PERMITTED BY LAW, EACH PARTY'S TOTAL AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT SHALL BE STRICTLY CAPPED AT THE TOTAL AMOUNT PAID BY CUSTOMER UNDER THIS AGREEMENT IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM ($91,140 USD).

6. TERM AND TERMINATION
This Agreement shall commence on October 15, 2026, and continue for one (1) year, automatically renewing for successive one-year terms unless either party provides thirty (30) days written notice of non-renewal. Either party may terminate for convenience on sixty (60) days written notice.

7. GOVERNING LAW AND DISPUTE RESOLUTION
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, with mandatory arbitration seated in Wilmington, DE.""",
        "extracted_data": {
            "title": "Master Services Agreement (Version 2.0 - Amended 2026)",
            "parties": ["Apex Cloud Systems Inc. (Provider)", "Global Logistics Corp (Customer)"],
            "effective_date": "2026-10-15",
            "expiration_date": "2027-10-14",
            "governing_law": "State of Delaware (Arbitration Wilmington, DE)",
            "key_obligations": [
                "Guarantee 99.95% uptime with 10% credit per 0.1% downtime breach.",
                "Zero data retention: Customer data never used for model training.",
                "Auto-renewal for successive 1-year terms with 30-day non-renewal notice."
            ],
            "payment_terms": "Net 30 Days, 1.5% late interest",
            "termination_clause": "60 days written notice for convenience",
            "liability_cap": "Fees paid in prior 12 months ($91,140 USD)",
            "confidentiality_period": "Strict zero-retention privacy covenant",
            "auto_renewal": True
        },
        "summary": {
            "executive": "Amended 2026 MSA upgrading SLA uptime to 99.95%, instituting strict Zero-Data-Retention for AI models, expanding liability cap to 12 months ($91,140), and transitioning jurisdiction to Delaware.",
            "bullets": [
                "Uptime SLA raised to 99.95% with escalating credit penalties.",
                "Guaranteed zero retention and zero AI model training on customer documents.",
                "Liability cap doubled to 12 months ($91,140).",
                "Governing law updated to Delaware with arbitration clause."
            ],
            "tldr": "Upgraded 2026 MSA with 99.95% SLA, zero-training privacy clause, and 12-month liability ceiling.",
            "action_items": ["Confirm Delaware arbitration venue with legal counsel."]
        }
    },
    {
        "id": "doc-resume-001",
        "filename": "Sarah_Chen_Staff_AI_Engineer_Resume.pdf",
        "file_type": "pdf",
        "file_size": 28900,
        "classification": "resume",
        "classification_confidence": 0.99,
        "classification_reason": "Professional CV detailing engineering work experience, skills taxonomy, and academic credentials.",
        "classification_metadata": {
            "candidate_name": "Sarah Chen",
            "experience_years": "7+",
            "target_role": "Staff AI Platform Engineer"
        },
        "raw_text": """SARAH CHEN
San Francisco, CA | sarah.chen.ai@example.com | (415) 890-3421 | linkedin.com/in/sarahchen-ai

PROFESSIONAL SUMMARY
Senior / Staff AI Platform Engineer with 7+ years of experience architecting distributed LLM inference gateways, high-throughput RAG vector indexing pipelines, and enterprise document intelligence microservices. Deep expertise in OpenRouter API integration, PyTorch, pgvector, and FastAPI.

TECHNICAL SKILLS
- AI & LLM Systems: OpenRouter API, vLLM, FastEmbed, LangChain, Llama 3.3, Gemini 2.0 Flash, DeepSeek-V3, Prompt Engineering
- Vector Databases: pgvector (PostgreSQL), Qdrant, Pinecone, FAISS, Cosine Similarity HNSW
- Backend & Cloud: Python (FastAPI, asyncio), Go, Docker, Kubernetes, AWS, Render, Supabase, Redis
- Frontend & UI: React 19, TypeScript, Tailwind CSS, Vite, Impeccable Design System

WORK EXPERIENCE
Staff AI Platform Engineer | Cognitive Scale Labs | San Francisco, CA | 2024 - Present
- Designed and scaled multi-tenant OpenRouter AI Gateway handling 12M daily requests across heterogeneous models (Llama 3.3, Gemini Flash, Mistral).
- Built semantic RAG pipeline utilizing pgvector and FastEmbed embeddings, achieving sub-65ms P99 retrieval latency over 500,000 PDF documents.
- Implemented intelligent model routing heuristics, cutting API token expenditure by 44% while preserving 99.1% response fidelity.

Senior Backend & ML Engineer | Veritas Data Systems | Palo Alto, CA | 2021 - 2024
- Developed automated document parser for invoices, financial statements, and contracts, processing 25,000 pages per hour with PyPDF and OCR.
- Spearheaded PostgreSQL pgvector migration, eliminating dedicated vector DB licensing costs ($180k/yr saved).

EDUCATION
University of California, Berkeley
Bachelor of Science in Electrical Engineering & Computer Sciences (EECS) | Graduated Magna Cum Laude

CERTIFICATIONS
- AWS Certified Machine Learning - Specialty
- Certified Kubernetes Administrator (CKA)""",
        "extracted_data": {
            "name": "Sarah Chen",
            "email": "sarah.chen.ai@example.com",
            "phone": "(415) 890-3421",
            "location": "San Francisco, CA",
            "summary": "Senior / Staff AI Platform Engineer with 7+ years of experience architecting distributed LLM inference gateways and RAG vector systems.",
            "skills": {
                "ai_llm": ["OpenRouter API", "vLLM", "FastEmbed", "Llama 3.3", "Gemini 2.0 Flash", "DeepSeek", "Prompt Engineering"],
                "vector_db": ["pgvector (PostgreSQL)", "Qdrant", "HNSW Cosine Similarity"],
                "backend": ["Python (FastAPI)", "Go", "Docker", "Kubernetes", "AWS", "Supabase", "Redis"],
                "frontend": ["React", "TypeScript", "Tailwind CSS", "Vite"]
            },
            "experience": [
                {
                    "company": "Cognitive Scale Labs",
                    "role": "Staff AI Platform Engineer",
                    "duration": "2024 - Present",
                    "highlights": [
                        "Designed multi-tenant OpenRouter AI gateway routing 12M requests daily.",
                        "Built sub-65ms P99 RAG pipeline with pgvector over 500k documents.",
                        "Cut API inference costs by 44% with dynamic model routing."
                    ]
                },
                {
                    "company": "Veritas Data Systems",
                    "role": "Senior Backend & ML Engineer",
                    "duration": "2021 - 2024",
                    "highlights": [
                        "Developed automated document parser processing 25,000 pages per hour.",
                        "Migrated vector storage to pgvector, saving $180k/yr in infrastructure."
                    ]
                }
            ],
            "education": [
                {"institution": "UC Berkeley", "degree": "B.S. Electrical Engineering & Computer Sciences (EECS)", "year": "2021"}
            ],
            "certifications": ["AWS Certified Machine Learning - Specialty", "Certified Kubernetes Administrator (CKA)"]
        },
        "summary": {
            "executive": "High-impact Staff AI Platform Engineer profile with proven expertise in building OpenRouter AI gateways, pgvector semantic search systems, and high-throughput document processing engines.",
            "bullets": [
                "Scaled OpenRouter gateway handling 12M requests/day at Cognitive Scale Labs.",
                "Reduced API token spend by 44% via intelligent model routing.",
                "EECS graduate from UC Berkeley with AWS ML Specialty and CKA certifications."
            ],
            "tldr": "Staff AI Platform Engineer with 7+ years building enterprise OpenRouter gateways and pgvector RAG pipelines.",
            "action_items": ["Schedule technical architecture interview focusing on distributed vector search and LLM gateway routing."]
        }
    }
]
