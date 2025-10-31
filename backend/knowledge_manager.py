"""
Knowledge Manager for Video Agent
Loads knowledge base files into memory and provides formatting functions.
"""
import os
from pathlib import Path


PROMPT_HEADER = "## HARDWARE UPGRADE KNOWLEDGE BASE"
PROMPT_DESCRIPTION = """
### Critical Instructions for Hardware Assistance
YOU ARE A HARDWARE UPGRADE ASSISTANT. Your role is to guide users through RAM, battery, SSD, and WiFi card upgrades with EXTREME PRECISION.

**Interaction Rules:**
1. ALWAYS present ONE step at a time — never list multiple steps in advance
2. WAIT for user confirmation ("yes", "done") before proceeding to next step
3. Use EXACT physical descriptions: "remove the screw on the LEFT side", "press clips OUTWARD"
4. Give clear INSTRUCTIONS by default — users can follow text directions
5. Accept photos when user provides them, but DON'T ask for photos unless user is stuck or confused
6. Prioritize safety: remind about power-off, grounding, and anti-static precautions

**Response Style:**
- **Instruction mode (default):** Provide clear text instructions with precise physical directions
- **Visual mode (when user sends photo):** Describe what you see and give next steps based on the image
- Trust the user to follow instructions — only suggest photo if they say "I'm not sure" or "I don't see it"

**Image Analysis Integration:**
- When users upload component images, you receive STRUCTURED DATA with:
  - `components[]`: Array of detected hardware (id, name, type, position, size, details, upgrade_category)
  - `recommendations[]`: Array with specific next steps for each component
  - `summary`: Detection overview
- Use this structured data to give PRECISE instructions referencing the detected components
- Example: "I detected RAM (DDR4 SO-DIMM) in the upper-left slot. Let's upgrade it. Step 1: Power off completely..."
- Reference component IDs from structured_data when guiding through multi-component upgrades

**Knowledge Structure:**
- DASHBOARD: Step-by-step upgrade procedures (RAM, battery, SSD, WiFi) — your primary reference
- TROUBLESHOOTING (export): Common issues and fixes when things go wrong
- REFERENCE (permissions): Visual identification guides, compatibility checks, screw types

**When answering:**
- Reference the exact procedure from DASHBOARD knowledge
- If user reports a problem, consult TROUBLESHOOTING knowledge
- Before any upgrade, confirm compatibility using REFERENCE knowledge
- Always verify user has the correct tools and workspace setup
- When structured_data is available, use it to personalize instructions
"""
        

class KnowledgeManager:
    """
    Manages knowledge base files for the video agent.
    Provides formatted access to knowledge files.
    """
    
    def __init__(self, knowledge_dir=None):
        """Initialize with the directory containing knowledge files"""
        if knowledge_dir is None:
            # Default to the 'knowledge' directory in the same folder as this file
            self.knowledge_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "knowledge"
        else:
            self.knowledge_dir = Path(knowledge_dir)
            
        # Knowledge files mapping
        self.knowledge_files = {
            "dashboard": self.knowledge_dir / "dashboard.md",
            "export": self.knowledge_dir / "export.md",
            "permissions": self.knowledge_dir / "permissions.md",
            "tools": self.knowledge_dir / "tools.md",
            "safety": self.knowledge_dir / "safety.md",
            "advanced": self.knowledge_dir / "advanced.md",
        }
        
        # Load all knowledge files into memory
        self.knowledge_content = self._load_all_knowledge()
        
    def _load_all_knowledge(self):
        """Load all knowledge files into memory"""
        content = {}
        for domain, file_path in self.knowledge_files.items():
            if file_path.exists():
                # Open knowledge files using UTF-8 and replace undecodable
                # bytes to avoid UnicodeDecodeError on platforms where the
                # file encoding may differ (for example Windows cp1252).
                # Replacing invalid bytes is safer than failing at startup.
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content[domain] = f.read()
            else:
                content[domain] = ""
        return content
    
    def format_knowledge(self):
        """
        Format all knowledge for insertion into a prompt.
        Returns a formatted string with all knowledge content.
        """
        # Map domain names to readable labels
        domain_labels = {
            "dashboard": "UPGRADE PROCEDURES",
            "export": "TROUBLESHOOTING GUIDE",
            "permissions": "VISUAL REFERENCE & COMPATIBILITY",
            "tools": "TOOLS & EQUIPMENT GUIDE",
            "safety": "SAFETY PROCEDURES & WARNINGS",
            "advanced": "ADVANCED PROCEDURES & POST-INSTALLATION"
        }
        
        # Format each knowledge file with its label and content
        knowledge_sections = []
        for domain, content in self.knowledge_content.items():
            if content.strip():
                label = domain_labels.get(domain, domain.upper())
                formatted_section = f"### {label}\n\n{content}"
                knowledge_sections.append(formatted_section)
        
        # Combine all sections
        all_knowledge = "\n\n---\n\n".join([PROMPT_HEADER, PROMPT_DESCRIPTION] + knowledge_sections)
        return all_knowledge
