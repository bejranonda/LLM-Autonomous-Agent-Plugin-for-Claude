#!/usr/bin/env python3
"""
Dependency Graph Analyzer for Autonomous Claude Agent Plugin

Builds comprehensive dependency graphs, detects circular dependencies,
analyzes coupling metrics, and provides visualization capabilities.
"""

import ast
import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict, deque

class DependencyGraphAnalyzer:
    """Analyze code dependencies and build dependency graphs."""

    def __init__(self, project_root: str = "."):
        """Initialize dependency analyzer."""
        self.project_root = Path(project_root)
        self.dependency_graph = {}
        self.reverse_graph = {}
        self.file_asts = {}

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single Python file for dependencies.

        Args:
            file_path: Path to Python file

        Returns:
            Dictionary containing dependency information
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=str(file_path))
            self.file_asts[str(file_path)] = tree

            dependencies = {
                "file": str(file_path),
                "imports": [],
                "from_imports": [],
                "internal_deps": [],
                "external_deps": [],
                "functions": [],
                "classes": []
            }

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies["imports"].append({
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno
                        })

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        dependencies["from_imports"].append({
                            "module": module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "level": node.level,
                            "line": node.lineno
                        })

                elif isinstance(node, ast.FunctionDef):
                    dependencies["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args]
                    })

                elif isinstance(node, ast.ClassDef):
                    dependencies["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "bases": [
                            self._extract_base_name(base)
                            for base in node.bases
                        ]
                    })

            # Classify as internal or external
            project_name = self.project_root.name

            for imp in dependencies["imports"]:
                module = imp["module"]
                if self._is_internal_module(module, project_name):
                    dependencies["internal_deps"].append(imp)
                else:
                    dependencies["external_deps"].append(imp)

            for imp in dependencies["from_imports"]:
                module = imp["module"]
                if imp["level"] > 0 or self._is_internal_module(module, project_name):
                    dependencies["internal_deps"].append(imp)
                else:
                    dependencies["external_deps"].append(imp)

            return dependencies

        except Exception as e:
            return {
                "file": str(file_path),
                "error": str(e),
                "imports": [],
                "from_imports": [],
                "internal_deps": [],
                "external_deps": []
            }

    def _extract_base_name(self, base_node):
        """Extract base class name from AST node."""
        if isinstance(base_node, ast.Name):
            return base_node.id
        elif isinstance(base_node, ast.Attribute):
            return f"{base_node.value.id}.{base_node.attr}"
        else:
            return str(base_node)

    def _is_internal_module(self, module: str, project_name: str) -> bool:
        """Determine if module is internal to project."""
        if not module:
            return True  # Relative imports

        # Check if module starts with project name
        if module.startswith(project_name):
            return True

        # Check if module file exists in project
        module_path = self.project_root / module.replace(".", "/")
        if module_path.with_suffix(
    ".py").exists() or (module_path / "__init__.py").exists():,
)
            return True

        return False

    def build_dependency_graph(self, python_files: List[Path]) -> Dict[str, List[str]]:
        """
        Build complete dependency graph for project.

        Args:
            python_files: List of Python file paths

        Returns:
            Dictionary mapping files to their dependencies
        """
        self.dependency_graph = {}
        self.reverse_graph = defaultdict(list)

        for file_path in python_files:
            deps = self.analyze_file(file_path)

            # Extract module names from internal dependencies
            dep_modules = []
            for imp in deps["internal_deps"]:
                module = imp.get("module", "")
                if module:
                    dep_modules.append(module)

            self.dependency_graph[str(file_path)] = dep_modules

            # Build reverse graph
            for dep in dep_modules:
                self.reverse_graph[dep].append(str(file_path))

        return self.dependency_graph

    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detect circular dependencies using DFS.

        Returns:
            List of circular dependency chains
        """
        def dfs(
    node: str,
    visited: Set[str],
    rec_stack: Set[str],
    path: List[str]) -> List[List[str]]:,
)
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            cycles = []

            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    cycles.extend(dfs(neighbor, visited, rec_stack, path[:]))
                elif neighbor in rec_stack:
                    # Found a cycle
                    try:
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        cycles.append(cycle)
                    except ValueError:
                        pass

            rec_stack.discard(node)
            return cycles

        all_cycles = []
        visited = set()

        for node in self.dependency_graph:
            if node not in visited:
                cycles = dfs(node, visited, set(), [])
                all_cycles.extend(cycles)

        # Remove duplicate cycles
        unique_cycles = []
        seen = set()

        for cycle in all_cycles:
            # Normalize cycle (rotate to start with lexicographically smallest)
            normalized = tuple(cycle[cycle.index(min(cycle)):] + cycle[:cycle.index(min(cycle))])
            if normalized not in seen:
                seen.add(normalized)
                unique_cycles.append(list(normalized))

        return unique_cycles

    def calculate_coupling_metrics(self) -> Dict[str, Any]:
        """
        Calculate coupling metrics for each module.

        Returns:
            Dictionary containing coupling metrics
        """
        metrics = {
            "afferent_coupling": {},   # How many modules depend on this
            "efferent_coupling": {},   # How many modules this depends on
            "instability": {},          # Ce / (Ce + Ca)
            "abstractness": {}          # Abstract classes / Total classes
        }

        # Calculate afferent coupling (Ca)
        for module in self.dependency_graph:
            afferent_count = len(self.reverse_graph.get(module, []))
            metrics["afferent_coupling"][module] = afferent_count

        # Calculate efferent coupling (Ce)
        for module, deps in self.dependency_graph.items():
            efferent_count = len(deps)
            metrics["efferent_coupling"][module] = efferent_count

        # Calculate instability (I = Ce / (Ce + Ca))
        for module in self.dependency_graph:
            ce = metrics["efferent_coupling"].get(module, 0)
            ca = metrics["afferent_coupling"].get(module, 0)

            total = ce + ca
            metrics["instability"][module] = ce / max(total, 1)

        # Identify highly coupled modules
        highly_coupled = []
        for module in self.dependency_graph:
            total_coupling = (
                metrics["afferent_coupling"].get(module, 0) +
                metrics["efferent_coupling"].get(module, 0)
            )

            if total_coupling > 10:
                highly_coupled.append({
                    "module": module,
                    "afferent": metrics["afferent_coupling"][module],
                    "efferent": metrics["efferent_coupling"][module],
                    "instability": metrics["instability"][module],
                    "total": total_coupling
                })

        metrics["highly_coupled"] = sorted(
            highly_coupled,
            key=lambda x: x["total"],
            reverse=True
        )

        return metrics

    def find_dependency_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        Find shortest dependency path between two modules using BFS.

        Args:
            source: Source module
            target: Target module

        Returns:
            List representing dependency path, or None if no path exists
        """
        if source not in self.dependency_graph:
            return None

        queue = deque([(source, [source])])
        visited = {source}

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            for neighbor in self.dependency_graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def analyze_module_layers(self) -> Dict[int, List[str]]:
        """
        Organize modules into layers based on dependency depth.

        Returns:
            Dictionary mapping layer number to modules in that layer
        """
        layers = defaultdict(list)

        # Find modules with no dependencies (leaf modules)
        leaf_modules = [
            module for module, deps in self.dependency_graph.items()
            if len(deps) == 0
        ]

        layers[0] = leaf_modules
        visited = set(leaf_modules)

        layer_num = 1
        while len(visited) < len(self.dependency_graph):
            current_layer = []

            for module in self.dependency_graph:
                if module in visited:
                    continue

                # Check if all dependencies are in previous layers
                deps = self.dependency_graph[module]
                if all(dep in visited for dep in deps):
                    current_layer.append(module)
                    visited.add(module)

            if not current_layer:
                # Circular dependencies prevent clean layering
                remaining = set(self.dependency_graph.keys()) - visited
                layers[-1] = list(remaining)
                break

            layers[layer_num] = current_layer
            layer_num += 1

        return dict(layers)

    def calculate_impact_score(self, module: str) -> float:
        """
        Calculate impact score for a module (how many modules depend on it).

        Args:
            module: Module to calculate impact for

        Returns:
            Impact score (0-100)
        """
        # Direct dependents
        direct_dependents = len(self.reverse_graph.get(module, []))

        # Indirect dependents (BFS)
        indirect_dependents = set()
        visited = set()
        queue = deque([module])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.add(current)

            for dependent in self.reverse_graph.get(current, []):
                if dependent != module and dependent not in visited:
                    indirect_dependents.add(dependent)
                    queue.append(dependent)

        # Calculate score
        total_dependents = direct_dependents + len(indirect_dependents)
        total_modules = len(self.dependency_graph)

        impact_score = min(100, (total_dependents / max(total_modules, 1)) * 200)

        return impact_score

    def generate_dot_graph(
    self,
    output_file: str = "dependencies.dot",
    max_nodes: int = 50):,
)
        """
        Generate GraphViz DOT file for visualization.

        Args:
            output_file: Output file path
            max_nodes: Maximum number of nodes to include
        """
        # Limit to most important modules if too many
        if len(self.dependency_graph) > max_nodes:
            # Sort by coupling and take top modules
            coupling = self.calculate_coupling_metrics()
            sorted_modules = sorted(
                coupling["afferent_coupling"].items(),
                key=lambda x: x[1] + coupling["efferent_coupling"].get(x[0], 0),
                reverse=True
            )
            important_modules = set([m[0] for m in sorted_modules[:max_nodes]])
        else:
            important_modules = set(self.dependency_graph.keys())

        with open(output_file, 'w') as f:
            f.write("digraph Dependencies {\n")
            f.write("  rankdir=LR;\n")
            f.write("  node [shape=box, style=rounded];\n\n")

            # Write nodes
            for module in important_modules:
                # Simplify module name for display
                display_name = Path(module).stem
                f.write(f'  "{module}" [label="{display_name}"];\n')

            f.write("\n")

            # Write edges
            for module, deps in self.dependency_graph.items():
                if module not in important_modules:
                    continue

                for dep in deps:
                    if dep in important_modules:
                        f.write(f'  "{module}" -> "{dep}";\n')

            f.write("}\n")

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive dependency analysis report.

        Returns:
            Dictionary containing complete analysis
        """
        circular_deps = self.detect_circular_dependencies()
        coupling_metrics = self.calculate_coupling_metrics()
        layers = self.analyze_module_layers()

        # Calculate summary statistics
        total_modules = len(self.dependency_graph)
        total_deps = sum(len(deps) for deps in self.dependency_graph.values())
        avg_deps_per_module = total_deps / max(total_modules, 1)

        # Find critical modules (high impact)
        critical_modules = []
        for module in self.dependency_graph:
            impact = self.calculate_impact_score(module)
            if impact > 50:
                critical_modules.append({
                    "module": module,
                    "impact_score": impact,
                    "direct_dependents": len(self.reverse_graph.get(module, [])),
                    "dependencies": len(self.dependency_graph[module])
                })

        critical_modules.sort(key=lambda x: x["impact_score"], reverse=True)

        return {
            "summary": {
                "total_modules": total_modules,
                "total_dependencies": total_deps,
                "avg_dependencies_per_module": avg_deps_per_module,
                "circular_dependencies_count": len(circular_deps),
                "highly_coupled_modules_count": len(coupling_metrics["highly_coupled"]),
                "layer_count": len(layers)
            },
            "circular_dependencies": circular_deps,
            "coupling_metrics": {
                "highly_coupled": coupling_metrics["highly_coupled"][:10],  # Top 10
                "average_instability": sum(
    coupling_metrics["instability"].values()) / max(len(coupling_metrics["instability"]),
    1,
)
            },
            "critical_modules": critical_modules[:10],  # Top 10
            "architecture_layers": {
                str(k): v for k, v in layers.items()
            },
            "recommendations": self._generate_recommendations(
                circular_deps,
                coupling_metrics,
                critical_modules
            )
        }

    def _generate_recommendations(
        self,
        circular_deps: List[List[str]],
        coupling_metrics: Dict[str, Any],
        critical_modules: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []

        # Circular dependencies
        if len(circular_deps) > 0:
            recommendations.append(
                f"CRITICAL: Found {len(circular_deps)} circular dependencies. "
                "Break cycles by introducing interfaces or dependency injection."
            )

        # Highly coupled modules
        if len(coupling_metrics["highly_coupled"]) > 0:
            top_coupled = coupling_metrics["highly_coupled"][0]
            recommendations.append(
                f"HIGH: Module '{Path(top_coupled['module']).stem}' is highly coupled "
                f"({top_coupled['total']} total connections). Consider refactoring."
            )

        # Critical modules
        if len(critical_modules) > 0:
            top_critical = critical_modules[0]
            recommendations.append(
                f"MEDIUM: Module '{Path(top_critical['module']).stem}' is critical "
                f"(impact score: {top_critical['impact_score']:.1f}). "
                "Ensure comprehensive test coverage."
            )

        # Instability
        avg_instability = coupling_metrics.get("average_instability", 0.5)
        if avg_instability > 0.7:
            recommendations.append(
                f"MEDIUM: High average instability ({avg_instability:.2f}). "
                "Many modules depend on too many others. Consider stabilizing core modules."
            )

        if not recommendations:
            recommendations.append("Good: No major dependency issues detected.")

        return recommendations


def main():
    """Command-line interface for dependency graph analyzer."""
    parser = argparse.ArgumentParser(description='Dependency Graph Analyzer')
    parser.add_argument('--root', default='.', help='Project root directory')
    parser.add_argument(
    '--output',
    default='dependency_report.json',
    help='Output report file',
)
    parser.add_argument('--dot', help='Generate DOT file for GraphViz')
    parser.add_argument('--max-nodes', type=int, default=50, help='Max nodes in graph')

    args = parser.parse_args()

    analyzer = DependencyGraphAnalyzer(args.root)

    # Find all Python files
    project_root = Path(args.root)
    python_files = list(project_root.rglob("*.py"))

    if not python_files:
        print("No Python files found in project.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing {len(python_files)} Python files...")

    # Build dependency graph
    analyzer.build_dependency_graph(python_files)

    # Generate report
    report = analyzer.generate_report()

    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Report saved to: {args.output}")

    # Print summary
    summary = report["summary"]
    print(f"\n=== Dependency Analysis Summary ===")
    print(f"Total modules: {summary['total_modules']}")
    print(f"Total dependencies: {summary['total_dependencies']}")
    print(f"Avg dependencies per module: {summary['avg_dependencies_per_module']:.2f}")
    print(f"Circular dependencies: {summary['circular_dependencies_count']}")
    print(f"Highly coupled modules: {summary['highly_coupled_modules_count']}")
    print(f"Architecture layers: {summary['layer_count']}")

    # Print recommendations
    print(f"\n=== Recommendations ===")
    for rec in report["recommendations"]:
        print(f"  • {rec}")

    # Generate DOT file if requested
    if args.dot:
        analyzer.generate_dot_graph(args.dot, args.max_nodes)
        print(f"\n✓ GraphViz DOT file saved to: {args.dot}")
        print(f"  Generate PNG: dot -Tpng {args.dot} -o dependencies.png")


if __name__ == '__main__':
    main()
