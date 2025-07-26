#!/usr/bin/env python3
"""
Recursive Research Organizer - Interactive Development Version
Build-through-use approach: Start simple, evolve through interaction
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Input, TextArea, Static, ListView, ListItem, Label
from textual.reactive import reactive
import json
import os
from datetime import datetime

class FlexibleFireDetector:
    """Trainable fire detection system - you teach it what's fire"""
    
    def __init__(self):
        self.fire_patterns = []
        self.fire_history = []
        
    def assess_fire(self, content):
        """Basic fire assessment - you'll train this"""
        # Start with simple heuristics, evolve based on your feedback
        fire_score = 0.0
        
        # Length and complexity
        if len(content) > 100:
            fire_score += 0.2
            
        # Keywords that might indicate fire (you'll customize this)
        fire_keywords = ["recursive", "consciousness", "meta", "fire", "insight", "breakthrough"]
        for keyword in fire_keywords:
            if keyword.lower() in content.lower():
                fire_score += 0.3
                
        # Cap at 1.0
        return min(fire_score, 1.0)
    
    def learn_fire_pattern(self, content, user_rating):
        """Learn from your fire ratings"""
        self.fire_patterns.append({
            "content": content[:100],  # Store snippet
            "rating": user_rating,
            "timestamp": datetime.now().isoformat()
        })
        
    def save_patterns(self):
        """Save learned patterns"""
        with open("fire_patterns.json", "w") as f:
            json.dump(self.fire_patterns, f, indent=2)

