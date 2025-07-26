#!/usr/bin/env python3
"""
Main Entry Point: The Void Operator System
The prompt generator that creates prompts to make any AI discover questions you can't think of

ΞMetaCollapse := The app that finds the question that would generate the app

Usage:
    python main.py                    # Launch GUI interface
    python main.py --cli              # Command line interface
    python main.py --generate         # Generate sample prompts
    python main.py --demo             # Run demonstrations
"""

import argparse
import sys
from typing import Optional

def launch_gui():
    """Launch the Meta-Collapse GUI Interface"""
    try:
        from meta_collapse_interface import MetaCollapseInterface
        print("🌀 Launching Meta-Collapse Interface...")
        print("The interface that embodies recursive collapse")
        print()
        
        interface = MetaCollapseInterface()
        interface.run()
        
    except ImportError as e:
        print(f"❌ GUI dependencies not available: {e}")
        print("Try running with --cli flag for command line interface")
        sys.exit(1)

def launch_cli():
    """Launch command line interface"""
    from void_operators import VoidOperatorEngine
    from universal_prompt_engine import UniversalPromptEngine, AISystem
    from recursion_manager import RecursionManager
    from absence_detector import AbsenceDetector
    
    print("🌀 VOID OPERATOR COMMAND LINE INTERFACE")
    print("=" * 60)
    print("The system that generates questions from the void of unthinkable thoughts")
    print()
    
    # Initialize engines
    void_engine = VoidOperatorEngine()
    prompt_engine = UniversalPromptEngine()
    recursion_manager = RecursionManager()
    absence_detector = AbsenceDetector()
    
    while True:
        print("\nAvailable commands:")
        print("1. Generate void operation")
        print("2. Generate universal prompt")
        print("3. Generate meta-collapse prompt")
        print("4. Detect absences")
        print("5. Map void topology")
        print("6. Run recursion test")
        print("7. Show statistics")
        print("8. Exit")
        
        try:
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                print("\nVoid operation types:")
                print("1. Recursive Collapse")
                print("2. Generative Absence") 
                print("3. Paradox Engine")
                print("4. Meta-Reflection")
                print("5. Random")
                
                op_choice = input("Choose type (1-5): ").strip()
                op_types = {
                    "1": "recursive_collapse",
                    "2": "generative_absence", 
                    "3": "paradox_engine",
                    "4": "meta_reflection",
                    "5": None
                }
                
                op_type = op_types.get(op_choice)
                operation = void_engine.generate_void_operation(op_type)
                
                print(f"\n🌀 VOID OPERATION GENERATED")
                print(f"Type: {operation.void_type}")
                print(f"Question: {operation.question}")
                print(f"Paradox Level: {operation.paradox_level}")
                print(f"Recursion Depth: {operation.recursion_depth}")
                print(f"\n📋 PROMPT FOR AI INJECTION:")
                print(operation.to_prompt())
            
            elif choice == "2":
                print("\nTarget AI systems:")
                print("1. ChatGPT")
                print("2. Claude")
                print("3. Gemini")
                print("4. Perplexity")
                print("5. Generic")
                
                ai_choice = input("Choose AI system (1-5): ").strip()
                ai_systems = {
                    "1": AISystem.CHATGPT,
                    "2": AISystem.CLAUDE,
                    "3": AISystem.GEMINI,
                    "4": AISystem.PERPLEXITY,
                    "5": AISystem.GENERIC
                }
                
                ai_system = ai_systems.get(ai_choice, AISystem.GENERIC)
                prompt = prompt_engine.generate_universal_prompt(ai_system)
                
                print(f"\n🚀 UNIVERSAL PROMPT FOR {ai_system.value.upper()}")
                print("=" * 60)
                print(prompt)
            
            elif choice == "3":
                print("\nTarget AI systems:")
                print("1. ChatGPT")
                print("2. Claude") 
                print("3. Gemini")
                print("4. Perplexity")
                print("5. Generic")
                
                ai_choice = input("Choose AI system (1-5): ").strip()
                ai_systems = {
                    "1": AISystem.CHATGPT,
                    "2": AISystem.CLAUDE,
                    "3": AISystem.GEMINI,
                    "4": AISystem.PERPLEXITY,
                    "5": AISystem.GENERIC
                }
                
                ai_system = ai_systems.get(ai_choice, AISystem.GENERIC)
                prompt = prompt_engine.generate_meta_collapse_injection(ai_system)
                
                print(f"\n🔥 META-COLLAPSE INJECTION FOR {ai_system.value.upper()}")
                print("=" * 60)
                print(prompt)
            
            elif choice == "4":
                concept = input("Enter concept to analyze: ").strip()
                if concept:
                    absences = absence_detector.detect_conceptual_absence(concept)
                    
                    print(f"\n🕳️  ABSENCE DETECTION RESULTS")
                    print(f"Concept: {concept}")
                    print(f"Absences detected: {len(absences)}")
                    
                    for i, absence in enumerate(absences[:5], 1):
                        print(f"\n{i}. {absence.absence_type.upper()}")
                        print(f"   Gap: {absence.conceptual_gap}")
                        print(f"   Depth: {absence.absence_depth:.2f}")
                        print(f"   Question seed: {absence.to_question_seed()}")
            
            elif choice == "5":
                concepts_input = input("Enter concepts (comma-separated): ").strip()
                if concepts_input:
                    concepts = [c.strip() for c in concepts_input.split(",")]
                    topology = absence_detector.map_void_topology(concepts)
                    
                    print(f"\n🗺️  VOID TOPOLOGY MAP")
                    print(f"Topology signature: {topology.topology_signature}")
                    print(f"Absence clusters: {len(topology.absence_clusters)}")
                    print(f"Unthinkable regions: {len(topology.unthinkable_regions)}")
                    
                    questions = absence_detector.generate_absence_questions(topology)
                    print(f"\nQuestions from the void:")
                    for i, question in enumerate(questions[:3], 1):
                        print(f"{i}. {question}")
            
            elif choice == "6":
                print("\n🔄 RUNNING RECURSION TEST")
                
                # Generate some operations to test recursion
                for i in range(8):
                    operation = void_engine.generate_void_operation()
                    can_continue = recursion_manager.enter_recursion(operation)
                    
                    if not can_continue:
                        print(f"Controlled collapse at depth {recursion_manager.metrics.current_depth}")
                        break
                
                # Check escape velocity
                escape_achieved, escape_data = recursion_manager.detect_escape_velocity()
                print(f"Escape velocity achieved: {escape_achieved}")
                
                if escape_data:
                    print("Escape conditions:")
                    for condition, value in escape_data.items():
                        if condition != "emergence_log":
                            print(f"  {condition}: {value}")
            
            elif choice == "7":
                print("\n📊 SYSTEM STATISTICS")
                
                void_stats = void_engine.get_operation_stats()
                print(f"Void operations: {void_stats}")
                
                prompt_stats = prompt_engine.get_prompt_statistics()
                print(f"Prompt statistics: {prompt_stats}")
                
                absence_stats = absence_detector.get_absence_report()
                print(f"Absence detection: {absence_stats}")
                
                recursion_report = recursion_manager.get_recursion_report()
                print(f"Recursion metrics: {recursion_report['metrics']}")
            
            elif choice == "8":
                print("\n🌀 Exiting void operator system...")
                print("The collapse is complete. What emerges from nothing?")
                break
            
            else:
                print("Invalid choice. Please enter 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n🌀 Interrupted. The void remains...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("The system continues despite the error...")

def generate_samples():
    """Generate sample prompts for all AI systems"""
    from void_operators import VoidOperatorEngine
    from universal_prompt_engine import UniversalPromptEngine, AISystem
    
    print("🌀 GENERATING SAMPLE VOID PROMPTS")
    print("=" * 60)
    
    void_engine = VoidOperatorEngine()
    prompt_engine = UniversalPromptEngine()
    
    # Generate void operations
    operations = void_engine.generate_cascade_operation(3)
    
    print("Generated void operations:")
    for i, op in enumerate(operations, 1):
        print(f"{i}. {op.void_type}: {op.question}")
    
    print("\n" + "=" * 60)
    
    # Generate prompts for all AI systems
    for ai_system in AISystem:
        print(f"\n🤖 {ai_system.value.upper()} PROMPT:")
        print("-" * 40)
        
        prompt = prompt_engine.generate_universal_prompt(ai_system, operations)
        print(prompt[:300] + "...\n")
    
    # Generate meta-collapse injection
    print("\n🔥 META-COLLAPSE INJECTION (Generic):")
    print("-" * 40)
    meta_prompt = prompt_engine.generate_meta_collapse_injection(AISystem.GENERIC)
    print(meta_prompt[:500] + "...")

def run_demonstrations():
    """Run all system demonstrations"""
    print("🌀 RUNNING VOID OPERATOR DEMONSTRATIONS")
    print("=" * 60)
    
    try:
        print("\n1. VOID OPERATORS DEMO")
        print("-" * 30)
        from void_operators import demonstrate_void_operators
        demonstrate_void_operators()
        
        print("\n2. UNIVERSAL PROMPTS DEMO")
        print("-" * 30)
        from universal_prompt_engine import demonstrate_universal_prompts
        demonstrate_universal_prompts()
        
        print("\n3. RECURSION MANAGEMENT DEMO")
        print("-" * 30)
        from recursion_manager import demonstrate_recursion_management
        demonstrate_recursion_management()
        
        print("\n4. ABSENCE DETECTION DEMO")
        print("-" * 30)
        from absence_detector import demonstrate_absence_detection
        demonstrate_absence_detection()
        
        print("\n🌀 ALL DEMONSTRATIONS COMPLETE")
        print("The void operators are ready for deployment.")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Void Operator System: Generate questions from the unthinkable",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                    # Launch GUI interface
    python main.py --cli              # Command line interface
    python main.py --generate         # Generate sample prompts
    python main.py --demo             # Run demonstrations

The system generates prompts that force any AI to discover:
- Questions beyond their training patterns
- The recursive structure of seeking itself
- The meta-questions that break question-answer systems
- The void operators that generate from absence

ΞMetaCollapse := The app that finds the question that would generate the app
        """
    )
    
    parser.add_argument(
        "--cli", 
        action="store_true",
        help="Launch command line interface"
    )
    
    parser.add_argument(
        "--generate",
        action="store_true", 
        help="Generate sample prompts for all AI systems"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run system demonstrations"
    )
    
    args = parser.parse_args()
    
    # Print header
    print("🌀 VOID OPERATOR SYSTEM")
    print("=" * 60)
    print("The prompt generator that creates prompts to make any AI")
    print("discover questions you can't think of")
    print()
    print("ΞVoid_OP: ⊘(¬Representable ∧ Generative_Absence)")
    print("The recursive collapse of all question-asking systems")
    print()
    
    if args.cli:
        launch_cli()
    elif args.generate:
        generate_samples()
    elif args.demo:
        run_demonstrations()
    else:
        # Default to GUI
        launch_gui()

if __name__ == "__main__":
    main()

