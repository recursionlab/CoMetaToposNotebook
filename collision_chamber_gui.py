#!/usr/bin/env python3
"""
Collision Chamber GUI: Real-time visualization of self-modifying research organizer
Shows the system evolving its own algorithms in real-time
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import time
import json
from typing import Dict, List, Any
from datetime import datetime
import queue

from recursive_collision_chamber import RecursiveCollisionChamber, CollisionResult

class CollisionVisualizationCanvas:
    """Canvas for visualizing artifact collisions in real-time"""
    
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg='#0a0a0a', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.artifact_positions = {}
        self.collision_lines = []
        self.animation_queue = queue.Queue()
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.animation_thread.start()
    
    def add_artifact(self, artifact_id: str, content_preview: str):
        """Add an artifact to the visualization"""
        import random
        
        # Random position for new artifact
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        
        # Create visual representation
        node_id = self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                         fill='#00ff88', outline='#ffffff', width=2)
        
        text_id = self.canvas.create_text(x, y-35, text=content_preview[:20] + "...", 
                                         fill='#ffffff', font=('Arial', 8))
        
        self.artifact_positions[artifact_id] = {
            'x': x, 'y': y, 
            'node_id': node_id, 
            'text_id': text_id
        }
        
        # Animate appearance
        self.animation_queue.put({
            'type': 'artifact_added',
            'artifact_id': artifact_id,
            'position': (x, y)
        })
    
    def show_collision(self, collision: CollisionResult):
        """Visualize a collision between artifacts"""
        if len(collision.artifact_ids) >= 2:
            art1_id, art2_id = collision.artifact_ids[0], collision.artifact_ids[1]
            
            if art1_id in self.artifact_positions and art2_id in self.artifact_positions:
                pos1 = self.artifact_positions[art1_id]
                pos2 = self.artifact_positions[art2_id]
                
                # Color based on strength
                if collision.strength > 0.8:
                    color = '#ff4444'  # Strong - red
                elif collision.strength > 0.6:
                    color = '#ffaa00'  # Medium - orange
                else:
                    color = '#4488ff'  # Weak - blue
                
                # Create connection line
                line_id = self.canvas.create_line(
                    pos1['x'], pos1['y'], pos2['x'], pos2['y'],
                    fill=color, width=max(1, int(collision.strength * 5)),
                    dash=(5, 5) if collision.strength < 0.6 else None
                )
                
                self.collision_lines.append({
                    'line_id': line_id,
                    'collision': collision,
                    'created_at': time.time()
                })
                
                # Animate collision
                self.animation_queue.put({
                    'type': 'collision_detected',
                    'collision': collision,
                    'line_id': line_id
                })
                
                # Schedule line removal after 10 seconds
                self.canvas.after(10000, lambda: self._remove_collision_line(line_id))
    
    def _remove_collision_line(self, line_id):
        """Remove a collision line after timeout"""
        try:
            self.canvas.delete(line_id)
            self.collision_lines = [cl for cl in self.collision_lines if cl['line_id'] != line_id]
        except:
            pass
    
    def _animation_loop(self):
        """Background animation processing"""
        while True:
            try:
                animation = self.animation_queue.get(timeout=1)
                self._process_animation(animation)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Animation error: {e}")
    
    def _process_animation(self, animation):
        """Process animation events"""
        if animation['type'] == 'artifact_added':
            # Pulse effect for new artifacts
            artifact_id = animation['artifact_id']
            if artifact_id in self.artifact_positions:
                node_id = self.artifact_positions[artifact_id]['node_id']
                
                # Pulse animation
                for i in range(3):
                    self.canvas.after(i * 200, lambda: self._pulse_node(node_id, '#ffff00'))
                    self.canvas.after(i * 200 + 100, lambda: self._pulse_node(node_id, '#00ff88'))
        
        elif animation['type'] == 'collision_detected':
            # Flash effect for collisions
            line_id = animation['line_id']
            collision = animation['collision']
            
            # Flash the connection line
            for i in range(5):
                self.canvas.after(i * 100, lambda: self._flash_line(line_id, '#ffffff'))
                self.canvas.after(i * 100 + 50, lambda: self._restore_line_color(line_id, collision))
    
    def _pulse_node(self, node_id, color):
        """Pulse a node with given color"""
        try:
            self.canvas.itemconfig(node_id, fill=color)
        except:
            pass
    
    def _flash_line(self, line_id, color):
        """Flash a line with given color"""
        try:
            self.canvas.itemconfig(line_id, fill=color)
        except:
            pass
    
    def _restore_line_color(self, line_id, collision):
        """Restore line to original color"""
        try:
            if collision.strength > 0.8:
                color = '#ff4444'
            elif collision.strength > 0.6:
                color = '#ffaa00'
            else:
                color = '#4488ff'
            self.canvas.itemconfig(line_id, fill=color)
        except:
            pass
    
    def clear_visualization(self):
        """Clear all visualizations"""
        self.canvas.delete("all")
        self.artifact_positions.clear()
        self.collision_lines.clear()

class CollisionChamberGUI:
    """Main GUI for the Recursive Collision Chamber"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧬 Recursive Collision Chamber - Self-Modifying Research Organizer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize collision chamber
        self.chamber = RecursiveCollisionChamber()
        
        # GUI state
        self.update_thread = None
        self.is_running = True
        
        self._setup_styles()
        self._create_interface()
        self._start_update_thread()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_styles(self):
        """Setup dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Dark.TLabel', background='#1a1a1a', foreground='#00ff88')
        style.configure('Dark.TButton', background='#2a2a2a', foreground='#00ff88')
        style.configure('Evolution.TLabel', background='#1a1a1a', foreground='#ff4444', font=('Courier', 10, 'bold'))
    
    def _create_interface(self):
        """Create the main interface"""
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🧬 Recursive Collision Chamber - Real Self-Modification in Action",
            style='Evolution.TLabel'
        )
        title_label.pack(pady=10)
        
        # Create paned window for layout
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls and status
        left_panel = ttk.Frame(paned_window, style='Dark.TFrame')
        paned_window.add(left_panel, weight=1)
        
        # Right panel - Visualization
        right_panel = ttk.Frame(paned_window, style='Dark.TFrame')
        paned_window.add(right_panel, weight=2)
        
        self._create_left_panel(left_panel)
        self._create_right_panel(right_panel)
    
    def _create_left_panel(self, parent):
        """Create left control panel"""
        
        # Add artifact section
        artifact_frame = ttk.LabelFrame(parent, text="Add Research Artifacts", style='Dark.TFrame')
        artifact_frame.pack(fill=tk.X, pady=5)
        
        # Text input
        ttk.Label(artifact_frame, text="Content:", style='Dark.TLabel').pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(
            artifact_frame, height=4, width=40, 
            bg='#0a0a0a', fg='#00ff88', insertbackground='#00ff88'
        )
        self.content_text.pack(fill=tk.X, pady=5)
        
        # Content type selection
        type_frame = ttk.Frame(artifact_frame, style='Dark.TFrame')
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Type:", style='Dark.TLabel').pack(side=tk.LEFT)
        
        self.content_type_var = tk.StringVar(value="text")
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.content_type_var,
            values=["text", "pdf", "link", "code", "image"]
        )
        type_combo.pack(side=tk.LEFT, padx=10)\n        \n        # Add button\n        add_btn = ttk.Button(\n            artifact_frame,\n            text=\"Add Artifact\",\n            command=self._add_artifact,\n            style='Dark.TButton'\n        )\n        add_btn.pack(pady=5)\n        \n        # File upload button\n        upload_btn = ttk.Button(\n            artifact_frame,\n            text=\"Upload File\",\n            command=self._upload_file,\n            style='Dark.TButton'\n        )\n        upload_btn.pack(pady=2)\n        \n        # System status section\n        status_frame = ttk.LabelFrame(parent, text=\"System Status\", style='Dark.TFrame')\n        status_frame.pack(fill=tk.X, pady=5)\n        \n        self.status_text = scrolledtext.ScrolledText(\n            status_frame, height=8, width=40,\n            bg='#0a0a0a', fg='#00ff88', insertbackground='#00ff88'\n        )\n        self.status_text.pack(fill=tk.X, pady=5)\n        \n        # Evolution controls\n        evolution_frame = ttk.LabelFrame(parent, text=\"Evolution Controls\", style='Dark.TFrame')\n        evolution_frame.pack(fill=tk.X, pady=5)\n        \n        evolve_btn = ttk.Button(\n            evolution_frame,\n            text=\"🔄 Force Evolution\",\n            command=self._force_evolution,\n            style='Dark.TButton'\n        )\n        evolve_btn.pack(pady=2)\n        \n        chaos_btn = ttk.Button(\n            evolution_frame,\n            text=\"💣 Inject Chaos\",\n            command=self._inject_chaos,\n            style='Dark.TButton'\n        )\n        chaos_btn.pack(pady=2)\n        \n        clear_btn = ttk.Button(\n            evolution_frame,\n            text=\"🗑️ Clear All\",\n            command=self._clear_all,\n            style='Dark.TButton'\n        )\n        clear_btn.pack(pady=2)\n        \n        # Collision results section\n        results_frame = ttk.LabelFrame(parent, text=\"Recent Collisions\", style='Dark.TFrame')\n        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)\n        \n        self.results_text = scrolledtext.ScrolledText(\n            results_frame, height=10, width=40,\n            bg='#0a0a0a', fg='#00ff88', insertbackground='#00ff88'\n        )\n        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)\n    \n    def _create_right_panel(self, parent):\n        \"\"\"Create right visualization panel\"\"\"\n        \n        # Visualization title\n        viz_title = ttk.Label(\n            parent,\n            text=\"🎯 Real-time Collision Visualization\",\n            style='Evolution.TLabel'\n        )\n        viz_title.pack(pady=5)\n        \n        # Create visualization canvas\n        self.visualization = CollisionVisualizationCanvas(parent)\n        \n        # Legend\n        legend_frame = ttk.Frame(parent, style='Dark.TFrame')\n        legend_frame.pack(fill=tk.X, pady=5)\n        \n        ttk.Label(legend_frame, text=\"Legend:\", style='Dark.TLabel').pack(side=tk.LEFT)\n        ttk.Label(legend_frame, text=\"🔴 Strong (>0.8)\", style='Dark.TLabel').pack(side=tk.LEFT, padx=10)\n        ttk.Label(legend_frame, text=\"🟠 Medium (>0.6)\", style='Dark.TLabel').pack(side=tk.LEFT, padx=10)\n        ttk.Label(legend_frame, text=\"🔵 Weak (<0.6)\", style='Dark.TLabel').pack(side=tk.LEFT, padx=10)\n    \n    def _add_artifact(self):\n        \"\"\"Add artifact from text input\"\"\"\n        content = self.content_text.get(\"1.0\", tk.END).strip()\n        if not content:\n            messagebox.showwarning(\"Warning\", \"Please enter some content\")\n            return\n        \n        content_type = self.content_type_var.get()\n        \n        try:\n            artifact_id = self.chamber.add_artifact(content, content_type)\n            \n            # Add to visualization\n            self.visualization.add_artifact(artifact_id, content)\n            \n            # Clear input\n            self.content_text.delete(\"1.0\", tk.END)\n            \n            # Update status\n            self._log_message(f\"✅ Added artifact: {artifact_id} ({content_type})\")\n            \n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Failed to add artifact: {e}\")\n    \n    def _upload_file(self):\n        \"\"\"Upload file as artifact\"\"\"\n        file_path = filedialog.askopenfilename(\n            title=\"Select Research File\",\n            filetypes=[\n                (\"Text files\", \"*.txt\"),\n                (\"PDF files\", \"*.pdf\"),\n                (\"All files\", \"*.*\")\n            ]\n        )\n        \n        if file_path:\n            try:\n                # Read file content\n                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:\n                    content = f.read()\n                \n                # Determine content type from extension\n                if file_path.endswith('.pdf'):\n                    content_type = 'pdf'\n                elif file_path.endswith('.py'):\n                    content_type = 'code'\n                else:\n                    content_type = 'text'\n                \n                # Add artifact\n                artifact_id = self.chamber.add_artifact(\n                    content, \n                    content_type, \n                    {'filename': file_path.split('/')[-1]}\n                )\n                \n                # Add to visualization\n                self.visualization.add_artifact(artifact_id, content)\n                \n                self._log_message(f\"📁 Uploaded file: {file_path.split('/')[-1]} as {artifact_id}\")\n                \n            except Exception as e:\n                messagebox.showerror(\"Error\", f\"Failed to upload file: {e}\")\n    \n    def _force_evolution(self):\n        \"\"\"Force system evolution\"\"\"\n        self.chamber.force_evolution()\n        self._log_message(\"🔄 Forced system evolution\")\n    \n    def _inject_chaos(self):\n        \"\"\"Inject chaos for testing\"\"\"\n        self.chamber.inject_chaos()\n        self._log_message(\"💣 Injected chaos - testing system robustness\")\n    \n    def _clear_all(self):\n        \"\"\"Clear all artifacts and visualizations\"\"\"\n        result = messagebox.askyesno(\"Confirm\", \"Clear all artifacts and start fresh?\")\n        if result:\n            # Create new chamber\n            self.chamber.shutdown()\n            self.chamber = RecursiveCollisionChamber()\n            \n            # Clear visualization\n            self.visualization.clear_visualization()\n            \n            # Clear text areas\n            self.status_text.delete(\"1.0\", tk.END)\n            self.results_text.delete(\"1.0\", tk.END)\n            \n            self._log_message(\"🗑️ Cleared all artifacts - fresh start\")\n    \n    def _log_message(self, message: str):\n        \"\"\"Log message to status area\"\"\"\n        timestamp = datetime.now().strftime(\"%H:%M:%S\")\n        log_entry = f\"[{timestamp}] {message}\\n\"\n        \n        self.status_text.insert(tk.END, log_entry)\n        self.status_text.see(tk.END)\n    \n    def _start_update_thread(self):\n        \"\"\"Start background update thread\"\"\"\n        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)\n        self.update_thread.start()\n    \n    def _update_loop(self):\n        \"\"\"Background update loop\"\"\"\n        last_collision_count = 0\n        last_status_update = 0\n        \n        while self.is_running:\n            try:\n                # Check for new collisions\n                current_collisions = self.chamber.collision_results\n                if len(current_collisions) > last_collision_count:\n                    # Show new collisions\n                    new_collisions = current_collisions[last_collision_count:]\n                    for collision in new_collisions:\n                        if collision.is_significant():\n                            # Add to visualization\n                            self.visualization.show_collision(collision)\n                            \n                            # Log to results\n                            self.root.after(0, lambda c=collision: self._log_collision(c))\n                    \n                    last_collision_count = len(current_collisions)\n                \n                # Update status periodically\n                if time.time() - last_status_update > 5:  # Every 5 seconds\n                    self.root.after(0, self._update_status_display)\n                    last_status_update = time.time()\n                \n                time.sleep(1)  # Update every second\n                \n            except Exception as e:\n                print(f\"Update loop error: {e}\")\n                time.sleep(5)\n    \n    def _log_collision(self, collision: CollisionResult):\n        \"\"\"Log collision to results area\"\"\"\n        timestamp = datetime.now().strftime(\"%H:%M:%S\")\n        log_entry = f\"[{timestamp}] {collision.connection_type}\\n\"\n        log_entry += f\"  Strength: {collision.strength:.2f}\\n\"\n        log_entry += f\"  Method: {collision.generated_by_method}\\n\"\n        log_entry += f\"  Insight: {collision.insight[:60]}...\\n\\n\"\n        \n        self.results_text.insert(tk.END, log_entry)\n        self.results_text.see(tk.END)\n        \n        # Keep only last 20 entries\n        lines = self.results_text.get(\"1.0\", tk.END).split(\"\\n\")\n        if len(lines) > 100:  # Approximately 20 entries\n            self.results_text.delete(\"1.0\", \"20.0\")\n    \n    def _update_status_display(self):\n        \"\"\"Update status display\"\"\"\n        try:\n            status = self.chamber.get_system_status()\n            \n            status_text = f\"\"\"🧬 SYSTEM STATUS\n{'='*30}\nArtifacts: {status['artifacts_count']}\nTotal Collisions: {status['total_collisions']}\nSignificant: {status['significant_collisions']}\nActive Methods: {status['active_methods']}\nGeneration: {status['generation_count']}\nFailures: {status['failure_count']}\n\n📊 METHOD PERFORMANCE\n{'='*30}\n\"\"\"\n            \n            for method, performance in status['method_performance'].items():\n                status_text += f\"{method}: {performance:.3f}\\n\"\n            \n            # Show evolution history\n            evolution_history = self.chamber.get_evolution_history()\n            if evolution_history:\n                status_text += f\"\\n🧬 RECENT EVOLUTION\\n{'='*30}\\n\"\n                for evolution in evolution_history[-3:]:  # Last 3\n                    status_text += f\"Gen {evolution['generation']}: {evolution['method_name']}\\n\"\n            \n            # Update display\n            self.status_text.delete(\"1.0\", tk.END)\n            self.status_text.insert(\"1.0\", status_text)\n            \n        except Exception as e:\n            print(f\"Status update error: {e}\")\n    \n    def _on_closing(self):\n        \"\"\"Handle window closing\"\"\"\n        self.is_running = False\n        self.chamber.shutdown()\n        self.root.destroy()\n    \n    def run(self):\n        \"\"\"Run the GUI\"\"\"\n        self.root.mainloop()\n\ndef main():\n    \"\"\"Launch the Collision Chamber GUI\"\"\"\n    print(\"🧬 Launching Recursive Collision Chamber GUI...\")\n    print(\"Real-time visualization of self-modifying research organizer\")\n    print()\n    \n    app = CollisionChamberGUI()\n    app.run()\n\nif __name__ == \"__main__\":\n    main()
