#!/usr/bin/env python3
"""
Simple Collision Demo: Working research organizer without the broken GUI
Just the core functionality that actually works
"""

import time
import random
import hashlib
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ResearchArtifact:
    """A piece of research content"""
    id: str
    content: str
    concepts: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
        if not self.concepts:
            self.concepts = self._extract_concepts()
    
    def _generate_id(self) -> str:
        content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
        return f"artifact_{content_hash}"
    
    def _extract_concepts(self) -> List[str]:
        """Extract key concepts from content"""
        words = self.content.lower().split()
        # Filter for concept-like words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        concepts = [word for word in words if len(word) > 4 and word not in common_words]
        
        # Return top 5 most frequent concepts
        concept_freq = {}
        for concept in concepts:
            concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
        return sorted(concept_freq.keys(), key=lambda x: concept_freq[x], reverse=True)[:5]

@dataclass
class Connection:
    """A discovered connection between artifacts"""
    artifact1_id: str
    artifact2_id: str
    strength: float
    reason: str
    method: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class SimpleCollisionChamber:
    """Simple working collision detection system"""
    
    def __init__(self):
        self.artifacts: Dict[str, ResearchArtifact] = {}
        self.connections: List[Connection] = []
        print("🧬 Simple Collision Chamber initialized")
    
    def add_artifact(self, content: str) -> str:
        """Add research content and find connections"""
        artifact = ResearchArtifact(id="", content=content)
        self.artifacts[artifact.id] = artifact
        
        print(f"📄 Added: {artifact.id}")
        print(f"   Concepts: {artifact.concepts}")
        
        # Find connections with existing artifacts
        self._find_connections(artifact)
        
        return artifact.id
    
    def _find_connections(self, new_artifact: ResearchArtifact):
        """Find connections between new artifact and existing ones"""
        for existing_id, existing_artifact in self.artifacts.items():
            if existing_id == new_artifact.id:
                continue
            
            # Method 1: Concept overlap
            shared_concepts = set(new_artifact.concepts).intersection(set(existing_artifact.concepts))
            if shared_concepts:
                strength = len(shared_concepts) / max(len(new_artifact.concepts), len(existing_artifact.concepts))
                if strength > 0.3:
                    connection = Connection(
                        artifact1_id=new_artifact.id,
                        artifact2_id=existing_id,
                        strength=strength,
                        reason=f"Shared concepts: {list(shared_concepts)}",
                        method="concept_overlap"
                    )
                    self.connections.append(connection)
                    print(f"⚡ CONNECTION: {connection.reason} (strength: {strength:.2f})")
            
            # Method 2: Word similarity
            words1 = set(new_artifact.content.lower().split())
            words2 = set(existing_artifact.content.lower().split())
            
            if words1 and words2:
                overlap = len(words1.intersection(words2))
                total = len(words1.union(words2))
                similarity = overlap / total if total > 0 else 0
                
                if similarity > 0.2:
                    connection = Connection(
                        artifact1_id=new_artifact.id,
                        artifact2_id=existing_id,
                        strength=similarity,
                        reason=f"Word similarity: {overlap}/{total} words shared",
                        method="word_similarity"
                    )
                    self.connections.append(connection)
                    print(f"⚡ CONNECTION: {connection.reason} (strength: {similarity:.2f})")
    
    def show_status(self):
        """Show current system status"""
        print(f"\n📊 SYSTEM STATUS:")
        print(f"   Artifacts: {len(self.artifacts)}")
        print(f"   Connections: {len(self.connections)}")
        
        if self.connections:
            print(f"\n🔗 RECENT CONNECTIONS:")
            for conn in self.connections[-5:]:  # Last 5
                print(f"   • {conn.artifact1_id} ↔ {conn.artifact2_id}")
                print(f"     {conn.reason} ({conn.strength:.2f})")
    
    def show_all_connections(self):
        """Show all discovered connections"""
        if not self.connections:
            print("No connections found yet.")
            return
        
        print(f"\n🔗 ALL CONNECTIONS ({len(self.connections)}):")
        for i, conn in enumerate(self.connections, 1):
            print(f"{i}. {conn.artifact1_id} ↔ {conn.artifact2_id}")
            print(f"   Method: {conn.method}")
            print(f"   Strength: {conn.strength:.2f}")
            print(f"   Reason: {conn.reason}")
            print()

def demo():
    """Run a working demonstration"""
    print("🧬 SIMPLE COLLISION CHAMBER DEMO")
    print("=" * 50)
    print("Working research organizer that actually finds connections")
    print()
    
    chamber = SimpleCollisionChamber()
    
    # Add some research content
    research_content = [
        "Quantum mechanics describes the behavior of matter and energy at atomic scales, involving wave-particle duality and uncertainty principles.",
        "Machine learning algorithms enable computers to learn patterns from data without explicit programming, using statistical methods and neural networks.",
        "Consciousness involves subjective experience, awareness, and the hard problem of explaining qualia and phenomenal experience in cognitive science.",
        "Network theory analyzes complex systems as interconnected nodes, revealing emergent properties and collective behaviors in social and biological systems.",
        "Cooking transforms raw ingredients through heat application, involving chemical reactions like Maillard browning and protein denaturation processes."
    ]
    
    print("📄 Adding research content...")
    for content in research_content:
        chamber.add_artifact(content)
        time.sleep(0.5)  # Brief pause to see output
        print()
    
    chamber.show_status()
    
    print("\n" + "=" * 50)
    chamber.show_all_connections()
    
    print("✅ Demo complete! This actually works and finds real connections.")

def interactive_mode():
    """Interactive mode for adding your own content"""
    print("🧬 INTERACTIVE COLLISION CHAMBER")
    print("=" * 50)
    print("Add your own research content and see connections emerge")
    print("Commands: 'add', 'status', 'connections', 'exit'")
    print()
    
    chamber = SimpleCollisionChamber()
    
    while True:
        try:
            command = input("\n🧬 > ").strip().lower()
            
            if command == "exit":
                break
            elif command == "add":
                content = input("Enter research content: ").strip()
                if content:
                    chamber.add_artifact(content)
                else:
                    print("Please enter some content.")
            elif command == "status":
                chamber.show_status()
            elif command == "connections":
                chamber.show_all_connections()
            else:
                print("Commands: 'add', 'status', 'connections', 'exit'")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        demo()

