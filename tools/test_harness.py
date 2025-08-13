"""
Testing harness for Janus psychological profiling system.
Runs predefined decision sequences and reports detailed results.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add src to path to import game modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from engine import (
    default_state, load_scenarios, apply_choice_effects,
    StateManager,
    generate_decision_recap, generate_final_epilogue,
    Telemetry
)
from modules.scoring import top_archetype


class TestHarness:
    """Test harness for running automated game sequences."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
        self.scenarios = load_scenarios(self.data_path)
        self.test_results = []
        
    def create_test_scenario(self, name: str, description: str, decisions: List[Tuple[str, int]]) -> Dict[str, Any]:
        """
        Create a test scenario with predefined decisions.
        
        Args:
            name: Test scenario name
            description: What this test is checking
            decisions: List of (scene_id, choice_index) tuples
        """
        return {
            "name": name,
            "description": description,
            "decisions": decisions,
            "expected_traits": {},  # Can be filled in later
            "expected_reveal_type": None
        }
    
    def run_test_scenario(self, test_scenario: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        """Run a single test scenario and return detailed results."""
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"TEST: {test_scenario['name']}")
            print(f"{'='*80}")
            print(f"Description: {test_scenario['description']}")
            print()
        
        # Initialize game state
        state = default_state()
        state["player"]["name"] = f"TestPlayer_{test_scenario['name']}"
        telemetry = Telemetry(None)  # No file output for tests
        
        results = {
            "test_name": test_scenario['name'],
            "decisions_made": [],
            "trait_progression": [],
            "final_traits": {},
            "final_reveal": "",
            "success": True,
            "errors": []
        }
        
        try:
            # Process each decision
            for decision_step, (target_scene_id, choice_index) in enumerate(test_scenario['decisions']):
                if verbose:
                    print(f"\nDECISION {decision_step + 1}:")
                    print(f"Target Scene: {target_scene_id}")
                
                # Find the scene across all acts
                scene_found = None
                for act_num, scenes in self.scenarios.items():
                    for scene in scenes:
                        if scene.get("scene_id") == target_scene_id:
                            scene_found = scene
                            break
                    if scene_found:
                        break
                
                if not scene_found:
                    error_msg = f"Scene '{target_scene_id}' not found"
                    results["errors"].append(error_msg)
                    if verbose:
                        print(f"ERROR: {error_msg}")
                    continue
                
                # Display scene context
                if verbose:
                    print(f"Scene Text: {scene_found.get('text', 'No text')}")
                    print("Available Choices:")
                    for i, choice in enumerate(scene_found.get('choices', [])):
                        marker = ">>>" if i == choice_index else "   "
                        print(f"  {marker} {i+1}. {choice.get('text', 'No text')}")
                
                # Validate choice index
                choices = scene_found.get('choices', [])
                if choice_index >= len(choices):
                    error_msg = f"Choice index {choice_index} out of range for scene '{target_scene_id}'"
                    results["errors"].append(error_msg)
                    if verbose:
                        print(f"ERROR: {error_msg}")
                    continue
                
                chosen_choice = choices[choice_index]
                
                # Record decision
                decision_record = {
                    "step": decision_step + 1,
                    "scene_id": target_scene_id,
                    "choice_index": choice_index,
                    "choice_text": chosen_choice.get('text', ''),
                    "primary_trait": chosen_choice.get('primary_trait'),
                    "primary_weight": chosen_choice.get('primary_weight', 0.0),
                    "secondary_trait": chosen_choice.get('secondary_trait'),
                    "secondary_weight": chosen_choice.get('secondary_weight', 0.0)
                }
                results["decisions_made"].append(decision_record)
                
                # Apply choice effects
                state_mgr = StateManager(state)
                traits_before = dict(state["memory"]["trait_scores"])
                apply_choice_effects(state, chosen_choice, state_mgr, telemetry, debug_mode=True)
                traits_after = dict(state["memory"]["trait_scores"])
                
                # Record trait changes
                trait_changes = {}
                for trait, new_value in traits_after.items():
                    old_value = traits_before.get(trait, 0.0)
                    if new_value != old_value:
                        trait_changes[trait] = {
                            "before": old_value,
                            "after": new_value,
                            "change": new_value - old_value
                        }
                
                results["trait_progression"].append({
                    "after_decision": decision_step + 1,
                    "traits": dict(traits_after),
                    "changes": trait_changes
                })
                
                if verbose:
                    print(f"Chosen: {chosen_choice.get('text', '')}")
                    if trait_changes:
                        print("Trait Changes:")
                        for trait, change_info in trait_changes.items():
                            print(f"  {trait}: {change_info['before']:.1f} -> {change_info['after']:.1f} (+{change_info['change']:.1f})")
                    else:
                        print("No trait changes (decoy choice)")
            
            # Final analysis
            results["final_traits"] = dict(state["memory"]["trait_scores"])
            
            # Generate final chronicle summary
            recap = generate_decision_recap(state)
            archetype_name, archetype_desc = top_archetype(state_mgr.trait_scores)
            epilogue = generate_final_epilogue(state_mgr)
            results["final_reveal"] = "\n".join(
                part for part in [recap, f"{archetype_name}: {archetype_desc}", epilogue] if part
            )
            
            if verbose:
                print(f"\n{'='*40}")
                print("FINAL RESULTS")
                print(f"{'='*40}")
                print("Final Trait Scores:")
                if results["final_traits"]:
                    sorted_traits = sorted(results["final_traits"].items(), key=lambda x: x[1], reverse=True)
                    for trait, value in sorted_traits:
                        print(f"  {trait}: {value:.1f}")
                else:
                    print("  No traits accumulated")
                
                print(f"\nFinal Reveal:")
                print(f"  {results['final_reveal']}")
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Unexpected error: {str(e)}")
            if verbose:
                print(f"ERROR: {str(e)}")
        
        return results
    
    def create_sample_tests(self) -> List[Dict[str, Any]]:
        """Create some sample test scenarios."""
        tests = []
        
        # Test 1: High Wrath pathway
        tests.append(self.create_test_scenario(
            name="HighWrath",
            description="Test pathway that should accumulate high Wrath trait",
            decisions=[
                ("shattered_clock", 1),  # Strike the clock (Wrath +0.2)
                ("whisper_gallery", 0),  # Demand portrait speak (Wrath +0.2, Control +0.1)
                ("twin_scholar", 0),     # Dissect their argument (likely high Wrath)
                ("mask_market", 0),      # Haggle ruthlessly (likely Avarice/Control)
            ]
        ))
        
        # Test 2: High Rigidity/Control pathway  
        tests.append(self.create_test_scenario(
            name="HighControl",
            description="Test pathway emphasizing order and control",
            decisions=[
                ("mirror_pool", 1),        # Stand motionless (Rigidity +0.2)
                ("labyrinth_library", 0),  # Methodically reorder (likely Control)
                ("frozen_echo", 1),        # Listen to echo (patience/control)
                ("twin_scholar", 1),       # Applaud politely (restraint)
            ]
        ))
        
        # Test 3: Mixed decoy pathway
        tests.append(self.create_test_scenario(
            name="MixedDecoys",
            description="Test pathway with many decoy choices (should show low scores)",
            decisions=[
                ("mask_market", 2),         # Browse without buying (Apathy 0.0)
                ("labyrinth_library", 2),   # Browse and leave (Apathy 0.0) 
                ("twin_scholar", 1),        # Applaud politely (Apathy 0.0)
                ("frozen_echo", 1),         # Listen to echo (Apathy 0.0)
            ]
        ))
        
        return tests
    
    def run_all_tests(self, tests: List[Dict[str, Any]] = None, verbose: bool = True) -> List[Dict[str, Any]]:
        """Run all test scenarios and return results."""
        if tests is None:
            tests = self.create_sample_tests()
        
        all_results = []
        
        for test in tests:
            result = self.run_test_scenario(test, verbose)
            all_results.append(result)
        
        return all_results
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate a summary report of all test results."""
        report = []
        report.append("\n" + "="*80)
        report.append("TEST HARNESS SUMMARY REPORT")
        report.append("="*80)
        
        for result in results:
            report.append(f"\nTest: {result['test_name']}")
            report.append(f"Success: {'✓' if result['success'] else '✗'}")
            report.append(f"Decisions Made: {len(result['decisions_made'])}")
            
            if result['errors']:
                report.append(f"Errors: {len(result['errors'])}")
                for error in result['errors']:
                    report.append(f"  - {error}")
            
            if result['final_traits']:
                top_trait = max(result['final_traits'].items(), key=lambda x: x[1])
                report.append(f"Top Trait: {top_trait[0]} ({top_trait[1]:.1f})")
            else:
                report.append("Top Trait: None")
            
            report.append(f"Reveal: {result['final_reveal'][:50]}{'...' if len(result['final_reveal']) > 50 else ''}")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Run the test harness
    harness = TestHarness()
    
    print("Janus Testing Harness")
    print("=====================")
    print("Running predefined test scenarios...")
    
    # Run all tests
    results = harness.run_all_tests(verbose=True)
    
    # Generate summary
    summary = harness.generate_summary_report(results)
    print(summary)
    
    # Optionally save detailed results to JSON
    output_file = Path("outputs/test_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: {output_file}")
