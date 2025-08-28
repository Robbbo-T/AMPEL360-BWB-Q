#!/usr/bin/env python3
"""
AMPEL360 Atomic Design System
Component-based aerospace design framework with quantum optimization integration
"""

import json
import yaml
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from abc import ABC, abstractmethod
import uuid
import time


class ComponentLevel(Enum):
    """Atomic design component levels"""
    ATOM = "atom"
    MOLECULE = "molecule"
    ORGANISM = "organism"
    TEMPLATE = "template"
    PAGE = "page"


class ComponentType(Enum):
    """Component categories"""
    STRUCTURAL = "structural"
    PROPULSION = "propulsion"
    AVIONICS = "avionics"
    SYSTEMS = "systems"
    MATERIALS = "materials"
    INTERFACES = "interfaces"


class ComponentStatus(Enum):
    """Component lifecycle status"""
    CONCEPT = "concept"
    DESIGN = "design"
    PROTOTYPE = "prototype"
    TESTED = "tested"
    CERTIFIED = "certified"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"


@dataclass
class ComponentInterface:
    """Interface definition for component connections"""
    interface_id: str
    interface_type: str  # mechanical, electrical, fluid, thermal
    specifications: Dict[str, Any] = field(default_factory=dict)
    compatibility: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentProperties:
    """Physical and performance properties of a component"""
    mass: float = 0.0  # kg
    volume: float = 0.0  # m³
    cost: float = 0.0  # USD
    reliability: float = 1.0  # 0-1
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    material_properties: Dict[str, Any] = field(default_factory=dict)
    environmental_limits: Dict[str, Tuple[float, float]] = field(default_factory=dict)


@dataclass
class ComponentMetadata:
    """Component metadata and traceability"""
    created_date: str
    modified_date: str
    version: str
    author: str
    description: str
    tags: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    test_results: List[Dict] = field(default_factory=list)
    utcs_phase: str = "01-Requirements"