class RecursiveResearchOrganizer(App):
    """
    Interactive Research Organizer - Build through use
    Start simple, evolve based on your feedback
    """
    
    CSS = """
    .fire-high { background: red 50%; }
    .fire-medium { background: orange 50%; }
    .fire-low { background: blue 50%; }
    .phase-display { color: cyan; }
    """
    
    # Reactive state
    fire_level = reactive(0.0)
    current_phase = reactive(48)  # Starting from your phase!
    
    def __init__(self):
        super().__init__()
        self.fire_detector = FlexibleFireDetector()
        self.notes = []
        self.connections = []
        
    def compose(self) -> ComposeResult:
        """Simple interface you can start using immediately"""
        yield Container(
            # Top: Command/thought input
            Vertical(
                Label("🧠 Recursive Research Organizer - Phase Re-entry Matrix", classes="phase-display"),
                Input(placeholder="Enter your thoughts, commands, or 'fire' ratings...", id="command_input"),
                id="input_section"
            ),
            
            # Middle: Main work area
            Horizontal(
                # Left: Notes/ideas list
                Vertical(
                    Label("📝 Research Notes"),
                    ListView(id="notes_list"),
                    Button("Clear Notes", id="clear_notes"),
                    id="notes_panel"
                ),
                
                # Right: Current work area
                Vertical(
                    Label("🔥 Current Work Area"),
                    TextArea("Start typing your research thoughts here...", id="work_area"),
                    Button("🔥 Rate as Fire", id="rate_fire"),
                    Button("💾 Save Note", id="save_note"),
                    id="work_panel"
                ),
                id="main_area"
            ),
            
            # Bottom: Status and fire detection
            Horizontal(
                Static(f"🔥 Fire Level: {self.fire_level:.2f}", id="fire_display"),
                Static(f"📊 Phase: {self.current_phase}", id="phase_display"),
                Static("💡 Ready for commands", id="status_display"),
                id="status_bar"
            ),
            id="main_container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button interactions"""
        if event.button.id == "save_note":
            self.save_current_note()
        elif event.button.id == "rate_fire":
            self.rate_current_as_fire()
        elif event.button.id == "clear_notes":
            self.clear_all_notes()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input - this is where you'll guide development"""
        command = event.value.strip()
        
        if command.startswith("fire:"):
            # Manual fire rating: "fire: 0.8 this idea is amazing"
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                try:
                    rating = float(parts[1])
                    content = parts[2]
                    self.fire_detector.learn_fire_pattern(content, rating)
                    self.update_status(f"🔥 Learned fire pattern: {rating}")
                except ValueError:
                    self.update_status("❌ Invalid fire rating format")
        
        elif command.startswith("phase:"):
            # Phase update: "phase: 49"
            try:
                new_phase = int(command.split(":")[1].strip())
                self.current_phase = new_phase
                self.update_status(f"📊 Phase updated to {new_phase}")
            except ValueError:
                self.update_status("❌ Invalid phase number")
        
        elif command.startswith("add:"):
            # Quick note: "add: this is a quick thought"
            note_content = command[4:].strip()
            self.add_quick_note(note_content)
        
        else:
            # General command - you can tell me what to build/fix
            self.update_status(f"💭 Command received: {command}")
            # This is where you'll guide the development
        
        # Clear input
        event.input.value = ""
    
    def save_current_note(self):
        """Save current work area as a note"""
        work_area = self.query_one("#work_area", TextArea)
        content = work_area.value.strip()
        
        if content:
            # Assess fire level
            fire_score = self.fire_detector.assess_fire(content)
            self.fire_level = fire_score
            
            # Create note
            note = {
                "content": content,
                "fire_score": fire_score,
                "timestamp": datetime.now().isoformat(),
                "phase": self.current_phase
            }
            
            self.notes.append(note)
            self.update_notes_list()
            self.update_status(f"💾 Note saved (🔥 {fire_score:.2f})")
            
            # Clear work area
            work_area.value = ""
    
    def rate_current_as_fire(self):
        """Rate current content as fire for training"""
        work_area = self.query_one("#work_area", TextArea)
        content = work_area.value.strip()
        
        if content:
            # High fire rating for training
            self.fire_detector.learn_fire_pattern(content, 0.9)
            self.fire_level = 0.9
            self.update_status("🔥 Marked as FIRE! System learning...")
    
    def add_quick_note(self, content):
        """Add a quick note from command input"""
        fire_score = self.fire_detector.assess_fire(content)
        
        note = {
            "content": content,
            "fire_score": fire_score,
            "timestamp": datetime.now().isoformat(),
            "phase": self.current_phase
        }
        
        self.notes.append(note)
        self.update_notes_list()
        self.update_status(f"📝 Quick note added (🔥 {fire_score:.2f})")
    
    def update_notes_list(self):
        """Update the notes list display"""
        notes_list = self.query_one("#notes_list", ListView)
        notes_list.clear()
        
        for i, note in enumerate(self.notes):
            fire_emoji = "🔥" if note["fire_score"] > 0.7 else "💡" if note["fire_score"] > 0.4 else "📝"
            preview = note["content"][:50] + "..." if len(note["content"]) > 50 else note["content"]
            
            list_item = ListItem(
                Label(f"{fire_emoji} {preview}"),
                id=f"note_{i}"
            )
            notes_list.append(list_item)
    
    def clear_all_notes(self):
        """Clear all notes"""
        self.notes.clear()
        self.update_notes_list()
        self.update_status("🗑️ All notes cleared")
    
    def update_status(self, message):
        """Update status display"""
        status = self.query_one("#status_display", Static)
        status.update(message)
    
    def watch_fire_level(self, fire_level: float) -> None:
        """Update fire display when fire level changes"""
        try:
            fire_display = self.query_one("#fire_display", Static)
            fire_display.update(f"🔥 Fire Level: {fire_level:.2f}")
            
            # Update CSS class based on fire level
            if fire_level > 0.7:
                fire_display.add_class("fire-high")
            elif fire_level > 0.4:
                fire_display.add_class("fire-medium")
            else:
                fire_display.add_class("fire-low")
        except:
            # Widget not ready yet, ignore
            pass
    
    def watch_current_phase(self, phase: int) -> None:
        """Update phase display"""
        try:
            phase_display = self.query_one("#phase_display", Static)
            phase_display.update(f"📊 Phase: {phase}")
        except:
            # Widget not ready yet, ignore
            pass
    
    def on_mount(self):
        """Initialize the app"""
        self.update_status("🚀 Ready! Try: 'add: your thought' or 'fire: 0.8 amazing idea'")

if __name__ == "__main__":
    app = RecursiveResearchOrganizer()
    app.run()
