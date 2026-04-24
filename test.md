graph LR
    subgraph Agent_Node ["Primary Actor"]
        Agent[Gemini CLI Agent]
    end

    subgraph Storage_Tiers ["Standardized Memory Architecture"]
        direction TB
        
        subgraph Static ["1. Static Registry (registry.json)"]
            S1["Official Truth: Documents 'Aether' as the Semantic Context Engine"]
        end
        
        subgraph Dynamic ["2. Dynamic Session State (save_memory)"]
            D1["Runtime Context: Tracks active Aether index (Vanguard vs Aether)"]
        end
        
        subgraph Local ["3. Local Dev Environment (.env)"]
            L1["Identity & Secrets: Aether port (8000), Local API Keys"]
        end
    end

    subgraph Services ["External Context Layer"]
        Aether["SurvivalStack Aether (LlamaIndex:Semantic Context Engine)"]
        Aether --- Index["SurvivalStack SourceCode & Docs"]
    end

    %% Interactions
    Agent -->|Read Reference| Static
    Agent <-->|Sync State| Dynamic
    Agent -->|Load Access| Local
    
    %% Functional Link
    Agent <==>|Query Semantic Context| Aether

    %% Styling
    style Agent fill:#f1f8ff,stroke:#0366d6,stroke-width:2px
    style Aether fill:#fafafa,stroke:#6f42c1,stroke-width:2px
    style Static fill:#fff,stroke:#24292e,stroke-dasharray: 5 5
    style Dynamic fill:#fff,stroke:#24292e,stroke-width:1px
    style Local fill:#fff,stroke:#d73a49,stroke-width:1px