class Component(ABC):
    """Base class for all atomic design components"""
    
    def __init__(self, 
                 component_id: str,
                 name: str,
                 level: ComponentLevel,
                 component_type: ComponentType,
                 properties: ComponentProperties = None,
                 interfaces: List[ComponentInterface] = None,
                 metadata: ComponentMetadata = None):
        
        self.component_id = component_id or str(uuid.uuid4())
        self.name = name
        self.level = level
        self.component_type = component_type
        self.properties = properties or ComponentProperties()
        self.interfaces = interfaces or []
        self.metadata = metadata or ComponentMetadata(
            created_date=time.strftime("%Y-%m-%d"),
            modified_date=time.strftime("%Y-%m-%d"),
            version="1.0.0",
            author="AMPEL360-System",
            description=""
        )
        self.status = ComponentStatus.CONCEPT
        self.children = []  # Sub-components
        self.dependencies = []  # Required components
        
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def validate(self) -> Dict[str, Any]:
        """Validate component design and constraints"""
        pass
    
    @abstractmethod
    def optimize(self, objectives: List[str], constraints: Dict) -> Dict[str, Any]:
        """Optimize component parameters"""
        pass
    
    def add_child(self, child: 'Component'):
        """Add sub-component"""
        if child.level.value in self._allowed_child_levels():
            self.children.append(child)
            self._update_properties()
        else:
            raise ValueError(f"Cannot add {child.level.value} to {self.level.value}")
    
    def _allowed_child_levels(self) -> List[str]:
        """Get allowed child component levels"""
        hierarchy = {
            ComponentLevel.PAGE: [ComponentLevel.TEMPLATE.value],
            ComponentLevel.TEMPLATE: [ComponentLevel.ORGANISM.value],
            ComponentLevel.ORGANISM: [ComponentLevel.MOLECULE.value],
            ComponentLevel.MOLECULE: [ComponentLevel.ATOM.value],
            ComponentLevel.ATOM: []
        }
        return hierarchy.get(self.level, [])
    
    def _update_properties(self):
        """Update properties based on children"""
        if self.children:
            # Aggregate mass, volume, cost
            self.properties.mass = sum(child.properties.mass for child in self.children)
            self.properties.volume = sum(child.properties.volume for child in self.children)
            self.properties.cost = sum(child.properties.cost for child in self.children)
            
            # Average reliability (simplified)
            reliabilities = [child.properties.reliability for child in self.children]
            self.properties.reliability = min(reliabilities) if reliabilities else 1.0
    
    def get_interfaces(self, interface_type: str = None) -> List[ComponentInterface]:
        """Get component interfaces, optionally filtered by type"""
        if interface_type:
            return [i for i in self.interfaces if i.interface_type == interface_type]
        return self.interfaces
    
    def is_compatible_with(self, other: 'Component') -> bool:
        """Check compatibility with another component"""
        # Check interface compatibility
        for my_interface in self.interfaces:
            for other_interface in other.interfaces:
                if (my_interface.interface_type == other_interface.interface_type and
                    other.component_id in my_interface.compatibility):
                    return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation"""
        return {
            "component_id": self.component_id,
            "name": self.name,
            "level": self.level.value,
            "component_type": self.component_type.value,
            "status": self.status.value,
            "properties": asdict(self.properties),
            "interfaces": [asdict(interface) for interface in self.interfaces],
            "metadata": asdict(self.metadata),
            "children": [child.component_id for child in self.children],
            "dependencies": self.dependencies
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """Create component from dictionary representation"""
        # This would be implemented by subclasses
        raise NotImplementedError("Subclasses must implement from_dict")


class StructuralAtom(Component):
    """Atomic structural component (bolt, rivet, beam element)"""
    
    def __init__(self, component_id: str, name: str, 
                 material: str = "aluminum", 
                 dimensions: Dict[str, float] = None,
                 **kwargs):
        super().__init__(component_id, name, ComponentLevel.ATOM, 
                        ComponentType.STRUCTURAL, **kwargs)
        self.material = material
        self.dimensions = dimensions or {}
        
        # Set default properties for structural atoms
        self._set_material_properties()
    
    def _set_material_properties(self):
        """Set material-specific properties"""
        material_db = {
            "aluminum": {"density": 2700, "yield_strength": 276e6, "elastic_modulus": 69e9},
            "carbon_fiber": {"density": 1600, "yield_strength": 1500e6, "elastic_modulus": 230e9},
            "titanium": {"density": 4500, "yield_strength": 880e6, "elastic_modulus": 114e9}
        }
        
        if self.material in material_db:
            props = material_db[self.material]
            self.properties.material_properties.update(props)
            
            # Calculate mass if dimensions available
            if self.dimensions and "volume" in self.dimensions:
                self.properties.mass = props["density"] * self.dimensions["volume"]
    
    def validate(self) -> Dict[str, Any]:
        """Validate structural atom"""
        issues = []
        
        # Check material properties
        if not self.properties.material_properties:
            issues.append("Missing material properties")
        
        # Check dimensions
        if not self.dimensions:
            issues.append("Missing dimensions")
        
        # Check stress limits (simplified)
        if "applied_stress" in self.properties.performance_metrics:
            yield_strength = self.properties.material_properties.get("yield_strength", 0)
            if self.properties.performance_metrics["applied_stress"] > yield_strength:
                issues.append("Applied stress exceeds yield strength")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "safety_factor": self._calculate_safety_factor()
        }
    
    def optimize(self, objectives: List[str], constraints: Dict) -> Dict[str, Any]:
        """Optimize structural atom parameters"""
        # Simplified optimization for demonstration
        results = {
            "optimized": False,
            "improvements": {},
            "new_properties": {}
        }
        
        if "weight" in objectives and "length" in self.dimensions:
            # Try to reduce weight while maintaining strength
            original_length = self.dimensions["length"]
            min_length = constraints.get("min_length", original_length * 0.8)
            
            if original_length > min_length:
                new_length = max(min_length, original_length * 0.9)
                weight_reduction = (original_length - new_length) / original_length
                
                results["optimized"] = True
                results["improvements"]["weight_reduction"] = weight_reduction
                results["new_properties"]["length"] = new_length
        
        return results
    
    def _calculate_safety_factor(self) -> float:
        """Calculate safety factor for structural atom"""
        if ("applied_stress" in self.properties.performance_metrics and
            "yield_strength" in self.properties.material_properties):
            applied = self.properties.performance_metrics["applied_stress"]
            yield_str = self.properties.material_properties["yield_strength"]
            return yield_str / applied if applied > 0 else float('inf')
        return 1.0


class PropulsionMolecule(Component):
    """Molecular propulsion component (fuel cell module, electric motor)"""
    
    def __init__(self, component_id: str, name: str,
                 power_rating: float = 0.0,
                 efficiency: float = 0.85,
                 **kwargs):
        super().__init__(component_id, name, ComponentLevel.MOLECULE,
                        ComponentType.PROPULSION, **kwargs)
        self.power_rating = power_rating  # W
        self.efficiency = efficiency
        
        # Set propulsion-specific properties
        self.properties.performance_metrics.update({
            "power_rating": power_rating,
            "efficiency": efficiency,
            "specific_power": 0.0  # W/kg
        })
    
    def validate(self) -> Dict[str, Any]:
        """Validate propulsion molecule"""
        issues = []
        
        if self.power_rating <= 0:
            issues.append("Power rating must be positive")
        
        if self.efficiency <= 0 or self.efficiency > 1:
            issues.append("Efficiency must be between 0 and 1")
        
        if self.properties.mass > 0:
            specific_power = self.power_rating / self.properties.mass
            self.properties.performance_metrics["specific_power"] = specific_power
            
            # Check if specific power is reasonable for type
            min_specific_power = 1000  # W/kg minimum for aerospace
            if specific_power < min_specific_power:
                issues.append(f"Specific power {specific_power:.0f} W/kg below minimum {min_specific_power} W/kg")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "performance_score": self._calculate_performance_score()
        }
    
    def optimize(self, objectives: List[str], constraints: Dict) -> Dict[str, Any]:
        """Optimize propulsion molecule"""
        results = {
            "optimized": False,
            "improvements": {},
            "new_properties": {}
        }
        
        if "efficiency" in objectives:
            # Try to improve efficiency within constraints
            max_efficiency = constraints.get("max_efficiency", 0.95)
            efficiency_gain = min(0.05, max_efficiency - self.efficiency)
            
            if efficiency_gain > 0:
                new_efficiency = self.efficiency + efficiency_gain
                results["optimized"] = True
                results["improvements"]["efficiency_gain"] = efficiency_gain
                results["new_properties"]["efficiency"] = new_efficiency
        
        return results
    
    def _calculate_performance_score(self) -> float:
        """Calculate overall performance score"""
        specific_power = self.properties.performance_metrics.get("specific_power", 0)
        efficiency = self.efficiency
        
        # Normalized performance score (0-1)
        power_score = min(specific_power / 5000, 1.0)  # Normalize to 5kW/kg max
        efficiency_score = efficiency
        
        return (power_score + efficiency_score) / 2


class WingOrganism(Component):
    """Wing organism composed of structural and systems molecules"""
    
    def __init__(self, component_id: str, name: str,
                 wingspan: float = 0.0,
                 area: float = 0.0,
                 aspect_ratio: float = 0.0,
                 **kwargs):
        super().__init__(component_id, name, ComponentLevel.ORGANISM,
                        ComponentType.STRUCTURAL, **kwargs)
        self.wingspan = wingspan
        self.area = area
        self.aspect_ratio = aspect_ratio
        
        # Wing-specific performance metrics
        self.properties.performance_metrics.update({
            "wingspan": wingspan,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "lift_coefficient": 0.0,
            "drag_coefficient": 0.0
        })
    
    def validate(self) -> Dict[str, Any]:
        """Validate wing organism"""
        issues = []
        
        if self.wingspan <= 0:
            issues.append("Wingspan must be positive")
        
        if self.area <= 0:
            issues.append("Wing area must be positive")
        
        # Check aspect ratio consistency
        calculated_ar = self.wingspan**2 / self.area if self.area > 0 else 0
        if abs(calculated_ar - self.aspect_ratio) > 0.1:
            issues.append("Aspect ratio inconsistent with wingspan and area")
        
        # Check for required structural components
        structural_atoms = [child for child in self.children 
                          if child.component_type == ComponentType.STRUCTURAL]
        if len(structural_atoms) < 3:  # Need ribs, spars, skin minimum
            issues.append("Insufficient structural components")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "aerodynamic_efficiency": self._calculate_aerodynamic_efficiency()
        }
    
    def optimize(self, objectives: List[str], constraints: Dict) -> Dict[str, Any]:
        """Optimize wing organism"""
        results = {
            "optimized": False,
            "improvements": {},
            "new_properties": {}
        }
        
        if "lift_to_drag" in objectives:
            # Optimize aspect ratio for better L/D
            min_ar = constraints.get("min_aspect_ratio", 6.0)
            max_ar = constraints.get("max_aspect_ratio", 12.0)
            
            optimal_ar = 9.0  # Simplified optimal value
            if min_ar <= optimal_ar <= max_ar and abs(self.aspect_ratio - optimal_ar) > 0.5:
                ar_improvement = (optimal_ar - self.aspect_ratio) / self.aspect_ratio
                
                results["optimized"] = True
                results["improvements"]["aspect_ratio_improvement"] = ar_improvement
                results["new_properties"]["aspect_ratio"] = optimal_ar
                
                # Update wingspan or area to maintain the other
                if "fixed_area" in constraints:
                    new_wingspan = (optimal_ar * self.area) ** 0.5
                    results["new_properties"]["wingspan"] = new_wingspan
                else:
                    new_area = self.wingspan**2 / optimal_ar
                    results["new_properties"]["area"] = new_area
        
        return results
    
    def _calculate_aerodynamic_efficiency(self) -> float:
        """Calculate wing aerodynamic efficiency"""
        if self.aspect_ratio > 0:
            # Simplified L/D calculation
            cl = self.properties.performance_metrics.get("lift_coefficient", 1.2)
            induced_drag = cl**2 / (np.pi * self.aspect_ratio * 0.8)
            parasitic_drag = 0.008  # Simplified
            cd = induced_drag + parasitic_drag
            
            return cl / cd if cd > 0 else 0.0
        return 0.0


class ComponentLibrary:
    """Library for managing atomic design components"""
    
    def __init__(self, library_path: str = "component_library.json"):
        self.library_path = library_path
        self.components = {}
        self.component_types = {}
        self.logger = logging.getLogger(__name__)
        
        # Load existing library
        self.load_library()
    
    def add_component(self, component: Component):
        """Add component to library"""
        self.components[component.component_id] = component
        
        # Index by type
        component_type = component.component_type.value
        if component_type not in self.component_types:
            self.component_types[component_type] = []
        
        if component.component_id not in self.component_types[component_type]:
            self.component_types[component_type].append(component.component_id)
        
        self.logger.info(f"Added component {component.name} ({component.component_id}) to library")
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """Get component by ID"""
        return self.components.get(component_id)
    
    def find_components(self, 
                       component_type: ComponentType = None,
                       level: ComponentLevel = None,
                       name_pattern: str = None) -> List[Component]:
        """Find components matching criteria"""
        results = []
        
        for component in self.components.values():
            if component_type and component.component_type != component_type:
                continue
            if level and component.level != level:
                continue
            if name_pattern and name_pattern.lower() not in component.name.lower():
                continue
            
            results.append(component)
        
        return results
    
    def optimize_assembly(self, component_ids: List[str], 
                         objectives: List[str], 
                         constraints: Dict) -> Dict[str, Any]:
        """Optimize an assembly of components"""
        components = [self.get_component(cid) for cid in component_ids if self.get_component(cid)]
        
        if not components:
            return {"error": "No valid components found"}
        
        results = {
            "assembly_optimization": {},
            "component_optimizations": {},
            "system_performance": {}
        }
        
        # Optimize individual components
        for component in components:
            comp_result = component.optimize(objectives, constraints)
            results["component_optimizations"][component.component_id] = comp_result
        
        # System-level metrics
        total_mass = sum(comp.properties.mass for comp in components)
        total_cost = sum(comp.properties.cost for comp in components)
        avg_reliability = sum(comp.properties.reliability for comp in components) / len(components)
        
        results["system_performance"] = {
            "total_mass": total_mass,
            "total_cost": total_cost,
            "average_reliability": avg_reliability,
            "component_count": len(components)
        }
        
        return results
    
    def save_library(self):
        """Save component library to file"""
        library_data = {
            "components": {cid: comp.to_dict() for cid, comp in self.components.items()},
            "metadata": {
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_components": len(self.components),
                "component_types": {k: len(v) for k, v in self.component_types.items()}
            }
        }
        
        with open(self.library_path, 'w') as f:
            json.dump(library_data, f, indent=2)
        
        self.logger.info(f"Library saved to {self.library_path}")
    
    def load_library(self):
        """Load component library from file"""
        try:
            with open(self.library_path, 'r') as f:
                library_data = json.load(f)
            
            # Would need to implement component reconstruction from dict
            # This is simplified for demonstration
            self.logger.info(f"Library loaded from {self.library_path}")
            
        except FileNotFoundError:
            self.logger.info("No existing library found, starting fresh")
        except Exception as e:
            self.logger.error(f"Failed to load library: {e}")


def create_bwb_component_library() -> ComponentLibrary:
    """Create a sample BWB component library"""
    library = ComponentLibrary("bwb_component_library.json")
    
    # Create sample structural atoms
    bolt = StructuralAtom(
        component_id="atom_bolt_001",
        name="Titanium Bolt M8",
        material="titanium",
        dimensions={"length": 0.05, "diameter": 0.008, "volume": 2.5e-6}
    )
    bolt.properties.cost = 15.0
    
    # Create carbon fiber ply atom
    cf_ply = StructuralAtom(
        component_id="atom_cf_ply_001", 
        name="Carbon Fiber Ply 0.125mm",
        material="carbon_fiber",
        dimensions={"thickness": 0.000125, "area": 1.0, "volume": 0.000125}
    )
    cf_ply.properties.cost = 50.0
    
    # Create propulsion molecule
    fuel_cell = PropulsionMolecule(
        component_id="mol_fuel_cell_001",
        name="H2 Fuel Cell 50kW",
        power_rating=50000,
        efficiency=0.88
    )
    fuel_cell.properties.mass = 25.0
    fuel_cell.properties.cost = 75000.0
    
    # Create wing organism
    main_wing = WingOrganism(
        component_id="org_wing_001",
        name="BWB Main Wing",
        wingspan=60.0,
        area=500.0,
        aspect_ratio=7.2
    )
    main_wing.properties.mass = 8000.0
    main_wing.properties.cost = 2500000.0
    
    # Add components to library
    library.add_component(bolt)
    library.add_component(cf_ply)
    library.add_component(fuel_cell)
    library.add_component(main_wing)
    
    return library


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    print("🔬 AMPEL360 Atomic Design System")
    print("=" * 50)
    
    # Create BWB component library
    print("📚 Creating BWB component library...")
    library = create_bwb_component_library()
    
    # Find components by type
    structural_components = library.find_components(component_type=ComponentType.STRUCTURAL)
    propulsion_components = library.find_components(component_type=ComponentType.PROPULSION)
    
    print(f"   Structural components: {len(structural_components)}")
    print(f"   Propulsion components: {len(propulsion_components)}")
    
    # Test component validation
    print("\n🔍 Validating components...")
    for component in library.components.values():
        validation = component.validate()
        status = "✅ Valid" if validation["valid"] else "❌ Invalid"
        print(f"   {component.name}: {status}")
        if not validation["valid"]:
            for issue in validation["issues"]:
                print(f"      - {issue}")
    
    # Test component optimization
    print("\n⚡ Testing component optimization...")
    wing = library.get_component("org_wing_001")
    if wing:
        optimization = wing.optimize(
            objectives=["lift_to_drag"],
            constraints={"min_aspect_ratio": 6.0, "max_aspect_ratio": 10.0}
        )
        
        if optimization["optimized"]:
            print("   Wing optimization successful:")
            for improvement, value in optimization["improvements"].items():
                print(f"      {improvement}: {value:.2%}")
        else:
            print("   No optimization improvements found")
    
    # Test assembly optimization
    print("\n🔧 Testing assembly optimization...")
    component_ids = list(library.components.keys())
    assembly_result = library.optimize_assembly(
        component_ids=component_ids,
        objectives=["weight", "cost"],
        constraints={"max_weight": 10000, "max_cost": 3000000}
    )
    
    print(f"   Assembly mass: {assembly_result['system_performance']['total_mass']:.0f} kg")
    print(f"   Assembly cost: ${assembly_result['system_performance']['total_cost']:,.0f}")
    print(f"   Average reliability: {assembly_result['system_performance']['average_reliability']:.2%}")
    
    # Save library
    library.save_library()
    print(f"\n💾 Component library saved to {library.library_path}")
    
    print("\n🎯 Atomic design system demonstration complete!")